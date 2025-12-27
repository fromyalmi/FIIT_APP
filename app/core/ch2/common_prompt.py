from app.core.common.schema import CommonInput 

def build_common_prompt(input_obj: CommonInput) -> str:
    return f"""
[카페명] {input_obj.cafe_name}
[제품/서비스] {input_obj.product}
[메뉴 이름 또는 주제] {input_obj.menu_name}
[설명] {input_obj.menu_desc}
[타겟 플랫폼] {input_obj.platform}
[영상 길이] {input_obj.video_length}
[스타일 톤] {input_obj.tone}
"""
