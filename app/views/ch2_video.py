# app/views/ch2_video.py
import streamlit as st

from core.common.storage import save_json
from core.common.bootstrap import kst_now


def format_hashtags(tags: list[str]) -> str:
    # 화면 출력용: "#tag1 #tag2 ..."
    return " ".join(f"#{tag.lstrip('#')}" for tag in tags)


def render():
    components = st.session_state.get("ch2_result")
    mock = st.session_state.get("toggle_mock_ch2", False)

    if not components:
        st.info("사이드바에서 입력 후 '생성' 버튼을 눌러주세요.")
        return

    if "ch2_confirmed" not in st.session_state:
        st.session_state["ch2_confirmed"] = False

    if not st.session_state["ch2_confirmed"]:
        st.subheader("🪝 Hook 선택")
        selected_hook = st.selectbox(
            "Hook 문장",
            components.get("hooks", []),
            key="ch2_hook_select"
        )

        st.subheader("📝 영상 설명")
        st.text_area(
            "설명",
            value=components.get("description", ""),
            height=120,
            key="ch2_desc_text"
        )

        st.subheader("🎬 영상 스크립트")
        st.text_area(
            "스크립트",
            value=components.get("script", ""),
            height=240,
            key="ch2_script_text"
        )

        st.subheader("📢 CTA 선택")
        selected_cta = st.selectbox(
            "CTA 문장",
            components.get("ctas", []),
            key="ch2_cta_select"
        )

        st.subheader("🏷 해시태그 선택")
        hashtags = components.get("hashtags", [])
        selected_hashtags = st.multiselect(
            "해시태그",
            hashtags,
            default=hashtags[:10],
            key="ch2_hashtag_select"
        )

        # ✅ 확정 + 저장 (outputs/에 JSON 저장)
        if st.button("✅ 확정 및 저장", type="primary", key="btn_ch2_confirm_save"):
            final = {
                "hook": selected_hook,
                "description": st.session_state.get("ch2_desc_text", ""),
                "script": st.session_state.get("ch2_script_text", ""),
                "cta": selected_cta,
                "hashtags": selected_hashtags,
            }

            # 입력값 스냅샷(없으면 빈 dict로라도 저장)
            input_snapshot = st.session_state.get("ch2_input_snapshot", {})

            payload = {
                "meta": {
                    "chapter": "ch2_video",
                    "created_at_kst": kst_now().strftime("%Y-%m-%d_%H:%M:%S (KST)"),
                    "mock": mock,
                },
                "input": input_snapshot,
                "output": final,
            }

            saved_path = save_json(payload, filename_prefix="video_result")

            st.session_state["ch2_final"] = final
            st.session_state["ch2_saved_path"] = saved_path
            st.session_state["ch2_confirmed"] = True
            st.rerun()

    else:
        final = st.session_state.get("ch2_final", {})
        saved_path = st.session_state.get("ch2_saved_path", "")

        st.success("🎉 확정된 영상 콘텐츠")

        st.markdown("### 🪝 Hook")
        st.write(final.get("hook", ""))

        st.markdown("### 📝 영상 설명")
        st.write(final.get("description", ""))

        st.markdown("### 🎬 영상 스크립트")
        st.write(final.get("script", ""))

        st.markdown("### 📢 CTA")
        st.write(final.get("cta", ""))

        st.markdown("### 🏷 해시태그")
        st.code(format_hashtags(final.get("hashtags", [])))

        if saved_path:
            st.success(f"저장 완료: {saved_path}")

