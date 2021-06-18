from typing import Dict


def raise_petisco_config_exception(kdict: Dict, field_name=None):
    if field_name:
        field_name = f" ({field_name})"
    else:
        field_name = ""
    raise TypeError(
        f"Petisco Config Error: Given input{field_name} is not valid. Please check it {kdict}"
    )
