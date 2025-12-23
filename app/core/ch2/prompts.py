from core.common.schema import CommonInput


def build_video_prompt(input_obj: CommonInput) -> str:
    return f"""
너는 카페/로컬브랜드 숏폼 영상 기획자다.

[입력(CommonInput)]
- 카페명: {input_obj.cafe_name}
- 주제/제품: {input_obj.menu_name}
- 설명: {input_obj.menu_desc}
- 플랫폼: {input_obj.platform}
- 영상 길이: {input_obj.video_length}
- 스타일: {input_obj.style}

[출력 규칙]
- 반드시 JSON만 출력한다.
- 형식:
{{
  "title": "제목 한 줄",
  "script": "전체 스크립트(줄바꿈 허용)",
  "hashtags": ["#태그1", "#태그2", "#태그3", "#태그4", "#태그5"]
}}

[스크립트 규칙]
- 한국어
- 초반 1~2문장에 훅(시선 붙잡기)
- 길이에 맞게 과하지 않게
- 마지막에 CTA 포함(예: '저장해두기', '댓글로 질문!')
"""
