import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List

from src.write_failed_analysis import write_failed_analysis


def analyze(directory: Path):
    start_time = time.time()  # Start timing
    analysis_file = os.path.join(directory, "analysis.json")

    python_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".py")]
    if not python_files:
        print(f"No python file in directory {directory}. Skipping...")
        return

    python_file = python_files[0]  # Assuming there's only one .py file per directory
    custom_labware_directory = os.path.join(directory, "custom_labware")

    custom_labware = []
    if os.path.isdir(custom_labware_directory):
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
        analysis_file,
        python_file,
    ] + custom_labware
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running analysis: {e}")
        write_failed_analysis(analysis_file, str(e))
        return
    end_time = time.time()  # End timing
    print(f"Analysis of {directory} completed in {end_time - start_time:.2f} seconds")


def run_analyze_in_parallel(directories):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(analyze, Path(dir)) for dir in directories]

        for future in as_completed(futures):
            try:
                future.result()  # This blocks until the future is done
            except Exception as e:
                print(f"An error occurred: {e}")


def find_python_files(path_like: str) -> List[Path]:
    """
    Takes a path-like string and returns a list of all .py files found
    recursively in the given directory.

    :param path_like: A path-like string.
    :return: A list of Paths to the found .py files.
    """
    directory = Path(path_like)

    # Check if the provided path is a valid directory
    if not directory.is_dir():
        raise NotADirectoryError(f"The path {directory} is not a valid directory.")

    # Recursively find all .py files
    python_files = list(directory.rglob("*.py"))

    return python_files


if __name__ == "__main__":
    directories = find_python_files(".")
    run_analyze_in_parallel(directories)
