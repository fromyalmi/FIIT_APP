from core.common.schema import CommonInput


def build_ads_prompt(input_obj: CommonInput) -> str:
    """
    ✅ 입력 스키마(CommonInput) 기반으로 CH1 프롬프트 생성
    """
    return f"""
너는 카페 마케팅 카피라이터다.

[입력(CommonInput)]
- 카페명: {input_obj.cafe_name}
- 제품/서비스: {input_obj.product}
- 메뉴/주제: {input_obj.menu_name}
- 설명: {input_obj.menu_desc}
- 톤/스타일: {input_obj.tone}
- 개수(n): {input_obj.n}

[출력 규칙]
- 반드시 JSON만 출력한다. (설명/서문 금지)
- 형식:
{{
  "items": ["문구1", "문구2", ...]
}}

[카피 규칙]
- 한국어
- 1줄 문구(너무 길게 쓰지 말기)
- 이모지 0~2개 허용
- 마지막에 강한 CTA(예: '지금 주문!', '오늘 한 잔?') 포함
"""
