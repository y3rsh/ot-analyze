from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import subprocess
import time


def analyze(directory: Path):
    start_time = time.time()  # Start timing
    analysis_file = os.path.join(directory, "analysis.json")

    python_files = [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.endswith(".py")
    ]
    if not python_files:
        print(f"No python file in directory {directory}. Skipping...")
        return

    python_file = python_files[0]  # Assuming there's only one .py file per directory
    custom_labware_directory = os.path.join(directory, "custom_labware")

    custom_labware = []
    if os.path.isdir(custom_labware_directory):
        custom_labware = [
            os.path.join(custom_labware_directory, file)
            for file in os.listdir(custom_labware_directory)
            if file.endswith(".json")
        ]

    command = [
        "python",
        "-m",
        "opentrons.cli",
        "analyze",
        "--json-output",
        analysis_file,
        python_file,
    ] + custom_labware
    try:
        subprocess.run(command, check=True)
        # After running the command, read the analysis.json file to check for errors
        if os.path.exists(analysis_file):
            with open(analysis_file, "r") as f:
                data = json.load(f)
                if data.get("errors"):  # If the 'errors' key is not empty
                    print(f"Errors found in directory: {directory}")
    except subprocess.CalledProcessError as e:
        print(f"Command '{' '.join(command)}' failed with error: {str(e)}")

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
