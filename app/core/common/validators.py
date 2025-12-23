import streamlit as st


def validate_non_empty(value: str, field_name: str) -> None:
    """비어 있으면 Streamlit에서 즉시 에러를 띄우고 중단합니다."""
    if value is None or str(value).strip() == "":
        st.error(f"'{field_name}'을(를) 입력해주세요.")
        st.stop()


def clamp_int(n: int, min_value: int, max_value: int) -> int:
    """정수 범위 보정"""
    try:
        n = int(n)
    except Exception:
        return min_value
    return max(min_value, min(max_value, n))
