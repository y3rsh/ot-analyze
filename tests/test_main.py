import os
from pathlib import Path

import ot_analyze


def test_run_script_in_integration(capsys, clear_analysis_files):
    # Set up the environment variables as expected by the script
    os.environ["GITHUB_WORKSPACE"] = "./"  # Current directory
    os.environ["INPUT_BASE_DIRECTORY"] = "tests/test_data/many"  # Subdirectory with test files

    # Path setup as per your script's logic
    expected_path = Path(os.environ["GITHUB_WORKSPACE"], os.environ["INPUT_BASE_DIRECTORY"])

    # Ensure the directory exists and has the expected number of files
    assert expected_path.is_dir(), "Test directory does not exist"
    protocol_files = list(expected_path.glob("*.py"))
    assert len(protocol_files) == 3, "Test directory does not contain 3 .py files"

    # Call the main function of the script
    ot_analyze.main()
