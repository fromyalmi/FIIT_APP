# app/main.py
# ✅ 권장 실행(Windows 런처/경로 꼬임 예방):
# python -m streamlit run app\main.py

import os
import sys
import streamlit as st

# ------------------------------------------------------------
# ✅ Windows에서 import 루트(경로) 꼬임 방지 안전장치
# - PROJECT_ROOT: ...\FIIT_APP_V2_2_NAVTAB
# - APP_DIR:      ...\FIIT_APP_V2_2_NAVTAB\app
# 이 2개를 sys.path에 넣으면 core.xxx / app.core.xxx 모두 안전해짐
# ------------------------------------------------------------
APP_DIR = os.path.dirname(__file__)          # ...\app
PROJECT_ROOT = os.path.dirname(APP_DIR)      # ...\ (프로젝트 루트)

for p in (PROJECT_ROOT, APP_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

from core.common.bootstrap import app_header, sidebar_brand_block
from core.common.ui import collect_common_input
from core.common.validators import validate_non_empty

from core.ch1.generator import generate_ads
from core.ch2.generator import generate_video_script
from core.ch3.generator import generate_sns_post

from views.ch1_ads import render as render_ch1
from views.ch2_video import render as render_ch2
from views.ch3_sns import render as render_ch3


def _safe_obj_to_dict(obj) -> dict:
    """pydantic/일반객체 모두 dict로 안전 변환 (CH2 저장용 input 스냅샷)"""
    if obj is None:
        return {}
    for name in ("model_dump", "dict"):
        if hasattr(obj, name):
            try:
                return getattr(obj, name)()
            except Exception:
                pass
    if hasattr(obj, "__dict__"):
        try:
            return dict(obj.__dict__)
        except Exception:
            pass
    return {"repr": repr(obj)}


def render_top_nav():
    """
    ✅ A안 구현 핵심:
    - st.tabs는 '현재 선택 탭' 값을 파이썬에서 못 읽는다(클라이언트 UI).
    - 그래서 서버가 값을 아는 네비게이션(라디오/세그먼트)을 탭처럼 보이게 사용한다.
    """
    st.markdown(
        """
        <style>
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


def render_sidebar_inputs(active_nav: str) -> None:
    """
    - 현재 선택 메뉴 입력만 사이드바에 표시
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
                validate_non_empty(getattr(input_obj, "menu_name", ""), "메뉴/주제 이름")
                validate_non_empty(getattr(input_obj, "menu_desc", ""), "설명")
                with st.spinner("CH1 생성 중..."):
                   st.session_state["ch1_result"] = generate_ads(
                    purpose=getattr(input_obj, "purpose", ""),
                    product=getattr(input_obj, "product", ""),
                    menu_name=getattr(input_obj, "menu_name", ""),
                    menu_desc=getattr(input_obj, "menu_desc", ""),
                    tone=getattr(input_obj, "tone", ""),
                    platform=getattr(input_obj, "platform", "instagram"),
                    image_summary=st.session_state.get("ch1_image_summary", ""),
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

                # ✅ CH2 저장용: 입력 스냅샷 저장 (확정 후 outputs 저장에 사용)
                st.session_state["ch2_input_snapshot"] = _safe_obj_to_dict(input_obj)

                # ✅ 새로 생성하면 확정 상태 초기화(다시 선택 가능하게)
                st.session_state["ch2_confirmed"] = False
                st.session_state.pop("ch2_final", None)
                st.session_state.pop("ch2_saved_path", None)
                st.session_state.pop("ch2_save_pending", None)

                # ✅ 여기서 결과 생성 -> 세션에 저장
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


def main():
    app_header()
    sidebar_brand_block()

    active_nav = render_top_nav()
    render_sidebar_inputs(active_nav)

    if active_nav == "광고":
        render_ch1()
    elif active_nav == "영상":
        render_ch2()
    else:
        render_ch3()


if __name__ == "__main__":
    main()
