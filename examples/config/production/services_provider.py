from typing import Dict, Any

from petisco.application.dot_dict import DotDict


class Petisco:
    pass


def services_provider() -> Dict[str, Any]:
    return DotDict({"petisco": Petisco()})
