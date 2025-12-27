import os
import sys
import streamlit as st

# ------------------------------------------------------------
# ✅ Windows에서 `streamlit run app/main.py` 실행 시
#   app/ 폴더를 import 루트로 잡아주기 위한 안전장치
# ------------------------------------------------------------
APP_DIR = os.path.dirname(__file__)  # ...\app
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from core.common.bootstrap import app_header, sidebar_brand_block
from core.common.ui import collect_common_input
from core.common.validators import validate_non_empty

# CH1은 이미지 분석(analyze_image)까지 사용
from core.ch1.generator import generate_ads, analyze_image
from core.ch2.generator import generate_video_script
from core.ch3.generator import generate_sns_post

from views.ch1_ads import render as render_ch1
from views.ch2_video import render as render_ch2
from views.ch3_sns import render as render_ch3


def render_top_nav() -> str:
    """상단 네비(라디오를 탭처럼 보이게)"""
    st.markdown(
        """
        <style>
        /* 라디오를 탭처럼 보이게 하는 간단한 CSS */
        div[role="radiogroup"] > label {
            border: 1px solid #e5e7eb;
            border-radius: 999px;
            padding: 6px 12px;
            margin-right: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    nav = st.radio(
        "메뉴",
        ["광고", "영상", "SNS/블로그"],
        horizontal=True,
        label_visibility="collapsed",
        key="nav_main",
    )
    return nav


def _normalize_platform_for_ch1(raw: str) -> str:
    """CH1 프롬프트 규칙 키를 맞추기 위한 최소 정규화"""
    if raw is None:
        return "instagram"

    s = str(raw).strip().lower()

    # 이미 규칙 키면 그대로
    if s in {"instagram", "blog", "youtube_script"}:
        return s

    # 흔한 UI 라벨들 매핑
    mapping = {
        "insta": "instagram",
        "ig": "instagram",
        "instagram": "instagram",
        "인스타": "instagram",
        "인스타그램": "instagram",
        "naver blog": "blog",
        "blog": "blog",
        "블로그": "blog",
        "youtube": "youtube_script",
        "youtube shorts": "youtube_script",
        "shorts": "youtube_script",
        "릴스": "youtube_script",
        "쇼츠": "youtube_script",
    }
    return mapping.get(s, "instagram")


def render_sidebar_inputs(active_nav: str) -> None:
    """
    ✅ 구조 원칙(팀 작업 안정화용)
    - 사이드바 입력은 여기(main.py)에서만 만든다.
    - views/* 는 결과만 렌더링한다.
    """
    with st.sidebar:
        st.markdown("## 입력 폼")

        if active_nav == "광고":
            st.caption("CH1 | 광고(카피라이팅)")

            # ✅ CH1 전용: 이미지 업로드(선택)
            # (form 안에 file_uploader 넣으면 스트림릿 버전별로 동작이 헷갈릴 수 있어,
            #  form 밖에 두는 게 초보 팀에 더 안전함)
            imgs = st.file_uploader(
                "📸 광고용 이미지 업로드 (선택, 여러 장 가능)",
                type=["png", "jpg", "jpeg", "webp"],
                accept_multiple_files=True,
                key="ch1_imgs",
            )

            with st.form("form_ch1", clear_on_submit=False):
                input_obj = collect_common_input(prefix="ch1", mode="ch1")
                mock = st.toggle("Mock", value=False, key="toggle_mock_ch1")
                submitted = st.form_submit_button("생성", type="primary")

            if submitted:
                validate_non_empty(getattr(input_obj, "menu_name", ""), "메뉴/주제 이름")
                validate_non_empty(getattr(input_obj, "menu_desc", ""), "설명")

                # ✅ 이미지 분석: 요약 1~N개 만들고, 합쳐서 1줄 요약도 저장
                image_cards = []
                combined_summary = ""

                if imgs:
                    with st.spinner("이미지 분석 중..."):
                        summaries = []
                        for f in imgs:
                            # analyze_image 내부에서 read()를 쓰므로, seek(0) 포함되어 있어야 안전
                            summary = analyze_image(f)
                            summaries.append(summary)
                            image_cards.append(
                                {
                                    "name": getattr(f, "name", "image"),
                                    "bytes": f.getvalue(),
                                    "summary": summary,
                                }
                            )

                        combined_summary = " ".join(summaries).strip()

                # 세션에 저장해두면 view(ch1_ads.py)에서 이미지/요약을 보여줄 수 있음
                st.session_state["ch1_images"] = image_cards
                st.session_state["ch1_image_summary"] = combined_summary

                # ✅ CH1 생성: (팀원 패치 generator.py 시그니처에 맞춰 호출)
                with st.spinner("CH1 생성 중..."):
                    st.session_state["ch1_result"] = generate_ads(
                        purpose=getattr(input_obj, "purpose", ""),
                        product=getattr(input_obj, "product", ""),
                        menu_name=getattr(input_obj, "menu_name", ""),
                        menu_desc=getattr(input_obj, "menu_desc", ""),
                        tone=getattr(input_obj, "tone", ""),
                        platform=_normalize_platform_for_ch1(getattr(input_obj, "platform", "instagram")),
                        image_summary=combined_summary,
                        n=int(getattr(input_obj, "n", 5) or 5),
                        mock=mock,
                    )

        elif active_nav == "영상":
            st.caption("CH2 | 영상(릴스/쇼츠)")
            with st.form("form_ch2", clear_on_submit=False):
                input_obj = collect_common_input(prefix="ch2", mode="ch2")
                mock = st.toggle("Mock", value=False, key="toggle_mock_ch2")
                submitted = st.form_submit_button("생성", type="primary")

            if submitted:
                validate_non_empty(getattr(input_obj, "menu_name", ""), "메뉴/주제 이름")
                with st.spinner("CH2 생성 중..."):
                    st.session_state["ch2_result"] = generate_video_script(input_obj=input_obj, mock=mock)

        else:  # "SNS/블로그"
            st.caption("CH3 | SNS/블로그 포스팅")
            with st.form("form_ch3", clear_on_submit=False):
                input_obj = collect_common_input(prefix="ch3", mode="ch3")
                mock = st.toggle("Mock", value=False, key="toggle_mock_ch3")
                submitted = st.form_submit_button("생성", type="primary")

            if submitted:
                validate_non_empty(getattr(input_obj, "cafe_name", ""), "카페명")
                validate_non_empty(getattr(input_obj, "menu_name", ""), "메뉴/주제 이름")
                with st.spinner("CH3 생성 중..."):
                    st.session_state["ch3_result"] = generate_sns_post(input_obj=input_obj, mock=mock)


def main() -> None:
    app_header()

    # 사이드바 상단 고정 안내
    sidebar_brand_block()

    # ✅ 상단 네비
    active_nav = render_top_nav()

    # ✅ 사이드바는 현재 메뉴 입력만
    render_sidebar_inputs(active_nav)

    # ✅ 메인 화면은 현재 메뉴 결과만
    if active_nav == "광고":
        render_ch1()
    elif active_nav == "영상":
        render_ch2()
    else:
        render_ch3()


if __name__ == "__main__":
    main()
