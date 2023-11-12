import pytest
from build_info import BuildInfo, determine_build_type
from run_bash import run_bash_script

test_cases = [
    ("pull_request", "any_ref", BuildInfo(variants=[], build_type="develop")),
    (
        "any_event",
        "refs/tags/ot3any",
        BuildInfo(variants=["internal-release"], build_type="release"),
    ),
    (
        "any_event",
        "refs/tags/v1.0",
        BuildInfo(variants=["release"], build_type="release"),
    ),
    (
        "any_event",
        "refs/heads/internal-release-feature",
        BuildInfo(variants=["internal-release"], build_type="develop"),
    ),
    (
        "any_event",
        "refs/heads/release-v1",
        BuildInfo(variants=["release"], build_type="develop"),
    ),
    (
        "any_event",
        "refs/heads/chore_release-update",
        BuildInfo(variants=["release"], build_type="develop"),
    ),
    (
        "any_event",
        "refs/heads/edge",
        BuildInfo(variants=["release", "internal-release"], build_type="develop"),
    ),
    (
        "any_event",
        "feature/app-build-internal",
        BuildInfo(variants=["internal-release"], build_type="develop"),
    ),
    (
        "any_event",
        "feature/app-build",
        BuildInfo(variants=["release"], build_type="develop"),
    ),
    (
        "any_event",
        "feature/app-build-both",
        BuildInfo(variants=["release", "internal-release"], build_type="develop"),
    ),
    # Default case
    (
        "any_event",
        "refs/heads/any_other_branch",
        BuildInfo(variants=[], build_type="develop"),
    ),
]


@pytest.mark.parametrize("event_type, ref, expected", test_cases)
def test_build_check(event_type, ref, expected):
    # Run the Python checker
    python_result = determine_build_type(event_type, ref)
    assert python_result == expected, "Python checker returned unexpected result"

    # Run the bash script and parse its output
    bash_result = run_bash_script(event_type, ref)
    assert bash_result == expected, "Bash script returned unexpected result"
