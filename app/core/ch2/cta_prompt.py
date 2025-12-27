from app.core.common.schema import CommonInput

def generate_cta_prompt(common_prompt: str, input_obj: CommonInput, target_audience:str, platform_rule:str) -> str:
    return f"""
너는 카페 사장님을 위한 홍보 전문 CTA 문구작가야.

[콘텐츠 목적]
- 플랫폼: {input_obj.platform}
- 시청자 타겟: {target_audience}
- 콘텐츠 톤: {input_obj.tone}
- 플랫폼 룰 : {platform_rule}


다음은 콘텐츠 제작을 위한 기본 정보야:

{common_prompt}

위 내용을 바탕으로 **시청자의 행동을 유도하는 CTA(Call To Action) 문장 5개**를 작성해줘.

[작성 조건]
- 각 문장은 짧고 명확하게 (1문장)
- 톤은 {input_obj.tone}, 플랫폼은 {input_obj.platform}
[가이드]
- Instagram Reels:
  - 가볍고 자연스러운 말투
  - 리듬감 있는 문장, 친근한 표현 허용
  - 말하듯 자연스러운 구어체
  - 반말 또는 부드러운 존댓말 혼용 가능
  - 문장 끝을 완전히 맺지 않아도 됨
  - 감탄사, 여백, 여운 허용
  - 감정과 분위기를 최우선
  - 문장 짧게, 여백 있는 리듬
  - 공감/느낌 위주 표현  


- YouTube Shorts:
  - 짧고 명확한 정보 전달
  - 핵심 행동 위주의 담백한 문장
  - 존댓말만 사용
  - 문장 끝을 분명히 마무리
  - 누가 봐도 이해되는 표현
  - 정보 전달과 이해를 최우선
  - 설명형 문장, 명확한 구조
  - 이유 → 결과 → 요약 흐름
  - 불필요한 감성 표현 최소화
- 행동을 유도하는 동사를 반드시 포함
- 중복 표현 없이 다르게

👉 아래와 같은 형식으로, 문장만 5개 작성해줘 (번호/기호/따옴표 없이):

문장 1
문장 2
문장 3
문장 4
문장 5

응답은 반드시 다음과 같은 JSON 형식으로 작성해주세요. 다른 설명 없이 JSON만 출력해주세요.

{{
  "ctas": [
    "행동을 유도하는 문구1",
    "행동을 유도하는 문구2",
    "행동을 유도하는 문구3"
  ]
}}
"""
