import streamlit as st
from .constants import TONES, VIDEO_PLATFORMS, VIDEO_LENGTHS, VIDEO_STYLES, SNS_PLATFORMS, SNS_VIBES
from .schema import CommonInput
from .validators import clamp_int


def _k(prefix: str, name: str) -> str:
    """Streamlit 위젯 key 충돌 방지용"""
    return f"{prefix}__{name}"


def collect_common_input(prefix: str, mode: str) -> CommonInput:
    """
    mode: "ch1" | "ch2" | "ch3"
    - mode에 따라 보여주는 필드를 다르게 하지만
    - 반환은 항상 CommonInput(키 통일)로 돌려준다.
    """
    # 공통(모든 챕터에서 존재하는 값)
    cafe_name = st.text_input("카페명", value="CREMA STUDIO", key=_k(prefix, "cafe_name"))
    product = st.text_input("제품/서비스", value="카페 음료", key=_k(prefix, "product"))
    menu_name = st.text_input("메뉴/주제 이름", value="말차 라떼", key=_k(prefix, "menu_name"))
    menu_desc = st.text_area("설명", value="", height=110, key=_k(prefix, "menu_desc"))

    tone = "유머"
    n = 5
    platform = "Instagram"
    video_length = "30초"
    style = "엔터테인먼트"
    vibe = "감성"

    if mode == "ch1":
        tone = st.selectbox("톤/스타일", TONES, index=0, key=_k(prefix, "tone"))
        n = st.slider("생성 개수", min_value=1, max_value=10, value=5, step=1, key=_k(prefix, "n"))
        n = clamp_int(n, 1, 20)

    if mode == "ch2":
        platform = st.selectbox("플랫폼", VIDEO_PLATFORMS, index=1, key=_k(prefix, "platform_video"))
        video_length = st.selectbox("영상 길이", VIDEO_LENGTHS, index=1, key=_k(prefix, "video_length"))
        style = st.selectbox("스타일", VIDEO_STYLES, index=0, key=_k(prefix, "style"))

    if mode == "ch3":
        platform = st.selectbox("플랫폼", SNS_PLATFORMS, index=0, key=_k(prefix, "platform_sns"))
        vibe = st.selectbox("분위기", SNS_VIBES, index=0, key=_k(prefix, "vibe"))

    return CommonInput(
        cafe_name=cafe_name,
        product=product,
        menu_name=menu_name,
        menu_desc=menu_desc,
        tone=tone,
        n=n,
        platform=platform,
        video_length=video_length,
        style=style,
        vibe=vibe,
    )
