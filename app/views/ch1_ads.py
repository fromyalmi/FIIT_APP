import streamlit as st
import json

from core.common.validators import validate_non_empty, clamp_int
from core.ch1.generator import analyze_image, generate_ads, make_tts

def render():
        # CH1에서만 사이드바 숨기기
    hide_sidebar = """
        <style>
        [data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        </style>
    """
    st.markdown(hide_sidebar, unsafe_allow_html=True)
    st.title("🎯 광고 콘텐츠 생성기")
    st.caption("이미지 분석 + 목적 기반 카피 + 플랫폼 스타일 + TTS 음성 생성까지 한번에!")

    # -------------------------
    # 레이아웃 구성
    # -------------------------
    left_col, right_col = st.columns([1, 2], gap="large")

    # ==============================================================
    # ◀ LEFT : 입력 패널
    # ==============================================================

    PURPOSE_EXAMPLES = {
    "신메뉴 출시": {
        "product": "ex) 카페 음료",
        "menu_name": "ex) 말차 크림 라떼",
        "menu_desc": "ex) 진한 말차와 부드러운 크림이 만나 새롭게 탄생한 신메뉴를 만나보세요."
    },
    "단골 고객 이벤트": {
        "product": "ex) 혜택 안내",
        "menu_name": "ex) 단골 감사 이벤트",
        "menu_desc": "ex) 항상 찾아주시는 단골 고객님께 특별한 혜택을 드립니다."
    },
    "1+1 이벤트": {
        "product": "ex) 프로모션",
        "menu_name": "ex) 아메리카노 1+1",
        "menu_desc": "ex) 오늘 하루, 아메리카노 한 잔 더! 친구와 함께 즐겨보세요."
    },
    "시즌 메뉴": {
        "product": "ex) 시즌 음료",
        "menu_name": "ex) 겨울 딸기 라떼",
        "menu_desc": "ex) 제철 딸기의 달콤함을 담은 겨울 시즌 한정 메뉴입니다."
    },
    "시간대별 추천": {
        "product": "ex) 추천 메뉴",
        "menu_name": "ex) 오후 힐링 라떼",
        "menu_desc": "ex) 나른한 오후, 부드러운 라떼 한 잔으로 리프레시해보세요."
    },
    "한정 수량 판매": {
        "product": "ex) 한정 메뉴",
        "menu_name": "ex) 시그니처 디저트",
        "menu_desc": "ex) 매일 소량만 준비되는 한정 수량 메뉴입니다. 서둘러 주세요!"
    },
    "매장 분위기 강조": {
        "product": "ex) 매장 홍보",
        "menu_name": "ex) 감성 카페 공간",
        "menu_desc": "ex) 따뜻한 우드톤과 부드러운 조명이 어우러진 편안한 공간입니다."
    },}

    with left_col:
        st.markdown("### 📝 입력 정보")

        mock = st.toggle("Mock 모드", value=False, key="view_toggle_mock_ch1")

        purpose = st.selectbox(
        "홍보 목적",
        list(PURPOSE_EXAMPLES.keys()),
        key="ch1_purpose"
    )

        # 목적 변경 시 예시 자동 세팅
        example = PURPOSE_EXAMPLES[purpose]
        if st.session_state.get("prev_purpose") != purpose:
            st.session_state["ch1_product"] = example["product"]
            st.session_state["ch1_menu_name"] = example["menu_name"]
            st.session_state["ch1_menu_desc"] = example["menu_desc"]
            st.session_state["prev_purpose"] = purpose

        product = st.text_input("제품/서비스", key="ch1_product")

        menu_name = st.text_input("메뉴 이름", key="ch1_menu_name")

        menu_desc = st.text_area("메뉴 설명", height=110, key="ch1_menu_desc")

        tone = st.selectbox("광고 톤",
            ["유머", "감성", "정보형", "직설", "고급"],
            index=1,
            key="ch1_tone")

        platform = st.selectbox("플랫폼 스타일",
            ["instagram", "blog", "youtube_script"],
            index=0,
            key="ch1_platform")

        imgs = st.file_uploader("📸 광고용 이미지 업로드 (여러 장 가능)",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True)

        st.caption("여러 장 업로드 시 AI가 모든 이미지를 분석해 통합해 반영합니다.")

        n = st.slider("생성 개수", 1, 10, value=5, key="ch1_n")

        generate_btn = st.button("🚀 광고 콘텐츠 생성", use_container_width=True)

    # ==============================================================
    # ▶ RIGHT : 출력 패널
    # ==============================================================
    with right_col:
        st.markdown("### 📢 생성 결과")

        if generate_btn:

            # 입력 검증
            validate_non_empty(menu_name, "메뉴 이름")
            validate_non_empty(menu_desc, "메뉴 설명")
            n = clamp_int(n, 1, 20)

            # ---------------------
            # 1) 이미지 분석 처리
            # ---------------------
            image_summary = ""
            if imgs:
                st.markdown("#### 📸 이미지 분석")
                all_summaries = []

                with st.spinner("이미지 분석 중…"):
                    for img in imgs:
                        summary = analyze_image(img)
                        st.image(img, width=180)
                        all_summaries.append(summary)

                image_summary = " ".join(all_summaries)
                st.info(f"👉 최종 통합 이미지 요약:\n{image_summary}")

            # ---------------------
            # 2) 광고 카피 생성
            # ---------------------
            with st.spinner("✏️ 광고 문구 생성 중…"):
                result = generate_ads(
                    product=product,
                    menu_name=menu_name,
                    menu_desc=menu_desc,
                    tone=tone,
                    purpose=purpose,
                    platform=platform,
                    image_summary=image_summary,
                    n=n,
                    mock=mock,
                )

            items = result["items"]
            st.success("✔ 광고 문구 생성 완료!")

            # 카드 스타일 표시
            for i, line in enumerate(items, start=1):
                st.markdown(
                    f"""
                    <div style="
                        padding:14px;
                        margin-bottom:12px;
                        border-radius:10px;
                        background:#fff;
                        border:1px solid #e8e8e8;
                    ">
                    <b>{i}.</b> {line}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # ---------------------
            # 3) TTS 음성 생성
            # ---------------------
            st.markdown("### 🔉 음성 생성 (TTS)")

            try:
                sample_text = items[0] if items else ""
                with st.spinner("음성 변환 중…"):
                    audio_buf = make_tts(sample_text)

                st.audio(audio_buf, format="audio/mp3")
                st.download_button(
                    label="🔊 음성 파일 다운로드",
                    data=audio_buf,
                    file_name="ad_voice.mp3",
                    mime="audio/mp3"
                )

            except Exception as e:
                st.error(f"TTS 변환 중 오류가 발생했습니다: {e}")

            # 저장 경로 출력
            st.info(f"📁 JSON 저장 완료: {result['saved_path']}")
