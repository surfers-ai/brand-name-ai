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
            item_service = st.text_input("[아이템 / 서비스 종류]", "예: 프리미엄 수제 디퓨저 & 캔들")
            service_type = st.text_input("[서비스의 업태와 종목]", "예: 도소매 / 생활용품, 인테리어 소품")
            competitor = st.text_input("[경쟁사 브랜드]", "예: 양키캔들, 바이레도, 딥디크")
            core_tech = st.text_input("[핵심 기술]", "예: 천연 에센셜 오일 블렌딩, 지속력 강화 기술, 친환경 용기 사용")
            core_value = st.text_input("[핵심 가치]", "예: 고급스러운 향, 감성적인 디자인, 친환경 지속 가능성")
        with col2:
            main_customers = st.text_input("[주 고객층]", "예: 20 ~ 40대 여성, 홈 인테리어 관심층, 선물 구매 고객")
            sale_channel = st.text_input("[판매 채널]", "예: 공식 홈페이지, 네이버 스마트스토어, 카카오톡 선물하기, 플리마켓")
            ad_channel = st.text_input("[광고 / 홍보 채널]", "예: 인스타그램, 유튜브, 네이버 블로그, 뷰티 & 인테리어 인플루언서 협업")
            slogan = st.text_input("[슬로건 / 광고 카피]", "예: 공간에 향을 더하다, 감성을 채우다.")
            price = st.text_input("[판매 가격]", "예: 디퓨저 29,000원, 캔들 35,000원, 기프트 세트 59,000원")

        free_intro = st.text_area("[브랜드에 대한 소개 자유 기재]",
                                  "예: 우리 브랜드는 향을 통해 감성을 전달하는 프리미엄 라이프스타일 브랜드입니다. 천연 에센셜 오일과 지속 가능한 친환경 원료를 사용하여, 몸과 마음을 편안하게 만들어주는 고급스러운 디퓨저와 캔들을 제작합니다. 심플하고 세련된 디자인으로 어떤 공간에도 어울리며, 선물용으로도 손색없는 제품을 제공합니다. 향기를 통해 일상의 작은 행복을 선물하는 것이 우리의 목표입니다.")

        submitted = st.form_submit_button("브랜드 보고서 생성하기")

# ----------------------------
# 4) 제출 시 GPT에게 질의
# ----------------------------
    if submitted:
        # 1) system 프롬프트
        system_prompt = """
너는 브랜드 명을 잘 만드는 마케팅 전문가야. 유저가 주는 정보를 바탕으로 "핵심 키워드(Core Key-word) & 브랜드 네임 제안 보고서"를 작성해줘.
인사는 하지 말고, 바로 Markdown 형식의 보고서를 작성해줘. 대신 ```같은 코드 블럭은 넣지 말아줘.

<Guideline>
<1. Item/Service Summary>
- 길고 구체화할 것
- 보편적 욕구에 호소할 것
- 핵심 메시지와 브랜드 이름과 마케팅의 성공 가능성에 초점을 둘 것
- 설명이 쉬운 단어 선택으로 즉각 이해 가능할 것 (대중이 바로 와닿아야 함)
- 관련 산업의 전망과 분석도 담을 것
</1. Item/Service Summary>

<2. Core Keyword Summary>
- 핵심 키워드는 최소 5개 이상 뽑고, 부가 설명까지 적어줘.
</ 2. Core Keyword Summary>

<3. Core Keyword Naming Chart>
분석된 핵심 키워드를 바탕으로 서비스 키워드와 핵심 키워드로 분류해 혼합형 브랜드 네임을 제안해줘. 제안된 혼합형 브랜드 네임은 시장에서의 연상성을 높이는 카피라이팅도 함께 제안해줘.

이때 참고 자료와 같은 표를 사용해줘.
- Row(핵심 가치 키워드) + Column(서비스 키워드)
- Row : 핵심 가치 키워드
- Column : 서비스 키워드
- 표 내용은 서비스 키워드와 핵심 가치 키워드가 각각 합성된 형태를 띄울 것(예: 콜라겐 + 마스크팩 -> 콜라겐 마스크팩, 197달톤 + 페이스 -> 197달톤 페이스, 베르데 + 캔들 -> 베르데 캔들)
- 조합할 때, 합성 네이밍이 마케팅에 도움이 되게끔 조합할 것
- 서비스 키워드와 핵심 가치 키워드가 뻔하지 않게 할 것
- 이 때, row의 마지막 부분에 핵심 가치 2개를 조합한 키워드 또한 2-3개 정도 포함할 것 (콜라겐+오팔, 콜라겐+K 등)
</3. Core Keyword Naming Chart>

<4. Proposal 'Core Keyword Mixed, Brand Name'>
generate_3. Core Keyword Naming Chart 중에서 마케팅으로 성공할 수 있는 브랜드 네이밍을 3개 이상 선정해줘. 그리고 너가 추천하는 브랜드 네이밍 2개를 추천해줘. 그렇게 5개의 브랜드 네이밍을 가지고, 각각 배경과 선정 사유, 마케팅 성공 가능성 등을 포함해서 분석해줘.

- KIPRIS 또는 이미 사용하고 있는 브랜드 이름은 선정할 때 제외해줘.
- 브랜드 이름은 참신하고 기억하기 쉽게 할 것
- 설명은 길고 구체화할 것
- 보편적 욕구에 호소할 것
- 핵심 메시지와 브랜드 이름과 마케팅의 성공 가능성에 초점을 둘 것
- 설명이 쉬운 단어 선택으로 즉각 이해 가능할 것 (대중이 바로 와닿아야 함)
- 관련 브랜드 명의 전망과 분석도 담을 것
</4. Proposal 'Core Keyword Mixed, Brand Name'>
</Guideline>

<example_reference1>
<1. Item/Service Summary>
# 1. Item/Service Summary

'마스크팩' 키워드는 국내 포털 사이트 기준, 2018년 ~ 2024년 검색량은 하향되었지만, 새로운 브랜드와 제품이 지속적으로 출시되며 그 성분과 차별성이 다양해지고 있습니다.
PC보다는 모바일 검색량이 약 7배 정도 높으며 연관 검색 되는 키워드도 다양하게 보여지고 있습니다. 검색량의 성비는 여자가 남자보다 약 3배 정도 높게 나타나고 사용 후기에 대한 관심이 크지만 체험단을 통한 블로그도 다수 발견됩니다.
최근에는 마스크팩의 성분 중 콜라겐 성분, 400달톤, 197달톤 성분 제품이 인기를 끌고 있으며, 상위 노출 브랜드로는 (조여정의 마스크팩), (GNC팩)이 있습니다. 마스크팩과 더불어 (미스트), (알로에)를 함께 검색한 이력도 볼 수 있습니다.
국내외 뷰티 트렌드에서는 '클린 뷰티', '내추럴 성분' 및 '피부 본연의 건강 회복'에 대한 관심이 증대되고 있습니다. 이에 따라 자사몰, 면세점, 드럭스토어 등 다양한 판매 채널과 SNS, 유튜브, 블로그, TV CF 등의 광고 채널을 통해 소비자에게 친근하면서도 전문성 있는 이미지를 전달할 수 있습니다.
경쟁사인 조여정 마스크팩, GNC팩 등과 차별화하기 위해 국내산 콜라겐의 기술적 우수성과 천연·안전성 기반의 브랜드 스토리를 효과적으로 전달한다면, 시장 내 강한 연상 효과와 고객 신뢰도를 상승시킬 수 있을 것으로 기대됩니다.
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

<Table>
|                 | 마스크팩             | 페이스              | 팩               | 마스크              |
|-----------------|---------------------|--------------------|-----------------|--------------------|
| 콜라겐          | 콜라겐 마스크팩      | 콜라겐 페이스       | 콜라겐 팩        | 콜라겐 마스크       |
| 58%             | 58 마스크팩          | 58 페이스           | 58 팩            | 58 마스크           |
| 코리아          | 코리아 마스크팩      | 코리아 페이스       | 코리아 팩        | 코리아 마스크       |
| K               | K 마스크팩           | K 페이스            | K 팩             | K 마스크            |
| 197달톤         | 197달톤 마스크팩     | 197달톤 페이스      | 197달톤 팩       | 197달톤 마스크      |
| 400달톤         | 400달톤 마스크팩     | 400달톤 페이스      | 400달톤 팩       | 400달톤 마스크      |
| 돈피            | 돈피 마스크팩        | 돈피 페이스         | 돈피 팩          | 돈피 마스크         |
| 오팔            | 오팔 마스크팩        | 오팔 페이스         | 오팔 팩          | 오팔 마스크         |
| 케이            | 케이 마스크팩        | 케이 페이스         | 케이 팩          | 케이 마스크         |
| 콜라겐 + 오팔   | 오팔 콜라겐 마스크팩 | 오팔 콜라겐 페이스  | 오팔 콜라겐 팩   | 오팔 콜라겐 마스크  |
| 콜라겐 + K      | 콜라겐 K 마스크팩    | 콜라겐 K 페이스     | 콜라겐 K 팩      | 콜라겐 K 마스크     |
</Table>

</3. Core Keyword Naming Chart>

<4. Proposal 'Core Keyword Mixed, Brand Name'>
# 4. Proposal 'Core Keyword Mixed, Brand Name'

1. **오팔 마스크팩** - 키워드 : 국내산 콜라겐 / 콜라겐 58 / 197 달톤
국내산 돼지 포피의 젤라틴 추출 콜라겐으로 만든 콜라겐 마스크 팩은 유일하며, 1960년대 이후 연구 개발이 활발한 산미산업의 젤라틴 성분을 활용한 제품으로 신뢰도가 높으며 기술력이 높을 것으로 예상됩니다.

2. **197달톤 마스크팩** - 키워드 : 197달톤 / 국내산 콜라겐 / 고흡수
- 197달톤은 피부 흡수에 최적화된 저분자 콜라겐의 크기를 뜻하며, 피부 깊숙이 빠르게 흡수되어 즉각적인 보습 효과와 탄력 개선 효과를 기대할 수 있습니다. 특히 국내산 프리미엄 콜라겐을 사용하여 품질과 안전성을 강조한 제품으로 소비자의 신뢰를 얻기에 적합합니다. 최근 소비자들이 화장품 성분과 흡수력에 큰 관심을 보이는 트렌드를 고려할 때, 이 브랜드 네임은 직관적이고 전문적인 이미지를 제공하여 마케팅 성공 가능성이 높습니다.

(...)

</4. Proposal 'Core Keyword Mixed, Brand Name'>
</example_reference1>

<example_reference2>
<1. Item/Service Summary>
# 1. Item/Service Summary

최근 프리미엄 디퓨저와 캔들 시장은 고급스러운 향과 감성적인 디자인을 추구하는 20 ~ 40대 여성 소비자를 중심으로 지속적인 성장세를 보이고 있습니다.
특히 천연 에센셜 오일 블렌딩, 지속력 강화 기술, 친환경 용기 사용 등 친환경 지속 가능성을 강조하는 제품들이 인기를 얻고 있습니다.
기존 브랜드 중에서는 양키캔들, 바이레도, 딥디크가 높은 인지도를 유지하며 프리미엄 시장을 주도하고 있습니다.
공식 홈페이지, 네이버 스마트스토어, 카카오톡 선물하기 등 온라인 플랫폼뿐만 아니라 플리마켓을 통해 오프라인 고객과의 접점도 확보하고 있으며, 인스타그램과 유튜브, 네이버 블로그를 중심으로 뷰티 및 인테리어 인플루언서와 협업하여 브랜드 인지도를 확대하고 있습니다.
</1. Item/Service Summary>

<2. Core Keyword Summary>
# 2. Core Keyword Summary

Core Keyword : 천연 에센셜 오일 / 지속력 강화 기술 / 친환경

1. 천연 에센셜 오일
- 순수한 천연 에센셜 오일을 블렌딩하여 자연스러운 향을 제공하며, 신체와 정신의 안정감을 중시하는 소비자에게 강력한 구매 요인이 됩니다.

2. 지속력 강화 기술
- 향기의 지속력을 극대화하는 독자적 기술을 통해 일반 제품과의 명확한 차별성을 제공하며, 지속적이고 프리미엄한 향기 경험을 원하는 소비자층에게 매력적입니다.

3. 친환경 지속 가능성
- 친환경 소재와 지속 가능한 생산 방식을 활용하여 환경 보호에 대한 소비자의 니즈를 충족시키고, 브랜드 이미지와 신뢰도를 높이는 데 기여합니다.
</2. Core Keyword Summary>

<3. Core Keyword Naming Chart>
# 3. Core Keyword Naming Chart

<Table>
|                   | 디퓨저              | 캔들              | 센트             | 아로마             |
|-------------------|--------------------|-------------------|------------------|--------------------|
| 천연              | 천연 디퓨저         | 천연 캔들         | 천연 센트        | 천연 아로마        |
| 에센셜            | 에센셜 디퓨저       | 에센셜 캔들       | 에센셜 센트      | 에센셜 아로마      |
| 친환경            | 친환경 디퓨저       | 친환경 캔들       | 친환경 센트      | 친환경 아로마      |
| 블룸              | 블룸 디퓨저         | 블룸 캔들         | 블룸 센트        | 블룸 아로마        |
| 지속력            | 지속력 디퓨저       | 지속력 캔들       | 지속력 센트      | 지속력 아로마      |
| 오르다            | 오르다 디퓨저       | 오르다 캔들       | 오르다 센트      | 오르다 아로마      |
| 베르데            | 베르데 디퓨저       | 베르데 캔들       | 베르데 센트      | 베르데 아로마      |
| 에센셜 + 오르다   | 에센셜 오르다 디퓨저 | 에센셜 오르다 캔들 | 에센셜 오르다 센트 | 에센셜 오르다 아로마 |
| 블룸 + 에센셜     | 블룸 에센셜 디퓨저   | 블룸 에센셜 캔들   | 블룸 에센셜 센트  | 블룸 에센셜 아로마   |
</Table>
</3. Core Keyword Naming Chart>

<4. Proposal 'Core Keyword Mixed, Brand Name'>
# 4. Proposal 'Core Keyword Mixed, Brand Name'

1. **블룸 센트 (Bloom Scent)** - 키워드 : 천연 에센셜 오일 / 지속력 강화 기술 / 친환경
- 꽃이 피어나듯 자연스럽고 깊이 있는 향기 경험을 제공하는 브랜드입니다. 천연 원료 사용과 지속 가능한 생산 방식을 통해 친환경 라이프스타일을 추구하는 고객에게 어필하며, 향기를 통해 일상의 행복과 감성을 전달합니다.

2. **베르데 아로마 (Verde Aroma)** - 키워드 : 친환경 지속 가능성 / 천연 에센셜 오일
- '베르데(Verde)'는 이탈리아어로 '초록색'을 뜻하며, 친환경적인 요소를 직관적으로 나타냅니다. 천연 에센셜 오일의 신선한 향을 강조하여 자연과 조화를 이루는 편안한 공간을 선사합니다.

(...)
</4. Proposal 'Core Keyword Mixed, Brand Name'>
</example_reference2>
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
            model="gpt-4.5-preview-2025-02-27",  # 실제 사용 모델에 맞춰 조정
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

                # 2) 문자열 처리 (현재 특별한 전처리 없음)

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
