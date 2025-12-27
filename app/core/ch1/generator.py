# core/ch1/generator.py

import base64
import io
import streamlit as st
from typing import Dict, Any, List

from openai import OpenAI
from core.common.llm import chat_json
from core.common.storage import save_json
from core.common.bootstrap import kst_now
from core.ch1.prompts import build_ads_prompt

client = OpenAI()

# ---------------------------------------------------------
# 🔹 이미지 분석 기능
# ---------------------------------------------------------
def analyze_image(image_file):
    img_data = base64.b64encode(image_file.read()).decode()
    prompt = (
        "당신은 광고 이미지 분석 전문가입니다. "
        "이 이미지에서 느껴지는 분위기·색감·재질·감정 키워드를 1~2문장으로 감각적으로 요약하세요."
    )
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{img_data}"}
                    }
                ]
            }
        ]
    )
    summary = res.choices[0].message.content.strip()
    image_file.seek(0)
    return summary

# ---------------------------------------------------------
# 🔹 광고 문구 생성
# ---------------------------------------------------------
def generate_ads(
    purpose: str,
    product: str,
    menu_name: str,
    menu_desc: str,
    tone: str,
    platform: str,
    image_summary: str,
    n: int,
    mock: bool = False,
) -> Dict[str, Any]:

    prompt = build_ads_prompt(
        product=product,
        menu_name=menu_name,
        menu_desc=menu_desc,
        tone=tone,
        purpose=purpose,
        platform=platform,
        image_summary=image_summary,
        n=n,
    )

    # mock 모드
    mock_payload = {
        "items": [
            f"{menu_name} · {purpose} · {platform} 스타일 광고",
            f"이미지 특징 기반: {image_summary[:20]}...",
        ][:n]
    }

    data = chat_json(prompt, mock=mock, mock_payload=mock_payload)

    if isinstance(data, dict) and isinstance(data.get("items"), list):
        items = data["items"]
    else:
        items = ["광고 문구 생성에 실패했습니다. 다시 시도해주세요."]

    payload = {
        "meta": {
            "chapter": "ch1_ads",
            "created_at_kst": kst_now().strftime("%Y-%m-%d_%H:%M:%S (KST)"),
            "mock": mock,
            "platform": platform,
        },
        "input": {
            "purpose": purpose,
            "product": product,
            "menu_name": menu_name,
            "menu_desc": menu_desc,
            "tone": tone,
            "platform": platform,
            "image_summary": image_summary,
            "n": n,
        },
        "output": {"items": items},
    }

    saved_path = save_json(payload, filename_prefix="ads_result")
    return {"items": items, "saved_path": saved_path}


# ---------------------------------------------------------
# 🔹 TTS 기능
# ---------------------------------------------------------
def make_tts(text, voice="alloy"):
    import re
    if isinstance(text, dict):
        text = " ".join([v for v in text.values() if isinstance(v, str)])
    elif isinstance(text, list):
        text = " ".join([str(v) for v in text])
    text = str(text)

    text = re.sub(r'인트로[:：]?', '', text)
    text = re.sub(r'본문[:：]?', '', text)
    text = re.sub(r'아웃트로[:：]?', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    if len(text) > 700:
        text = text[:700] + "..."

    audio = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text
    )

    buf = io.BytesIO(audio.read())
    buf.name = "ad_voice.mp3"
    return buf
