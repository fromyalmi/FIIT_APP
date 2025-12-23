import os
import sys
import streamlit as st

APP_DIR = os.path.dirname(__file__)
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from core.common.bootstrap import app_header, sidebar_brand_block
from core.common.ui import collect_common_input
from core.common.validators import validate_non_empty
from core.ch1.generator import generate_ads
from core.ch2.generator import generate_video_script
from core.ch3.generator import generate_sns_post

from views.ch1_ads import render as render_ch1
from views.ch2_video import render as render_ch2
from views.ch3_sns import render as render_ch3


def render_top_nav():
    """
    ✅ A안 구현 핵심:
    - st.tabs는 '현재 선택 탭' 값을 파이썬에서 못 읽는다(클라이언트 UI).
    - 그래서 서버가 값을 아는 네비게이션(라디오/세그먼트)을 탭처럼 보이게 사용한다.
    """
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


def render_sidebar_inputs(active_nav: str):
    """
    ✅ 요청 반영(A):
    - '현재 선택된 메뉴'에 해당하는 입력 폼만 사이드바에 표시
    - 생성 버튼은 사이드바에서 누르고
    - 결과는 메인 화면(동일 메뉴 페이지)에서 확인
    """
    with st.sidebar:
        st.markdown("## 입력 폼")

        if active_nav == "광고":
            st.caption("CH1 | 광고(카피라이팅)")
            with st.form("form_ch1", clear_on_submit=False):
                input_obj = collect_common_input(prefix="ch1", mode="ch1")
                mock = st.toggle("Mock", value=False, key="toggle_mock_ch1")
                submitted = st.form_submit_button("생성", type="primary")

            if submitted:
                validate_non_empty(input_obj.menu_name, "메뉴/주제 이름")
                validate_non_empty(input_obj.menu_desc, "설명")
                with st.spinner("CH1 생성 중..."):
                    st.session_state["ch1_result"] = generate_ads(input_obj=input_obj, mock=mock)

        elif active_nav == "영상":
            st.caption("CH2 | 영상(릴스/쇼츠)")
            with st.form("form_ch2", clear_on_submit=False):
                input_obj = collect_common_input(prefix="ch2", mode="ch2")
                mock = st.toggle("Mock", value=False, key="toggle_mock_ch2")
                submitted = st.form_submit_button("생성", type="primary")

            if submitted:
                validate_non_empty(input_obj.menu_name, "메뉴/주제 이름")
                with st.spinner("CH2 생성 중..."):
                    st.session_state["ch2_result"] = generate_video_script(input_obj=input_obj, mock=mock)

        else:  # "SNS/블로그"
            st.caption("CH3 | SNS/블로그 포스팅")
            with st.form("form_ch3", clear_on_submit=False):
                input_obj = collect_common_input(prefix="ch3", mode="ch3")
                mock = st.toggle("Mock", value=False, key="toggle_mock_ch3")
                submitted = st.form_submit_button("생성", type="primary")

            if submitted:
                validate_non_empty(input_obj.cafe_name, "카페명")
                validate_non_empty(input_obj.menu_name, "메뉴/주제 이름")
                with st.spinner("CH3 생성 중..."):
                    st.session_state["ch3_result"] = generate_sns_post(input_obj=input_obj, mock=mock)


def main():
    app_header()

    # 사이드바 상단 고정 안내
    sidebar_brand_block()

    # ✅ 상단 네비(탭처럼 보이는 라디오)
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
