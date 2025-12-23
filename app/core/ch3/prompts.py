from core.common.schema import CommonInput


def build_sns_prompt(input_obj: CommonInput) -> str:
    return f"""
너는 카페 SNS 운영자다.

[입력(CommonInput)]
- 카페명: {input_obj.cafe_name}
- 메뉴/주제: {input_obj.menu_name}
- 설명: {input_obj.menu_desc}
- 플랫폼: {input_obj.platform}
- 분위기: {input_obj.vibe}

[출력 규칙]
- 반드시 JSON만 출력한다.
- 형식:
{{
  "caption": "본문(줄바꿈 허용)",
  "hashtags": ["#태그1", "#태그2", "#태그3", "#태그4", "#태그5", "#태그6"]
}}

[작성 규칙]
- 한국어
- 너무 광고 티만 나지 않게: 공감/상황/감각 표현 포함
- 마지막에 CTA(저장/방문/문의/DM 등) 포함
"""
