from app.core.common.schema import CommonInput

def generate_hashtag_prompt(common_prompt: str, input_obj: CommonInput, target_audience:str, platform_rule:str) -> str:
    return f"""
너는 카페 사장님의 카페 홍보를 위한 해시태그 관리 전문가야.

[콘텐츠 목적]
- 플랫폼: {input_obj.platform}
- 시청자 타겟: {target_audience}
- 플랫폼 룰 : {platform_rule}

다음은 콘텐츠 제작을 위한 기본 정보야:

{common_prompt}

이 정보를 바탕으로 이 릴스/쇼츠 콘텐츠에 어울리는 **해시태그 5~10개**를 생성해줘.

[작성 조건]
- 해시태그는 모두 **#**으로 시작
- 띄어쓰기 없이 작성
- 중복 없이 작성
- 너무 일반적인 태그는 피하고 메뉴/카페 특화 태그 포함
- 대분류3개, 중분류 3개, 소분류 4개 정도로 다양하게 구성

❗중요:
- 해시태그는 반드시 **리스트 형태(JSON 배열)** 로 반환해야 해
- 다른 설명 없이 JSON만 출력해

응답 형식 예시:

{{
  "hashtags": [
    "#말차라떼",
    "#감성카페",
    "#카페브랜딩",
    "#카페마케팅",
    "#릴스마케팅"
  ]
}}
"""
