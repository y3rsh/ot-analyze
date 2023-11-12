import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def simulate(directory: Path):
    start_time = time.time()  # Start timing

    python_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".py")]
    if not python_files:
        print(f"No python file in directory {directory}. Skipping...")
        return

    python_file = python_files[0]  # Assuming there's only one .py file per directory
    custom_labware_directory = Path(directory, "custom_labware")

    custom_labware = []
    if custom_labware_directory.exists() and custom_labware_directory.is_dir():
        json_files = [file for file in custom_labware_directory.iterdir() if file.suffix == ".json"]
        if json_files:
            custom_labware = [
                "-L",
                custom_labware_directory.resolve(),
            ]
        else:
            print(f"No .json files in {custom_labware_directory}.")
    if custom_labware == []:
        command = [
            "opentrons_simulate",
            python_file,
        ]
    else:
        command = [
            "opentrons_simulate",
            python_file,
        ] + custom_labware
    print(f"Running command: {command}")
    subprocess.run(command, check=True)
    end_time = time.time()  # End timing
    print(f"Simulate of {directory} completed in {end_time - start_time:.2f} seconds")


def run_simulate_in_parallel(directories):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(simulate, Path(dir)) for dir in directories]

        for future in as_completed(futures):
            try:
                future.result()  # This blocks until the future is done
            except Exception as e:
                print(f"An error occurred: {e}")
