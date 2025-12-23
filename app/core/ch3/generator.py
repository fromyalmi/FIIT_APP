from typing import Dict, Any, List

from core.common.llm import chat_json
from core.common.storage import save_json
from core.common.result import build_envelope
from core.common.schema import CommonInput
from .prompts import build_sns_prompt


def generate_sns_post(input_obj: CommonInput, mock: bool = False) -> Dict[str, Any]:
    prompt = build_sns_prompt(input_obj)

    mock_payload = {
        "caption": (
            f"{input_obj.cafe_name} 오늘의 추천 ☕\n"
            f"'{input_obj.menu_name}' 한 잔(또는 한 메뉴)으로 오후 리셋!\n"
            f"{input_obj.menu_desc}\n\n"
            "저장해두고, 다음에 오실 때 메뉴 고르기 쉬워지게 🙂\n"
            "DM으로 단체 주문/예약 문의도 가능해요!"
        ),
        "hashtags": ["#cremastudio", "#카페추천", "#오늘의메뉴", "#디저트카페", "#저장각", "#방문추천"],
    }

    data = chat_json(prompt, mock=mock, mock_payload=mock_payload)

    caption = data.get("caption", "") if isinstance(data, dict) else ""
    hashtags: List[str] = data.get("hashtags", []) if isinstance(data, dict) else []
    if not isinstance(hashtags, list):
        hashtags = []

    output_obj = {"caption": caption, "hashtags": hashtags}
    envelope = build_envelope("ch3_sns", input_obj=input_obj, output_obj=output_obj, mock=mock)

    saved_path = save_json(envelope, filename_prefix="sns_result")
    return {"caption": caption, "hashtags": hashtags, "saved_path": saved_path}
