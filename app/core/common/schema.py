from typing import List, Optional, Literal, Any, Dict
from pydantic import BaseModel, Field


class CommonInput(BaseModel):
    """
    ✅ CH1/CH2/CH3가 공유하는 '통일 입력 스키마'
    - 각 화면에서 필요 없는 값은 기본값/옵션으로 처리
    - 저장 JSON에서 input은 항상 이 키셋을 유지
    """
    cafe_name: str = Field(default="CREMA STUDIO", description="카페명")
    product: str = Field(default="카페 음료", description="제품/서비스")
    menu_name: str = Field(default="말차 라떼", description="메뉴명")
    menu_desc: str = Field(default="", description="메뉴/제품 설명")

    tone: str = Field(default="유머", description="카피/문구 톤")
    n: int = Field(default=5, description="CH1 생성 개수")

    platform: str = Field(default="Instagram", description="플랫폼(영상 또는 SNS)")
    video_length: str = Field(default="30초", description="영상 길이(예: 15초/30초/60초)")
    style: str = Field(default="엔터테인먼트", description="영상/콘텐츠 스타일")
    vibe: str = Field(default="감성", description="SNS 분위기")


class Meta(BaseModel):
    chapter: Literal["ch1_ads", "ch2_video", "ch3_sns"]
    created_at_kst: str
    mock: bool = False
    app_version: str = "v2"


class Ch1Output(BaseModel):
    items: List[str]


class Ch2Output(BaseModel):
    title: str
    script: str
    hashtags: List[str]


class Ch3Output(BaseModel):
    caption: str
    hashtags: List[str]


class Envelope(BaseModel):
    meta: Meta
    input: CommonInput
    output: Dict[str, Any]
