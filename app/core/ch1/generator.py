from typing import Dict, Any, List

from core.common.llm import chat_json
from core.common.storage import save_json
from core.common.result import build_envelope
from core.common.schema import CommonInput
from .prompts import build_ads_prompt


def generate_ads(input_obj: CommonInput, mock: bool = False) -> Dict[str, Any]:
    prompt = build_ads_prompt(input_obj)

    mock_payload = {
        "items": [
            f"🍰 오후에 처지는 순간, {input_obj.menu_name} 한 잔으로 리셋! 지금 바로!",
            f"☕ 커피 말고 {input_obj.menu_name}? 고소한 초록 한 모금, 오늘도 가볍게!",
            f"✨ {input_obj.menu_desc[:30]}... {input_obj.menu_name}로 오후 분위기 업! 지금 주문!",
            f"🌿 달달·고소·깔끔 끝판왕: {input_obj.menu_name}. 오늘 한 잔?",
            f"😌 점심 후 멍~할 때, {input_obj.menu_name}로 기분 전환! 지금 바로!",
        ][: max(1, int(input_obj.n or 1))]
    }

    data = chat_json(prompt, mock=mock, mock_payload=mock_payload)

    items: List[str] = data.get("items") if isinstance(data, dict) else None
    if not isinstance(items, list):
        items = ["(생성 실패) 다시 시도해 주세요."]

    output_obj = {"items": items}
    envelope = build_envelope("ch1_ads", input_obj=input_obj, output_obj=output_obj, mock=mock)

    saved_path = save_json(envelope, filename_prefix="ads_result")
    return {"items": items, "saved_path": saved_path}
