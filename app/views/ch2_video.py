import streamlit as st


def format_hashtags(tags: list[str]) -> str:
    return ", ".join(f"#{tag.lstrip('#')}" for tag in tags)

def render():
    components = st.session_state.get("ch2_result")
    mock = st.session_state.get("toggle_mock_ch2", False)

    if not components:
        st.info("사이드바에서 입력 후 '생성' 버튼을 눌러주세요.")
        return

    if "ch2_confirmed" not in st.session_state:
        st.session_state.ch2_confirmed = False

    if not st.session_state.ch2_confirmed:
        st.subheader("🪝 Hook 선택")
        selected_hook = st.selectbox(
            "Hook 문장",
            components["hooks"],
            key="ch2_hook_select"
        )

        st.subheader("📝 영상 설명")
        st.text_area(
            "설명",
            value=components["description"],
            height=120,
            key="ch2_desc_text"
        )

        st.subheader("🎬 영상 스크립트")
        st.text_area(
            "스크립트",
            value=components["script"],
            height=240,
            key="ch2_script_text"
        )

        st.subheader("📢 CTA 선택")
        selected_cta = st.selectbox(
            "CTA 문장",
            components["ctas"],
            key="ch2_cta_select"
        )

        st.subheader("🏷 해시태그 선택")
        selected_hashtags = st.multiselect(
            "해시태그",
            components["hashtags"],
            default=components["hashtags"][:10],
            key="ch2_hashtag_select"
        )

        if st.button("✅ 확정"):
            st.session_state.ch2_final = {
                "hook": selected_hook,
                "description": st.session_state.ch2_desc_text,
                "script": st.session_state.ch2_script_text,
                "cta": selected_cta,
                "hashtags": selected_hashtags,
            }
            st.session_state.ch2_confirmed = True
            st.rerun()

    else:
        final = st.session_state.ch2_final
        st.success("🎉 확정된 영상 콘텐츠")

        st.markdown("### 🪝 Hook")
        st.markdown(final["hook"])

        st.markdown("### 📝 영상 설명")
        st.markdown(final["description"])

        st.markdown("### 🎬 영상 스크립트")
        st.markdown(final["script"])

        st.markdown("### 📢 CTA")
        st.markdown(final["cta"])

        st.markdown("### 🏷 해시태그")
        st.markdown(format_hashtags(final["hashtags"]))
