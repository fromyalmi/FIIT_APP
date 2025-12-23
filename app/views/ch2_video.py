import streamlit as st


def render():
    st.markdown("## 영상 콘텐츠 스크립트 생성기")
    st.caption("✅ 입력은 왼쪽 사이드바에서 하고, 결과는 여기서 확인합니다.")

    result = st.session_state.get("ch2_result")
    if not result:
        st.info("왼쪽 사이드바에서 **CH2 입력 → CH2 생성**을 누르면 결과가 여기에 표시됩니다.")
        return

    st.markdown("### 결과")
    title = result.get("title", "")
    script = result.get("script", "")
    hashtags = result.get("hashtags", [])

    if title:
        st.info(f"제목 제안: {title}")
    if script:
        st.markdown("**본문**")
        st.write(script)
    if hashtags:
        st.markdown("**해시태그/키워드**")
        st.write(" ".join(hashtags))

    saved_path = result.get("saved_path", "")
    if saved_path:
        st.success(f"저장 완료: {saved_path}")
