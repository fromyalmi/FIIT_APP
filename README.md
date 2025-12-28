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

## ✅ 결과 저장 규칙 (팀원 질문 방지용: "저장 어디됨?" 금지)
- 저장 위치: **프로젝트 루트 기준 `outputs/` 폴더**
- 파일명 규칙: `ads_result_YYYYMMDD_HHMM.json`, `video_result_YYYYMMDD_HHMM.json`, `sns_result_YYYYMMDD_HHMM.json` (**KST 기준 타임스탬프**)
- 저장 트리거: 각 CH 결과 화면에서 **“확정(저장)” 버튼**을 눌러야 실제로 파일이 생성됨 (생성만 하면 저장 안 될 수 있음)
- 저장 완료 표시: 저장되면 **화면에 저장 완료 메시지 + saved_path(경로)**가 표시됨
- Git 관리: `outputs/`는 **.gitignore로 제외** (테스트 산출물 커밋 금지)이** 결과 생성 + 저장까지 됨

---

## 실행 가이드 (Windows / VS Code) — 팀원용

### 0) “정답 위치”부터 확인 (가장 중요)
- 반드시 **프로젝트 루트 폴더**에서 실행하세요.
  ✅ 루트 기준: `README.md`와 `app/` 폴더가 같은 위치에 보이는 곳
- ❌ `cd app`로 들어가서 실행하면 `core`/`views` import가 깨질 수 있어요.

### 1) 가상환경 만들기 (처음 1회)
터미널(CMD)에서 프로젝트 루트로 이동 후:

```bat
python -m venv .venv
```

### 2) 가상환경 활성화 (매번)
```bat
.venv\Scripts\activate
```

### 3) 패키지 설치 (처음 1회 + requirements 변경 시)
```bat
python -m pip install -r requirements.txt
```

### 4) 실행 (권장: 런처 오류를 피하는 방식)
```bat
python -m streamlit run app\main.py
```

---

## 자주 터지는 오류 3종 “즉시 처방”

### A) `Fatal error in launcher ... streamlit.exe ...` (윈도우 런처 깨짐)
아래 1줄로 복구 후 다시 실행:

```bat
python -m pip install --upgrade --force-reinstall streamlit
```

### B) `ModuleNotFoundError: No module named 'core'` 또는 `app.core...` 못 찾음
대부분 **루트가 아니라 다른 폴더에서 실행해서** 생깁니다.

1) 루트로 이동:
```bat
cd C:\Workspace\Team_FIIT\FIIT_APP\FIIT_APP_V2_2_NAVTAB
```
2) 다시 실행:
```bat
python -m streamlit run app\main.py
```

(임시 처방) 그래도 안 되면 한 번만:
```bat
set PYTHONPATH=%CD%
```

### C) `StreamlitDuplicateElementKey` (toggle key 중복)
- 같은 `key="..."` 위젯이 **2번 생성된 것**입니다.
- 해결 원칙: **위젯(토글/입력)은 한 곳에서만 생성**하고, 다른 곳은 `st.session_state.get(...)`로 값만 읽기.

---

## 팀원 제출 규칙 (패치 ZIP)
- ZIP 최상단에 `app/` 폴더가 **그대로** 있어야 함 ✅
- ZIP에 `.venv/`, `outputs/`, `.git/`, `__pycache__/` 포함 금지 🚫

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
