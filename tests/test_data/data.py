from pathlib import Path
from typing import List

POSITIVE_OT2: Path = Path(Path(__file__).parent, "positive_ot2_no_labware", "protocol.py")
POSITIVE_FLEX: Path = Path(Path(__file__).parent, "positive_flex_no_labware", "protocol.py")
ERROR: Path = Path(Path(__file__).parent, "error", "protocol.py")
NO_CI: Path = Path(Path(__file__).parent, "no_ci")
NO_PROTOCOL: Path = Path(Path(__file__).parent, "no_protocol")
FLEX_ERROR: Path = Path(Path(__file__).parent, "flex_error", "protocol.py")
# Creating an array of these paths
ALL: List[Path] = [POSITIVE_OT2, POSITIVE_FLEX, ERROR, NO_CI, NO_PROTOCOL, FLEX_ERROR]
