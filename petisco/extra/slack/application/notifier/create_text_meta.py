from typing import Any, Dict, Union


def create_text_meta(meta: Dict[str, Any]) -> Union[str, None]:
    text = None
    if meta:
        text = ""
        for key, value in meta.items():
            text += f"\n>{key}: `{value}`"
    return text
