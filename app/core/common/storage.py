import json
import os
from typing import Any, Dict

from .bootstrap import kst_stamp_compact


def ensure_outputs_dir(outputs_dir: str = "outputs") -> str:
    os.makedirs(outputs_dir, exist_ok=True)
    return outputs_dir


def save_json(payload: Dict[str, Any], filename_prefix: str, outputs_dir: str = "outputs") -> str:
    """
    payload를 outputs_dir에 JSON으로 저장하고 경로를 반환합니다.
    파일명 예) ads_result_YYYYMMDD_HHMM.json
    """
    outputs_dir = ensure_outputs_dir(outputs_dir)
    stamp = kst_stamp_compact()
    filename = f"{filename_prefix}_{stamp}.json"
    path = os.path.join(outputs_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return path
