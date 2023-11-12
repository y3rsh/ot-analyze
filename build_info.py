from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Literal, Optional

Variant = Literal["internal-release", "release"]
BuildType = Literal["develop", "release"]


@dataclass(frozen=True)
class BuildInfo:
    variants: List[Variant]
    build_type: BuildType


# Set of all valid BuildInfo objects based on the Bash script
valid_build_infos = [
    BuildInfo(variants=[], build_type="develop"),
    BuildInfo(variants=["internal-release"], build_type="release"),
    BuildInfo(variants=["release"], build_type="release"),
    BuildInfo(variants=["internal-release"], build_type="develop"),
    BuildInfo(variants=["release"], build_type="develop"),
    BuildInfo(variants=["release", "internal-release"], build_type="develop"),
]


# Interface for build checks
class BuildCheck(ABC):
    @abstractmethod
    def check(self, github_event_type: str, github_ref: str) -> Optional[BuildInfo]:
        pass


# Specific check implementations
class PullRequestCheck(BuildCheck):
    def check(self, github_event_type: str, github_ref: str) -> Optional[BuildInfo]:
        if github_event_type == "pull_request":
            return BuildInfo(variants=[], build_type="develop")


class OT3TagCheck(BuildCheck):
    def check(self, github_event_type: str, github_ref: str) -> Optional[BuildInfo]:
        if github_ref.startswith("refs/tags/ot3"):
            return BuildInfo(variants=["internal-release"], build_type="release")


class VTagCheck(BuildCheck):
    def check(self, github_event_type: str, github_ref: str) -> Optional[BuildInfo]:
        if github_ref.startswith("refs/tags/v"):
            return BuildInfo(variants=["release"], build_type="release")


class InternalReleaseBranchCheck(BuildCheck):
    def check(self, github_event_type: str, github_ref: str) -> Optional[BuildInfo]:
        if github_ref.startswith("refs/heads/internal-release"):
            return BuildInfo(variants=["internal-release"], build_type="develop")


class ReleaseBranchCheck(BuildCheck):
    def check(self, github_event_type: str, github_ref: str) -> Optional[BuildInfo]:
        if github_ref.startswith("refs/heads/release") or github_ref.startswith("refs/heads/chore_release"):
            return BuildInfo(variants=["release"], build_type="develop")


class EdgeBranchCheck(BuildCheck):
    def check(self, github_event_type: str, github_ref: str) -> Optional[BuildInfo]:
        if github_ref == "refs/heads/edge":
            return BuildInfo(variants=["release", "internal-release"], build_type="develop")


class AppBuildInternalSuffixCheck(BuildCheck):
    def check(self, github_event_type: str, github_ref: str) -> Optional[BuildInfo]:
        if github_ref.endswith("app-build-internal"):
            return BuildInfo(variants=["internal-release"], build_type="develop")


class AppBuildSuffixCheck(BuildCheck):
    def check(self, github_event_type: str, github_ref: str) -> Optional[BuildInfo]:
        if github_ref.endswith("app-build"):
            return BuildInfo(variants=["release"], build_type="develop")


class AppBuildBothSuffixCheck(BuildCheck):
    def check(self, github_event_type: str, github_ref: str) -> Optional[BuildInfo]:
        if github_ref.endswith("app-build-both"):
            return BuildInfo(variants=["release", "internal-release"], build_type="develop")


# Function to process build type checks
def determine_build_type(github_event_type: str, github_ref: str) -> BuildInfo:
    checks = [
        PullRequestCheck(),
        OT3TagCheck(),
        VTagCheck(),
        InternalReleaseBranchCheck(),
        ReleaseBranchCheck(),
        EdgeBranchCheck(),
        AppBuildInternalSuffixCheck(),
        AppBuildSuffixCheck(),
        AppBuildBothSuffixCheck(),
    ]

    for check in checks:
        result = check.check(github_event_type, github_ref)
        if result is not None:
            if result in valid_build_infos:
                return result
            else:
                raise ValueError(f"Invalid BuildInfo combination: {result}")

    # Default case if no other checks match
    return BuildInfo(variants=[], build_type="develop")
