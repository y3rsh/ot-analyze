import json
import os
import shutil
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, Iterator, List

from write_failed_analysis import write_failed_analysis

FILE_BASENAME = "protocols_and_analyses"


class ProtocolType(Enum):
    PROTOCOL_DESIGNER = auto()
    PYTHON = auto()



@dataclass
class ProtocolPaths:
    protocol_file: Path
    analysis_file: Path


def generate_analysis_path(protocol_file: Path) -> Path:
    """
    Takes a Path to a protocol file and returns a Path to the analysis file that
    should be generated by the analyze command.

    :param protocol_file: A Path to a protocol file.
    :return: A Path to the analysis file that should be generated by the analyze command.
    """
    return Path(protocol_file.parent, f"{protocol_file.stem}_analysis.json")


def analyze(protocol_path: ProtocolPaths) -> float:
    start_time = time.time()  # Start timing
    custom_labware_directory = Path(protocol_path.protocol_file.parent, "custom_labware")

    custom_labware = []
    # PD protocols contain their own custom labware
    if custom_labware_directory.is_dir() and protocol_path.protocol_file.suffix == ".py":
        custom_labware = [
            os.path.join(custom_labware_directory, file) for file in os.listdir(custom_labware_directory) if file.endswith(".json")
        ]

    command = [
        "python",
        "-I",
        "-m",
        "opentrons.cli",
        "analyze",
        "--json-output",
        protocol_path.analysis_file,
        protocol_path.protocol_file,
    ] + custom_labware
    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
    except Exception as e:
        print(f"Error in analysis of {protocol_path.protocol_file}")
        write_failed_analysis(protocol_path.analysis_file, e)
        end_time = time.time()
        return end_time - start_time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Successful analysis of {protocol_path.protocol_file} completed in {elapsed_time:.2f} seconds")
    return elapsed_time


def run_analyze_in_parallel(protocol_files: List[ProtocolPaths]):
    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(analyze, file) for file in protocol_files]
        accumulated_time = 0
        for future in as_completed(futures):
            try:
                accumulated_time += future.result()  # This blocks until the future is done
            except Exception as e:
                print(f"An error occurred: {e}")
        end_time = time.time()
        clock_time = end_time - start_time
        print(
            f"""{len(protocol_files)} protocols with total analysis time of {accumulated_time:.2f}seconds.
Analyzed in {clock_time:2f} seconds thanks to parallelization.
"""
        )


def has_designer_application(json_file_path):
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return "designerApplication" in data
    except json.JSONDecodeError:
        # Handle the exception if the file is not a valid JSON
        print(f"Invalid JSON file: {json_file_path}")
        return False




def find_protocol_paths(repo_relative_path: Path) -> List[ProtocolPaths]:
    def find_pd_protocols(directory: Path) -> List[Path]:
    # Check if the provided path is a valid directory
        if not directory.is_dir():
            raise NotADirectoryError(f"The path {directory} is not a valid directory.")

        # Recursively find all .json files
        json_files = list(directory.rglob("*.json"))
        filtered_json_files = [file for file in json_files if has_designer_application(file)]

        return filtered_json_files

    def find_python_protocols(directory: Path) -> List[Path]:
        # Check if the provided path is a valid directory
        if not directory.is_dir():
            raise NotADirectoryError(f"The path {directory} is not a valid directory.")

        # Recursively find all .py files
        python_files = list(directory.rglob("*.py"))
        # TODO: shallow test that they are valid protocol files
        return python_files
    return [
        ProtocolPaths(protocol_file, generate_analysis_path(protocol_file))
        for protocol_file
        in find_python_protocols(repo_relative_path) + find_pd_protocols(repo_relative_path)
    ]

def create_zip(directory_path: Path):
    absolute_directory_path = directory_path.absolute()
    try:
        archive_name = shutil.make_archive(FILE_BASENAME, 'zip', absolute_directory_path, absolute_directory_path)
        print(f"Zipfile created and saved to: {absolute_directory_path / archive_name}")

    except Exception as e:
        print(f"Error: {e}")


def main():
    repo_relative_path = Path(os.getenv("GITHUB_WORKSPACE"), os.getenv("INPUT_BASE_DIRECTORY"))
    print(f"Analyzing all protocol files in {repo_relative_path}")
    protocol_paths = find_protocol_paths(repo_relative_path)
    run_analyze_in_parallel(protocol_paths)
    create_zip(repo_relative_path)


if __name__ == "__main__":
    import contextlib

    @contextlib.contextmanager
    def set_env(**environ: Dict[str, str]) -> Iterator[None]:
        old_environ = dict(os.environ)
        os.environ.update(environ)
        try:
            yield
        finally:
            os.environ.clear()
            os.environ.update(old_environ)

    environ_vars_to_add = {}
    if os.getenv("GITHUB_WORKSPACE") is None:
        environ_vars_to_add["GITHUB_WORKSPACE"] = str(Path(__file__).parent.absolute())

    if os.getenv("INPUT_BASE_DIRECTORY") is None:
        environ_vars_to_add["INPUT_BASE_DIRECTORY"] = "../ot-analyze-test/protocols"
    if len(environ_vars_to_add) > 0:
        print(f"Running with the following temporary environment variables: {environ_vars_to_add}")

    with set_env(**environ_vars_to_add):
        main()

