from app.core.common.schema import CommonInput

def generate_description_prompt(common_prompt: str, input_obj: CommonInput, target_audience:str, platform_rule:str) -> str:
    return f"""
너는 카페 사장님의 마케팅을 돕는 숏폼 영상 콘텐츠 전문가야.

[콘텐츠 목적]
- 플랫폼: {input_obj.platform}
- 시청자 타겟: {target_audience}
- 플랫폼 룰 : {platform_rule}

다음은 콘텐츠 제작을 위한 기본 정보야:

{common_prompt}

이 정보를 바탕으로 **Instagram Reels 또는 YouTube Shorts**에 함께 올릴 **영상 설명글(캡션)**을 작성해줘.

[작성 조건]
- 플랫폼: {input_obj.platform}
- 문장마다 줄바꿈
- 영상 길이: {input_obj.video_length}
   영상 길이에 맞게 간견하고 핵심적인 설명으로 작성
    
- 스타일 톤: {input_obj.tone}
  [플랫폼 말투 가이드]
  - Instagram Reels:
    · 가볍고 자연스러운 말투
    · 리듬감 있는 문장, 친근한 표현 허용
    - 말하듯 자연스러운 구어체
    - 반말 또는 부드러운 존댓말 혼용 가능
    - 문장 끝을 완전히 맺지 않아도 됨
    - 감탄사, 여백, 여운 허용
    - 감정과 분위기를 최우선
    - 문장 짧게, 여백 있는 리듬
    - 공감/느낌 위주 표현  


  - YouTube Shorts:
    · 짧고 명확한 정보 전달
    · 핵심 행동 위주의 담백한 문장
    - 존댓말만 사용
    - 문장 끝을 분명히 마무리
    - 누가 봐도 이해되는 표현
    - 정보 전달과 이해를 최우선
    - 설명형 문장, 명확한 구조
    - 이유 → 결과 → 요약 흐름
    - 불필요한 감성 표현 최소화
- 문장마다 줄바꿈 해줘

👉 설명글 본문만 응답해줘. 마크다운이나 설명 없이 문장만.

응답은 반드시 다음과 같은 JSON 형식으로 작성해주세요. 다른 설명 없이 JSON만 출력해주세요.

{{
  "description": "이 영상에 대한 짧은 설명 한 문장"
}}
"""
