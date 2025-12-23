import streamlit as st


def render():
    st.markdown("## FIIT - Chapter 1: 광고 콘텐츠 생성기")
    st.caption("✅ 입력은 왼쪽 사이드바에서 하고, 결과는 여기서 확인합니다.")

    result = st.session_state.get("ch1_result")
    if not result:
        st.info("왼쪽 사이드바에서 **CH1 입력 → CH1 생성**을 누르면 결과가 여기에 표시됩니다.")
        return

    st.markdown("### 결과")
    for i, line in enumerate(result.get("items", []), start=1):
        st.write(f"{i}. {line}")

    saved_path = result.get("saved_path", "")
    if saved_path:
        st.success(f"저장 완료: {saved_path}")
