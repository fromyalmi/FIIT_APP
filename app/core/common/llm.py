import os
import json
from typing import Any, Dict, Optional

from dotenv import load_dotenv

# openai >= 1.x
try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None

load_dotenv()


def _get_client() -> "OpenAI":
    if OpenAI is None:
        raise RuntimeError("openai 패키지를 불러오지 못했습니다. requirements 설치를 확인하세요.")
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY가 비어있습니다. .env 설정을 확인하세요.")
    return OpenAI(api_key=api_key)


def chat_json(prompt: str, mock: bool = False, mock_payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    - mock=True: mock_payload를 그대로 반환
    - mock=False: OpenAI 호출 → JSON 파싱 후 dict 반환
    """
    if mock:
        return mock_payload or {}

    client = _get_client()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Always return valid JSON only. No extra text."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    text = resp.choices[0].message.content.strip()

    # 1차 파싱
    try:
        return json.loads(text)
    except Exception:
        # 2차: 코드블럭 제거 후 재시도
        cleaned = text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)
