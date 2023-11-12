import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def create_failed_analysis(error_message: str) -> Dict[str, Any]:
    created_at = datetime.utcnow().isoformat()

    return {
        "createdAt": created_at,
        "errors": [
            {
                "id": str(uuid.uuid4()),
                "errorType": "UnexpectedAnalysisError",
                "detail": error_message,
                "createdAt": created_at,
            }
        ],
        "files": [],
        "metadata": [],
        "commands": [],
        "labware": [],
        "pipettes": [],
        "modules": [],
        "liquids": [],
        "config": {},
    }


def write_failed_analysis(output_path: Path, error_message: str) -> None:
    if output_path.exists():
        print(f"Analysis file {output_path} already exists, skipping placeholder file.")
        return
    analysis = create_failed_analysis(error_message)
    with open(output_path, "w") as file:
        json.dump(analysis, file, indent=4)
