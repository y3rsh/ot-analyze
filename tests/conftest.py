from pathlib import Path

import pytest


def delete_analysis_files():
    analysis_files = list(Path("test_data").rglob("**/*analysis.json"))
    for analysis in analysis_files:
        if analysis.exists():
            try:
                analysis.unlink()  # Deletes the file
                print(f"Deleted {analysis.resolve()}")
            except Exception as e:
                print(f"Error deleting {analysis.resolve()}: {e}")


@pytest.fixture(scope="session", autouse=True)
def clear_analysis_files():
    delete_analysis_files()
