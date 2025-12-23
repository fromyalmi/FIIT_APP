from typing import Any, Dict, Literal
from .bootstrap import kst_now
from .schema import CommonInput, Meta


def build_envelope(
    chapter: Literal["ch1_ads", "ch2_video", "ch3_sns"],
    input_obj: CommonInput,
    output_obj: Dict[str, Any],
    mock: bool,
) -> Dict[str, Any]:
    """
    ✅ 저장 JSON의 공통 뼈대(meta/input/output)를 생성
    """
    meta = Meta(
        chapter=chapter,
        created_at_kst=kst_now().strftime("%Y-%m-%d_%H:%M:%S (KST)"),
        mock=mock,
    )
    return {
        "meta": meta.model_dump(),
        "input": input_obj.model_dump(),
        "output": output_obj,
    }
