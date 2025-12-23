"""
오프라인(=Mock) 스모크 테스트:
- OpenAI 키 없이도 실행 가능해야 합니다.
- outputs/에 JSON이 저장되는지 확인합니다.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(ROOT, "app")

os.chdir(ROOT)

if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from core.common.schema import CommonInput
from core.ch1.generator import generate_ads
from core.ch2.generator import generate_video_script
from core.ch3.generator import generate_sns_post


def main():
    input_base = CommonInput(
        cafe_name="CREMA STUDIO",
        product="카페 음료",
        menu_name="말차 라떼",
        menu_desc="점심 이후 졸린 오후를 리프레시해주는 말차 라떼!",
        tone="유머",
        n=3,
        platform="Instagram",
        video_length="30초",
        style="엔터테인먼트",
        vibe="감성",
    )

    ch1 = generate_ads(input_obj=input_base, mock=True)
    print("CH1 saved:", ch1["saved_path"])

    ch2_in = input_base.model_copy(update={"menu_name": "부드럽고 고소한 편백찜", "platform": "YouTube Shorts"})
    ch2 = generate_video_script(input_obj=ch2_in, mock=True)
    print("CH2 saved:", ch2["saved_path"])

    ch3_in = input_base.model_copy(update={"platform": "Instagram"})
    ch3 = generate_sns_post(input_obj=ch3_in, mock=True)
    print("CH3 saved:", ch3["saved_path"])


if __name__ == "__main__":
    main()
