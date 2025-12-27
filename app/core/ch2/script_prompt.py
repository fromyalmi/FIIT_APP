from app.core.common.schema import CommonInput

def generate_script_prompt(common_prompt: str, input_obj: CommonInput, target_audience:str, platform_rule: str,seconds: int) -> str:
    return f"""
너는 카페 사장님을 위한 숏폼 영상 스크립트 작가야.
[⚠️ 가장 중요한 규칙 ⚠️]
아래 플랫폼 말투 규칙을 **반드시 100% 준수해서 작성해.
다른 말투는 절대 사용하지 마.**

[플랫폼 말투 규칙]
{platform_rule}

[콘텐츠 정보]
- 플랫폼: {input_obj.platform}
- 시청자 타겟: {target_audience}
- 영상 길이: 약 {seconds}초


이 정보를 바탕으로 릴스/쇼츠 영상에 적합한 **영상 스크립트**를 작성해줘.

[기본 정보]
{common_prompt}

[작성 규칙 – 영상 길이]
- {seconds}초 분량에 맞게 문장 수 조절
- {seconds}가 15초일 경우 6~7문장
- {seconds}가 30초일 경우 10~12문장
- {seconds}가 60초일 경우 18~20문장
- 불필요한 문장 금지


[절대 금지]
- 다른 플랫폼 말투 섞기
- 반말/존댓말 혼용
- 규칙에 없는 표현 사용

- 문장마다 줄바꿈 해줘

다음은 콘텐츠 제작을 위한 기본 정보 :
👉 최종 스크립트만 반환. 마크다운, 설명 없이.

응답은 반드시 다음과 같은 JSON 형식으로 작성해주세요. 다른 설명 없이 JSON만 출력해주세요.

{{
  "script": "이 영상에 대한 스크립트"
}}
"""


