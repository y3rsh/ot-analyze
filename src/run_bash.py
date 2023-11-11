import subprocess
from pathlib import Path

from src.build_info import BuildInfo

script_path = Path(Path(__file__).parent, "release-type.sh")


def run_bash_script(event_type, ref):
    try:
        result = subprocess.run(
            [script_path.resolve(), event_type, ref],
            capture_output=True,
            text=True,
            check=True,
        )
        return parse_bash_output(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running bash script: {e}")
        return None


def parse_bash_output(output) -> BuildInfo:
    parsed_output = {"variants": [], "build_type": "develop"}
    for line in output.splitlines():
        key, value = line.split("=", 1)
        if key == "variants":
            # Parse variants list
            parsed_output["variants"] = eval(value)
        elif key == "type":
            # Parse build type
            parsed_output["build_type"] = value

    return BuildInfo(variants=parsed_output["variants"], build_type=parsed_output["build_type"])
