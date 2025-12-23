from typing import Dict, Any, List

from core.common.llm import chat_json
from core.common.storage import save_json
from core.common.result import build_envelope
from core.common.schema import CommonInput
from .prompts import build_video_prompt


def generate_video_script(input_obj: CommonInput, mock: bool = False) -> Dict[str, Any]:
    prompt = build_video_prompt(input_obj)

    mock_payload = {
        "title": f"{input_obj.menu_name} 한 번에 정리!",
        "script": (
            f"안녕하세요! 오늘은 {input_obj.video_length} 안에 끝내는 추천템 소개💡\n"
            f"{input_obj.menu_name} 포인트 3가지만 보여드릴게요.\n"
            "1) 향\n2) 식감\n3) 마무리\n"
            "저장해두고 다음에 꼭 써먹어봐요 🙂"
        ),
        "hashtags": ["#카페", "#쇼츠", "#릴스", "#추천", "#힐링타임"],
    }

    data = chat_json(prompt, mock=mock, mock_payload=mock_payload)

    title = data.get("title", "") if isinstance(data, dict) else ""
    script = data.get("script", "") if isinstance(data, dict) else ""
    hashtags: List[str] = data.get("hashtags", []) if isinstance(data, dict) else []
    if not isinstance(hashtags, list):
        hashtags = []

    output_obj = {"title": title, "script": script, "hashtags": hashtags}
    envelope = build_envelope("ch2_video", input_obj=input_obj, output_obj=output_obj, mock=mock)

    saved_path = save_json(envelope, filename_prefix="video_result")
    return {"title": title, "script": script, "hashtags": hashtags, "saved_path": saved_path}
