from typing import Dict, List


def create_text_meta(meta: Dict) -> List[Dict]:
    text = None
    if meta:
        text = ""
        for key, value in meta.items():
            text += f"\n>{key}: {value}"
    return text
