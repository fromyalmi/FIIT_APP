import streamlit as st
from datetime import datetime

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None


APP_TITLE = "CREMA STUDIO"
APP_SUBTITLE = "카페 사장님을 위한 AI 마케팅 플랫폼"


def kst_now() -> datetime:
    """KST(Asia/Seoul) 기준 현재 시각"""
    if ZoneInfo is None:
        return datetime.now()
    return datetime.now(ZoneInfo("Asia/Seoul"))


def kst_stamp_compact() -> str:
    """파일명용 스탬프: YYYYMMDD_HHMM"""
    return kst_now().strftime("%Y%m%d_%H%M")


def app_header():
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)


def sidebar_brand_block():
    with st.sidebar:
        st.markdown("### 입력 안내")
        st.write("프로그램 유저: 마케팅이 필요한 자영업자 카페 사장님")
        st.write("시연 샘플 카페명: **CREMA STUDIO**")
        st.divider()
        st.markdown("### 저장 규칙")
        st.write("결과는 `outputs/` 폴더에 JSON으로 저장됩니다.")
