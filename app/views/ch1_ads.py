import streamlit as st

from core.ch1.generator import make_tts


def render():
    """CH1 결과 화면

    ✅ 규칙:
    - 입력 UI(텍스트 입력/선택/Mock 토글/생성 버튼)는 main.py 사이드바에서만 만든다.
    - 이 파일은 '결과 표시' + (선택) TTS/카드 스타일만 담당한다.
    """

    st.markdown("# 🎯 광고 콘텐츠 생성기")
    st.caption("왼쪽 사이드바에서 입력하고 [생성]을 누르면 결과가 여기에 표시됩니다.")

    # ------------------------------------------------------------
    # ✅ (선택) 이미지 분석 결과 표시
    #   - main.py에서 st.session_state에 저장해 둔 값 활용
    # ------------------------------------------------------------
    image_cards = st.session_state.get("ch1_image_cards", [])
    combined_summary = st.session_state.get("ch1_image_summary", "")

    if image_cards:
        st.markdown("## 📸 이미지 분석")
        cols = st.columns(min(3, len(image_cards)))
        for idx, item in enumerate(image_cards):
            with cols[idx % len(cols)]:
                if item.get("bytes"):
                    st.image(item["bytes"], caption=item.get("name", ""), use_column_width=True)
                if item.get("summary"):
                    st.caption(item["summary"])

        if combined_summary:
            st.info(f"👉 최종 통합 이미지 요약: {combined_summary}")

    # ------------------------------------------------------------
    # ✅ 생성 결과
    # ------------------------------------------------------------
    result = st.session_state.get("ch1_result")
    if not result:
        st.info("아직 생성된 결과가 없어요. 사이드바에서 입력 후 [생성]을 눌러주세요.")
        return

    items = result.get("items") or []

    st.markdown("## 📣 생성 결과")

    if not items:
        st.warning("결과가 비어있습니다. (Mock 모드/입력값을 확인해 주세요)")
    else:
        for i, text in enumerate(items, start=1):
            with st.container(border=True):
                st.markdown(f"**{i}.** {text}")
                # 복사하기 편하게 코드 블록도 같이 제공
                st.code(text)

    saved_path = result.get("saved_path")
    if saved_path:
        st.success(f"저장 완료: {saved_path}")

    # ------------------------------------------------------------
    # ✅ (선택) TTS: 첫 번째 문구만
    #   - 비용/속도 때문에 버튼 눌렀을 때만 생성
    # ------------------------------------------------------------
    if items:
        st.markdown("## 🔊 TTS (첫 번째 문구)")
        voice = st.selectbox(
            "보이스",
            ["alloy", "aria", "sage", "verse", "coral"],
            index=0,
            key="ch1_tts_voice",
        )

        if st.button("TTS 생성", key="btn_ch1_tts"):
            with st.spinner("음성 생성 중..."):
                audio_buf = make_tts(items[0], voice=voice)
            st.audio(audio_buf, format="audio/mp3")
            st.download_button(
                "MP3 다운로드",
                data=audio_buf.getvalue(),
                file_name="ch1_ad_voice.mp3",
                mime="audio/mpeg",
            )
