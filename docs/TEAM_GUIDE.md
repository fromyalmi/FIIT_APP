# TEAM GUIDE (7인 역할 분담 기준)

## 공통 규칙 (절대 깨지면 안 됨)
1) **입력 스키마(CommonInput)는 공통**입니다. (CH1/CH2/CH3가 동일 키 사용)
2) 저장 JSON은 항상 같은 Envelope 구조를 사용합니다:
   - meta / input / output
3) Streamlit 위젯은 **반드시 key를 고유**하게 넣습니다.
4) 결과는 `outputs/`에 저장됩니다.

## 담당 파일
- CH1 (광고 2인)
  - `app/views/ch1_ads.py`
  - `app/core/ch1/*`
- CH2 (영상 2인)
  - `app/views/ch2_video.py`
  - `app/core/ch2/*`
- CH3 (SNS 2인)
  - `app/views/ch3_sns.py`
  - `app/core/ch3/*`
- 팀장 (깃/일정/공통 1인)
  - `app/main.py`
  - `app/core/common/*`
  - 스키마/저장/LLM 호출 규칙 유지

## 오프라인 테스트
```bash
python scripts/smoke_test_offline.py
```


## UI 레이아웃(중요)
- 입력칸은 **왼쪽 사이드바**에만 둡니다.
- 결과 출력은 메인 탭(광고/영상/SNS)에서만 보여줍니다.
- 즉, 팀원들은 각 챕터의 '입력 UI'를 메인 화면에 다시 만들지 않습니다.


## A안(현재 선택 메뉴만 사이드바 입력 노출)
- 상단 메뉴는 Streamlit 탭 대신 '가로 라디오(탭처럼 보이게 CSS)'로 구현했습니다.
- 이유: st.tabs는 파이썬에서 현재 선택 탭 값을 직접 알 수 없어, 사이드바 입력을 동기화하기 어렵습니다.
