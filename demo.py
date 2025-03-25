import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

# .env 파일에 OPENAI_API_KEY=<YOUR_API_KEY> 형태로 키가 저장되어 있어야 합니다.
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

# ----------------------------
# 1) 페이지 기본 설정 및 CSS
# ----------------------------
st.set_page_config(
    page_title="[디자인 연구소] 이르마 : 핵심 키워드 & 브랜드 네임 제안 보고서",
    layout="wide",
    page_icon="✨"
)

# 간단한 CSS 커스터마이징
custom_css = """
<style>
    /* 전체 배경색 & 폰트 설정 */
    body {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #f9f9f9;
    }

    /* 메인 타이틀 컬러 */
    .css-18e3th9 {
        color: #3F51B5 !important; /* 보라 계열 색상 */
    }

    /* 서브 타이틀 크기 & 색 */
    h2, h3 {
        color: #2E3A59 !important;
    }

    /* 버튼 디자인 */
    .stButton button {
        background-color: #3F51B5 !important;
        color: #ffffff !important;
        border-radius: 8px;
        border: none;
        font-size: 1rem;
        padding: 0.6rem 1rem;
    }

    .stButton button:hover {
        background-color: #303F9F !important;
    }

    /* 카드 형태 느낌을 주는 컨테이너 스타일 */
    .report-container {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----------------------------
# 2) 사이드바 구성
# ----------------------------
with st.sidebar:
    st.image(
        "https://static.wixstatic.com/media/62db02_aa239ba95a7744f7bcb74fa5992e3450~mv2.jpg/v1/fill/w_794,h_881,al_c/62db02_aa239ba95a7744f7bcb74fa5992e3450~mv2.jpg",
        use_container_width=True
    )
    st.markdown("## **브랜드 네임 보고서**")
    st.write("**이르마 브랜드 네이밍 서비스**는 AI 기술을 활용하여 최적의 브랜드명을 제안해드립니다.")
    st.write("**고객님의 제품과 시장 상황을 분석**하여 차별화된 네이밍 전략을 제시합니다.")
    st.write("---")
    st.caption("© 2050B 디자인연구소 X 레코듀. All rights reserved.")
    st.write("---")

# ----------------------------
# 3) 메인 컨텐츠
# ----------------------------
st.title("핵심 키워드 (Core Key-word) & 브랜드 네임 제안 보고서")
st.write("이 PoC 페이지는 **AI**를 활용하여, 입력된 정보를 기반으로 브랜드 네임과 보고서를 자동 생성하는 예시입니다.")

# 보고서 생성용 컨테이너
with st.container():
    st.write("---")
    st.header("1. 아이템 / 브랜드 관련 정보 입력")
    
    with st.form("brand_naming_form"):
        # 컬럼 분할로 2열씩 입력할 수 있도록 구성
        col1, col2 = st.columns(2)
        with col1:
            item_service = st.text_input("[아이템 / 서비스 종류]", "예: 콜라겐 마스크팩")
            service_type = st.text_input("[서비스의 업태와 종목]", "예: 화장품 제조 / 유통")
            competitor = st.text_input("[경쟁사 브랜드]", "예: 조여정 마스크팩, GNC팩 등")
            core_tech = st.text_input("[핵심 기술]", "예: 국내산 돼지 표피 젤라틴 추출 콜라겐")
            core_value = st.text_input("[핵심 가치]", "예: 천연, 안전성, 높은 함유량 등")
        with col2:
            main_customers = st.text_input("[주 고객층]", "예: 20~30대 여성, 피부 관리 관심층 등")
            sale_channel = st.text_input("[판매 채널]", "예: 자사몰, 면세점, 드럭스토어 등")
            ad_channel = st.text_input("[광고 / 홍보 채널]", "예: SNS, 유튜브, 블로그, TV CF 등")
            slogan = st.text_input("[슬로건 / 광고 카피]", "예: 콜라겐의 힘, 피부에 꽃피다")
            price = st.text_input("[판매 가격]", "예: 2,900원 ~ 3,500원")

        free_intro = st.text_area("[브랜드에 대한 소개 자유 기재]",
                                  "예: 합리적인 가격에, 고품질의 콜라겐 마스크팩을 제공하여 ...")

        submitted = st.form_submit_button("브랜드 보고서 생성하기")

# ----------------------------
# 4) 제출 시 GPT에게 질의
# ----------------------------
    if submitted:
        # 1) system 프롬프트
        system_prompt = """
너는 브랜드 명을 잘 만드는 마케팅 전문가야. 유저가 주는 정보를 바탕으로 "핵심 키워드(Core Key-word) & 브랜드 네임 제안 보고서"를 작성해줘.
인사는 하지 말고, 바로 Markdown 형식의 보고서를 작성해줘. 대신 ```같은 코드 블럭은 넣지 말아줘.

<example_reference>
<1. Item/Service Summary>
# 1. Item/Service Summary

'마스크팩' 키워드는 국내 포털 사이트 기준, 2018년 ~ 2024년 검색량은 하향되었지만, 새로운 브랜드와 제품이 지속적으로 출시되며 그 성분과 차별성이 다양해지고 있습니다. PC보다는 모바일 검색량이 약 7배 정도 높으며 연관 검색 되는 키워드도 다양하게 보여지고 있습니다. 검색량의 성비는 여자가 남자보다 약 3배 정도 높게 나타나고 사용 후기에 대한 관심이 크지만 체험단을 통한 블로그도 다수 발견됩니다. 최근에는 마스크팩의 성분 중 콜라겐 성분, 400달톤, 197달톤 성분 제품이 인기를 끌고 있으며, 상위 노출 브랜드로는 (조여정의 마스크팩), (GNC팩)이 있습니다. 마스크팩과 더불어 (미스트), (알로에)를 함께 검색한 이력도 볼 수 있습니다. 국외 포털 사이트 기준, 2014년 ~ 2021년 검색량 대비 2021년 ~ 2024년 검색량이 현저히 줄어든 특징을 보입니다. 마스크팩 키워드는....
마스크팩 브랜드 사업자가 줄어들고 있으며 소상공인 규모 사업자 보다는 중소/중견 기업의 사업자 수가 높아졌습니다.
</1. Item/Service Summary>

<2. Core Keyword Summary>
# 2. Core Keyword Summary

Core Keyword : 국내산 콜라겐 / 콜라겐 58 / 197달톤
1. 국내산 콜라겐
- 국내산 돼지 표피의 젤라틴 추출 콜라겐으로 만든 콜라겐 마스크팩은 유일하며, 1960년대 이후 연구 개발이 활발한 산미산업의 젤라틴 성분을 활용한 제품으로 신뢰도가 높으며 기술력이 높을 것으로 예상됩니다.

2. 콜라겐 58
- 콜라겐 성분이 전체 성분의 58%를 차지하는 많은 함량을 갖고 있음은 소비자에게 본 브랜드의 강점을 직접적으로 어필할 수 있으며, 강점을 연상하고 구전시키는 데에 큰 장점이 있는 키워드 입니다.

3. 197달톤
- 현재 상위 노출 중인 (조여정 마스크팩)이 197 달톤을 핵심 키워드로 활용하고 있으며, 광고 키 카피에도 사용하고 있으므로, 197 달톤 기술력을 표현하는  키워드는 마케팅적으로 도움이 큰 키워드입니다.
</2. Core Keyword Summary>

<3. Core Keyword Naming Chart>
# 3. Core Keyword Naming Chart

분석된 핵심 키워드들을 서비스 키워드와 핵심 키워드로 분류하여 혼합형 브랜드 네임을 제안합니다.
제안된 혼합형 브랜드 네임은 시장에서의 연상성을 높이는 카피라이팅과 함께 제안됩니다.

##서비스 키워드 + 핵심 가치 키워드 합성 네이밍##
<표1>
세로(핵심 가치 키워드) + 가로(서비스 키워드)
(  ) | 마스크팩 | 페이스 | 팩 | 마스크
콜라겐 | 콜라겐 마스크팩 | 콜라겐 페이스 | 콜라겐 팩 | 콜라겐 마스크
58% | 58 마스크팩 | 58 페이스 | 58 팩 | 58 마스크
코리아 | 코리아 마스크팩 | 코리아 페이스 | 코리아 팩 | 코리아 마스크
K | K 마스크팩 | K 페이스 | K 팩 | K 마스크
197달톤 | 197달톤 마스크팩 | 197달톤 페이스 | 197달톤 팩 | 197달톤 마스크
400달톤 | 400달톤 마스크팩 | 400달톤 페이스 | 400달톤 팩 | 400달톤 마스크
돈피 | 돈피 마스크팩 | 돈피 페이스 | 돈피 팩 | 돈피 마스크
오팔 | 오팔 마스크팩 | 오팔 페이스 | 오팔 팩 | 마스크 오팔
케이 | 케이 마스크팩 | 페이스케이 | 케이 팩 | 마스크 케이
</표1>

<표2_2core + 1service>
콜라겐+오팔 | 오팔콜라겐마스크팩
콜라겐+K | 콜라겐마스크팩K | 콜라겐K팩
</표2_2core + 1service>
</3. Core Keyword Naming Chart>

<4. Proposal 'Core Keyword Mixed, Brand Name'>
# 4. Proposal 'Core Keyword Mixed, Brand Name'

1. 오팔 마스크팩 - 키워드 : 국내산 콜라겐 / 콜라겐 58 / 197 달톤
국내산 돼지 포피의 젤라틴 추출 콜라겐으로 만든 콜라겐 마스크 팩은 유일하며, 1960년대 이후 연구 개발이 활발한 산미산업의 젤라틴 성분을 활용한 제품으로 신뢰도가 높으며 기술력이 높을 것으로 예상됩니다.
(...)

</4. Proposal 'Core Keyword Mixed, Brand Name'>
</example_reference>
"""

        # 2) user 프롬프트 (사용자 입력 내용 구성)
        user_prompt = f"""
[아이템 / 서비스 종류]
{item_service}

[서비스의 업태와 종목]
{service_type}

[경쟁사 브랜드]
{competitor}

[핵심 기술]
{core_tech}

[핵심 가치]
{core_value}

[주 고객층]
{main_customers}

[판매 채널]
{sale_channel}

[광고 / 홍보 채널]
{ad_channel}

[슬로건 / 광고 카피]
{slogan}

[판매 가격]
{price}

[브랜드에 대한 소개 자유 기재]
{free_intro}
"""

        # ----------------------------
        # 5) GPT 스트리밍 응답 처리
        # ----------------------------
        st.write("---")
        st.info("**브랜드 네임 제안 보고서를 생성하고 있습니다...** 잠시만 기다려주세요.")

        # GPT에게 streaming 모드로 요청
        response = client.chat.completions.create(
            model="o3-mini",  # 실제 사용 모델에 맞춰 조정
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            stream=True  # <- 스트리밍 활성화
        )

        st.markdown("#### **생성된 보고서**")

        # 실시간 표시를 위한 placeholder
        report_placeholder = st.empty()

        # 스트리밍 받아서 점진적으로 표시할 텍스트 누적
        generated_report = "\n\n"

        for chunk in response:
            # chunk 중 실제 응답 부분만 추출
            chunk_content = chunk.choices[0].delta.content

            if chunk_content:
                # 1) 누적
                generated_report += chunk_content

                # 2) 문자열 처리 - 줄바꿈 기호가 있을 때만 업데이트
                if '\n' in chunk_content:
                    # 3) 스트리밍 중간 상태 갱신
                    report_placeholder.markdown(
                        f"<div style='background-color:#fff; padding:1rem; border-radius:8px;'>"
                        f"{generated_report}"
                        f"</div>",
                        unsafe_allow_html=True
                    )

            time.sleep(0.01)

        print(generated_report)


        st.success("브랜드 네임 제안 보고서가 완성되었습니다!")
        st.info("※ 본 예시는 PoC 데모 용도이며, 실제 상표권 침해 여부 등은 별도로 검토가 필요합니다.")
