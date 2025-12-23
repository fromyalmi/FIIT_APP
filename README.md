# FIIT_APP_V2 (CREMA STUDIO 데모)

카페 사장님(자영업자)을 위한 **AI 마케팅 콘텐츠 생성기** 데모입니다.

- CH1: 광고(카피라이팅 문구) 생성기 (N개 리스트)
- CH2: 영상(인스타 릴스/유튜브 쇼츠) 스크립트 생성기 (길이/플랫폼/스타일)
- CH3: SNS/블로그 포스팅 생성기

시연 샘플 카페명: **CREMA STUDIO**

---

## ✅ V2 핵심
- **CH1/CH2/CH3 입력 키를 완전 통일**(CommonInput)
- 저장 결과 JSON도 **meta/input/output Envelope로 통일**
- Streamlit 토글/버튼/입력들 **전부 key 고정** (DuplicateElementId 방지)
- Mock 토글 ON이면 **OpenAI 호출 없이** 결과 생성 + 저장까지 됨

---

## 실행 (Windows / VS Code)

### 1) 가상환경
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2) 설치
```bash
pip install -r requirements.txt
```

### 3) 환경변수
1. `.env.example` → `.env` 로 복사
2. `.env`에 `OPENAI_API_KEY=...` 입력

### 4) 실행
```bash
streamlit run app/main.py
```

---

## 오프라인(Mock) 테스트
- 각 화면 좌측 `Mock` 토글 ON → OpenAI 호출 없이 더미 결과 생성 + outputs 저장
- 또는:
```bash
python scripts/smoke_test_offline.py
```

---

## 출력 파일
- 결과는 `outputs/`에 JSON으로 저장됩니다.
- 파일 예시:
  - `ads_result_20251223_1518.json`
  - `video_result_20251223_1518.json`
  - `sns_result_20251223_1518.json`

---

## 스키마 참고
- `schemas/` 폴더에 샘플 JSON 제공
