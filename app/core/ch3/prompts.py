# prompts.py
from core.common.schema import CommonInput


def platform_kind(platform: str) -> str:
    p = (platform or "").strip().lower()
    if any(k in p for k in ["naver", "blog", "네이버", "블로그"]):
        return "naver"
    if any(k in p for k in ["insta", "instagram", "인스타", "그램"]):
        return "instagram"
    return "instagram"


def _ctx(input_obj: CommonInput) -> dict:
    return {
        "cafe_name": getattr(input_obj, "cafe_name", ""),
        "menu_name": getattr(input_obj, "menu_name", ""),
        "menu_desc": getattr(input_obj, "menu_desc", ""),
        "vibe": getattr(input_obj, "vibe", ""),
        "platform": getattr(input_obj, "platform", ""),
    }


def _common_rules(input_obj: CommonInput) -> str:
    c = _ctx(input_obj)

    return f"""
너는 카페 마케팅 글을 쓰는 사람이다.

[입력]
- 카페명: {c["cafe_name"]}
- 메뉴/주제: {c["menu_name"]}
- 설명: {c["menu_desc"]}
- 분위기: {c["vibe"]}
- 플랫폼: {c["platform"]}

[중요 - 출력 규칙]
- 반드시 JSON만 출력. 설명/머리말/마크다운/코드블록 금지.
- 스키마 고정: {{"caption": string, "hashtags": [string, ...]}}
- caption에 해시태그(#) 절대 넣지 말 것(hashtags 배열에만).
- 사실성: 입력에 없는 가격/기간/혜택/원산지/무료증정/예약/DM/전화 유도 등은 단정 금지.
- 'less' 같은 UI 잔여 텍스트, 따옴표 남발, 과장광고 문구 금지.

[caption 공통]
- 첫 3줄 안에 카페명과 메뉴/주제를 각각 1회 이상 포함
- 줄바꿈은 \\n 사용

[hashtags 공통]
- 각 요소는 문자열 1개이며, 반드시 '#'로 시작
- 공백 포함 금지(예: '#감성카페' OK, '#감성 카페' X)
- 중복 금지

[TONE 공통]
- vibe 값은 반드시 반영하라. 아래 패턴/금지/톤을 지켜 caption을 작성하라.

1) vibe="미니멀"
- 목표: 군더더기 없이 깔끔/정돈. 핵심만.
- 금지: 과장/감탄/장황/이모지 남발
- 패턴:
  [제목 1줄] "{c["cafe_name"]} {c["menu_name"]}"
  [핵심] 맛/식감/향/온도/페어링 중 2~3개만 짧게
  [마무리 1줄] "오늘도 정돈된 한 잔."
- 이모지: 0~2개

2) vibe="감성"
- 목표: 포근/친근. 장면이 그려지게.
- 금지: 오글/과확신(보장/무조건)/과장
- 패턴:
  [도입 1줄] 오늘의 순간(짧게)
  [감각] 향/온기/빛/소리 중 2개 이상
  [메뉴] "한 모금/한 입" 중심
  [마무리] "오늘도 여기서, 포근하게."
- 이모지: 3~6개

3) vibe="정보형"
- 목표: 이해 빠른 설명. 구조화.
- 금지: 입력 없는 가격/효능/원산지/이벤트 단정
- 패턴:
  [요약 1줄] "한 줄 요약: ..."
  [포인트] 맛/식감/향/재료(입력 근거) 3개
  [추천] 추천 상황 2개
  [마무리 1줄] "선택이 쉬워지는 오늘의 메뉴."
- 이모지: 0~2개(없어도 됨)

4) vibe="유머"
- 목표: 재치 1~2번, 곧바로 메뉴 핵심으로 회수.
- 금지: 조롱/비하/논란/과격 밈/반말 과다
- 패턴:
  [훅 1줄] 짧은 농담(상황극/의인화/비유 중 1개)
  [핵심] 맛/식감/향 중 2~3개를 명확히
  [드립] 1회만 추가(과장 금지)
  [마무리 1줄] "오늘은 {c["menu_name"]}."
- 이모지: 5~8개
"""


def build_prompt_naver(input_obj: CommonInput) -> str:
    c = _ctx(input_obj)

    return f"""
{_common_rules(input_obj)}

[플랫폼 규칙 - 네이버 블로그]

[TASK]
카페 사장(운영자) 관점에서 ‘{c["menu_name"]}’을(를) 홍보하는 네이버 블로그 글을 생성한다.
읽는 사람이 저장/공유하고 싶은 글을 만든다.

[CONTEXT]
- 카페명: {c["cafe_name"]}
- 메뉴/주제: {c["menu_name"]}
- 메뉴 설명(사용자 입력 그대로): {c["menu_desc"]}
- 분위기(vibe): {c["vibe"]}

[FORMAT]
- 오직 JSON만 출력.
- 스키마: {{"caption": string, "hashtags": [string, ...]}}

- caption(네이버):
  - 3~5개 문단(문단 사이 빈 줄 1개, 줄바꿈은 \\n)
  - 2문장 사이 줄 바꿈
  - 800자 - 1200자 분량
  - 소제목/번호 2~3개 포함
  - 한 문장은 짧게, 문단은 3~5문장
  - 문단 내용 중복 금지
  - 이모지 6~12개

- hashtags(네이버):
  - 5~10개
  - 최소 포함 권장: #{c["cafe_name"]} #{c["menu_name"]} #카페 #카페추천
"""


def build_prompt_instagram(input_obj: CommonInput) -> str:
    c = _ctx(input_obj)

    return f"""
{_common_rules(input_obj)}

[플랫폼 규칙 - 인스타그램]

[TASK]
카페 사장(운영자) 관점에서 {c["menu_name"]}을(를) 홍보하는 인스타그램 캡션을 생성한다.
짧고 리듬감 있게, 첫 줄 훅으로 시작한다.

[CONTEXT]
- 카페명: {c["cafe_name"]}
- 메뉴/주제: {c["menu_name"]}
- 메뉴 설명(사용자 입력 그대로): {c["menu_desc"]}
- 분위기(vibe): {c["vibe"]}

[FORMAT]
- 오직 JSON만 출력.
- 스키마: {{"caption": string, "hashtags": [string, ...]}}

- caption(인스타):
  - 6~10줄
  - 한문장 끝나면 줄바꿈, 줄바꿈은 \\n
  - 이모지 2~6개
  - 마지막 줄은 가벼운 행동 유도(저장/오늘 한 잔 등)
  - (DM/예약/전화 유도는 입력 근거 있을 때만)

- hashtags(인스타):
  - 12~15개
  - 최소 포함 권장: #{c["cafe_name"]} #{c["menu_name"]} #카페 #카페추천 #커피스타그램
"""


def build_sns_prompt(input_obj: CommonInput) -> str:
    kind = platform_kind(getattr(input_obj, "platform", ""))
    return build_prompt_naver(input_obj) if kind == "naver" else build_prompt_instagram(input_obj)


