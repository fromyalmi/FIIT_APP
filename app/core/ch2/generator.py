from app.core.common.schema import CommonInput
from app.core.common.llm import chat_json

def normalize_platform(platform: str) -> str:
    if "Instagram" in platform:
        return "INSTAGRAM_REELS"
    if "YouTube" in platform:
        return "YOUTUBE_SHORTS"
    return "UNKNOWN"

def parse_seconds(video_length: str) -> int:
    try:
        return int(video_length.replace("초", "").strip())
    except Exception:
        return 3
    

from app.core.ch2.common_prompt import build_common_prompt
from app.core.ch2.hook_prompt import generate_hook_prompt
from app.core.ch2.script_prompt import generate_script_prompt
from app.core.ch2.description_prompt import generate_description_prompt
from app.core.ch2.cta_prompt import generate_cta_prompt
from app.core.ch2.hashtag_prompt import generate_hashtag_prompt
from app.core.ch2.viewer_prompt import generate_viewer_prompt

# ✅ 최초 생성 (사이드바 "생성" 버튼)
def generate_video_script(input_obj: CommonInput, mock: bool = False) -> dict:
    common_prompt = build_common_prompt(input_obj)
    
    if mock:
        return {
            "hooks": ["훅1", "훅2", "훅3", "훅4", "훅5"],
            "description": "영상 설명",
            "script": "본문 스크립트",
            "ctas": ["CTA1", "CTA2", "CTA3", "CTA4", "CTA5"],
            "hashtags": ["tag1","tag2","tag3","tag4","tag5","tag6","tag7","tag8","tag9","tag10"],
        }
    platform_key = normalize_platform(input_obj.platform)
    seconds = parse_seconds(input_obj.video_length)

    if platform_key == "INSTAGRAM_REELS":
        platform_rule = """
    · 가볍고 자연스러운 말투
    · 리듬감 있는 문장, 친근한 표현 허용
    - 말하듯 자연스러운 구어체
    - 반말 또는 부드러운 존댓말 혼용 가능
    - 문장 끝을 완전히 맺지 않아도 됨
    - 감탄사, 여백, 여운 허용
    - 감정과 분위기를 최우선
    - 문장 짧게, 여백 있는 리듬
    - 공감/느낌 위주 표현  
    - youtube_shorts와 차별화된 톤 유지
    """
    elif platform_key == "YOUTUBE_SHORTS":
        platform_rule = """
  · 짧고 명확한 정보 전달
  · 핵심 행동 위주의 담백한 문장
  - 존댓말만 사용
  - 문장 끝을 분명히 마무리
  - 누가 봐도 이해되는 표현
  - 정보 전달과 이해를 최우선
  - 설명형 문장, 명확한 구조
  - 이유 → 결과 → 요약 흐름
  - 불필요한 감성 표현 최소화
  - instagram_reels와 차별화된 톤 유지
    """
    else:
        platform_rule = "플랫폼별 말투 규칙을 사용합니다."

    # 시청자 타겟 추천용 프롬프트 추가
    viewer_prompt = generate_viewer_prompt(input_obj.platform)
    viewer_res = chat_json(viewer_prompt, mock=mock)
    target_audience = viewer_res.get("target", "전연령")


    hook_res = chat_json(
        generate_hook_prompt(common_prompt, input_obj, target_audience, platform_rule),
        mock=mock
    )

    script_res = chat_json(
        generate_script_prompt(common_prompt, input_obj, target_audience, platform_rule, seconds),
        mock=mock
    )

    desc_res = chat_json(
        generate_description_prompt(common_prompt, input_obj, target_audience, platform_rule),
        mock=mock
    )

    cta_res = chat_json(
        generate_cta_prompt(common_prompt, input_obj, target_audience, platform_rule),
        mock=mock
    )

    hashtag_res = chat_json(
        generate_hashtag_prompt(common_prompt, input_obj, target_audience,platform_rule),
        mock=mock
    )

    return {
        "hooks": hook_res.get("hooks", []),
        "script": script_res.get("script", ""),
        "description": desc_res.get("description", ""),
        "ctas": cta_res.get("ctas", []),
        "hashtags": hashtag_res.get("hashtags", []),
    }