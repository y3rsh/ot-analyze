from pathlib import Path
from typing import List

POSITIVE_OT2: Path = Path(Path(__file__).parent, "positive_ot2_no_labware")
POSITIVE_FLEX: Path = Path(Path(__file__).parent, "positive_flex_no_labware")
ERROR: Path = Path(Path(__file__).parent, "error")
NO_CI: Path = Path(Path(__file__).parent, "no_ci")
NO_PROTOCOL: Path = Path(Path(__file__).parent, "no_protocol")

# Creating an array of these paths
ALL: List[Path] = [POSITIVE_OT2, POSITIVE_FLEX, ERROR, NO_CI, NO_PROTOCOL]
