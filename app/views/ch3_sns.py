import streamlit as st


def render():
    st.markdown("## 카페 SNS/블로그 포스팅 생성기")
    st.caption("✅ 입력은 왼쪽 사이드바에서 하고, 결과는 여기서 확인합니다.")

    result = st.session_state.get("ch3_result")
    if not result:
        st.info("왼쪽 사이드바에서 **CH3 입력 → CH3 생성**을 누르면 결과가 여기에 표시됩니다.")
        return

    st.markdown("### 결과")
    caption = result.get("caption", "")
    hashtags = result.get("hashtags", [])

    if caption:
        st.markdown("**본문**")
        st.write(caption)
    if hashtags:
        st.markdown("**해시태그**")
        st.write(" ".join(hashtags))

    saved_path = result.get("saved_path", "")
    if saved_path:
        st.success(f"저장 완료: {saved_path}")
