import streamlit as st

# =========================================================
# 페이지 설정
# =========================================================
st.set_page_config(
    page_title="필터 버블 이해하기",
    page_icon="🫧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 파스텔 디자인 시스템
# =========================================================
PASTEL = {
    "bg":        "#FAF7FF",
    "card":      "#FFFFFF",
    "lavender":  "#C7B8FF",
    "mint":      "#A8E6CF",
    "peach":     "#FFD3B6",
    "pink":      "#FFC8DD",
    "sky":       "#B5D8FA",
    "yellow":    "#FFE5A0",
    "coral":     "#FFAAA5",
    "text":      "#5B5170",
    "text_soft": "#8B82A8",
    "border":    "#EFE9F7",
    "muted":     "#D8D4E8"
}

# =========================================================
# 커스텀 CSS
# =========================================================
st.markdown(f"""
<style>
    .stApp {{ background-color: {PASTEL["bg"]}; }}
    .main .block-container {{ padding-top: 2rem; max-width: 1100px; }}

    /* 헤로 배너 */
    .main-hero {{
        background: linear-gradient(135deg, #FFC8DD 0%, #C7B8FF 50%, #B5D8FA 100%);
        padding: 40px 36px;
        border-radius: 24px;
        margin-bottom: 28px;
        text-align: center;
    }}
    .main-hero .badge {{
        display: inline-block;
        background: rgba(255,255,255,0.4);
        color: white;
        font-size: 12px; font-weight: 700;
        padding: 6px 14px;
        border-radius: 12px;
        margin-bottom: 14px;
        letter-spacing: 1px;
    }}
    .main-hero h1 {{
        color: white !important;
        font-size: 34px; font-weight: 800;
        margin: 0 0 12px 0;
        letter-spacing: -1px;
    }}
    .main-hero p {{
        color: rgba(255,255,255,0.95);
        font-size: 15px;
        margin: 0; line-height: 1.7;
        max-width: 700px;
        margin-left: auto; margin-right: auto;
    }}

    /* 섹션 타이틀 */
    .section-title {{
        font-size: 22px; font-weight: 700;
        color: {PASTEL["text"]};
        margin: 28px 0 16px 0;
        letter-spacing: -0.5px;
        display: flex; align-items: center; gap: 10px;
    }}
    .section-title::before {{
        content: "";
        display: inline-block;
        width: 4px; height: 22px;
        background: {PASTEL["lavender"]};
        border-radius: 2px;
    }}

    /* 카드 */
    .concept-card {{
        background: {PASTEL["card"]};
        border: 1px solid {PASTEL["border"]};
        border-radius: 18px;
        padding: 24px 26px;
        margin-bottom: 16px;
        height: 100%;
    }}
    .concept-card .card-icon {{
        font-size: 32px; margin-bottom: 10px;
    }}
    .concept-card .card-title {{
        font-size: 17px; font-weight: 700;
        color: {PASTEL["text"]};
        margin-bottom: 8px;
    }}
    .concept-card .card-desc {{
        font-size: 13px; color: {PASTEL["text_soft"]};
        line-height: 1.7;
    }}

    /* 정의 카드 (강조) */
    .definition-card {{
        background: {PASTEL["card"]};
        border: 1px solid {PASTEL["border"]};
        border-left: 6px solid {PASTEL["lavender"]};
        border-radius: 16px;
        padding: 22px 26px;
        margin-bottom: 16px;
    }}
    .definition-card .term {{
        font-size: 13px; font-weight: 700;
        color: {PASTEL["lavender"]};
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }}
    .definition-card .term-ko {{
        font-size: 20px; font-weight: 700;
        color: {PASTEL["text"]};
        margin-bottom: 10px;
    }}
    .definition-card .term-def {{
        font-size: 14px; color: {PASTEL["text"]};
        line-height: 1.8;
    }}
    .definition-card .term-source {{
        font-size: 11px; color: {PASTEL["text_soft"]};
        margin-top: 10px;
        font-style: italic;
    }}

    /* 원리 단계 카드 */
    .step-card {{
        background: {PASTEL["card"]};
        border: 1px solid {PASTEL["border"]};
        border-radius: 16px;
        padding: 20px 22px;
        margin-bottom: 12px;
        position: relative;
    }}
    .step-card .step-num {{
        display: inline-block;
        width: 32px; height: 32px;
        background: {PASTEL["lavender"]};
        color: white;
        border-radius: 10px;
        text-align: center;
        line-height: 32px;
        font-weight: 700; font-size: 14px;
        margin-right: 10px;
    }}
    .step-card .step-title {{
        font-size: 16px; font-weight: 700;
        color: {PASTEL["text"]};
        display: inline-block;
        vertical-align: middle;
    }}
    .step-card .step-desc {{
        font-size: 13px; color: {PASTEL["text_soft"]};
        line-height: 1.7;
        margin-top: 10px;
        padding-left: 42px;
    }}

    /* ✅ 위험성 카드 - 높이 통일 (flexbox + min-height) */
    .danger-card {{
        background: {PASTEL["card"]};
        border: 1px solid {PASTEL["border"]};
        border-radius: 16px;
        padding: 20px 22px;
        margin-bottom: 14px;
        min-height: 175px;
        display: flex;
        flex-direction: column;
    }}
    .danger-card .danger-icon {{
        font-size: 28px; margin-bottom: 8px;
    }}
    .danger-card .danger-title {{
        font-size: 15px; font-weight: 700;
        color: {PASTEL["text"]};
        margin-bottom: 6px;
    }}
    .danger-card .danger-desc {{
        font-size: 13px; color: {PASTEL["text_soft"]};
        line-height: 1.6;
        flex-grow: 1;
    }}

    /* 사례 카드 */
    .case-card {{
        background: {PASTEL["card"]};
        border: 1px solid {PASTEL["border"]};
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 10px;
    }}
    .case-card .case-platform {{
        font-size: 11px; font-weight: 700;
        letter-spacing: 0.5px;
        padding: 3px 10px;
        border-radius: 8px;
        display: inline-block;
        margin-bottom: 8px;
    }}
    .case-card .case-text {{
        font-size: 13px; color: {PASTEL["text"]};
        line-height: 1.7;
    }}

    /* 관련 개념 카드 */
    .related-card {{
        background: {PASTEL["card"]};
        border: 1px solid {PASTEL["border"]};
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 12px;
    }}
    .related-card .rel-title {{
        font-size: 15px; font-weight: 700;
        color: {PASTEL["text"]};
        margin-bottom: 6px;
    }}
    .related-card .rel-desc {{
        font-size: 13px; color: {PASTEL["text_soft"]};
        line-height: 1.6;
    }}

    /* 수업 흐름 카드 */
    .flow-card {{
        background: {PASTEL["card"]};
        border: 2px solid {PASTEL["border"]};
        border-radius: 18px;
        padding: 22px 24px;
        text-align: center;
        height: 100%;
        transition: all 0.2s ease;
    }}
    .flow-card.step1 {{ border-color: {PASTEL["pink"]}; }}
    .flow-card.step2 {{ border-color: {PASTEL["sky"]}; }}
    .flow-card.step3 {{ border-color: {PASTEL["mint"]}; }}
    .flow-card .flow-num {{
        font-size: 11px; font-weight: 700;
        color: {PASTEL["text_soft"]};
        letter-spacing: 1px;
    }}
    .flow-card .flow-emoji {{
        font-size: 40px;
        margin: 8px 0;
    }}
    .flow-card .flow-title {{
        font-size: 16px; font-weight: 700;
        color: {PASTEL["text"]};
        margin-bottom: 6px;
    }}
    .flow-card .flow-desc {{
        font-size: 12px; color: {PASTEL["text_soft"]};
        line-height: 1.6;
    }}

    /* 인용구 */
    .quote-box {{
        background: linear-gradient(135deg, #FFF7E6 0%, #FFE5A0 100%);
        border-radius: 18px;
        padding: 24px 28px;
        margin: 20px 0;
        text-align: center;
    }}
    .quote-box .quote-mark {{
        font-size: 36px;
        color: rgba(91, 81, 112, 0.3);
        line-height: 1;
    }}
    .quote-box .quote-text {{
        font-size: 16px;
        color: {PASTEL["text"]};
        font-weight: 600;
        line-height: 1.6;
        margin: 6px 0;
    }}
    .quote-box .quote-author {{
        font-size: 12px;
        color: {PASTEL["text_soft"]};
        margin-top: 8px;
    }}

    /* 체크리스트 */
    .check-item {{
        background: {PASTEL["card"]};
        border: 1px solid {PASTEL["border"]};
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 8px;
        font-size: 13px;
        color: {PASTEL["text"]};
        line-height: 1.6;
    }}
    .check-item .check-mark {{
        color: {PASTEL["mint"]};
        font-weight: 700;
        margin-right: 8px;
    }}

    /* 버튼 */
    .stButton > button {{
        border-radius: 14px;
        font-weight: 700; font-size: 14px;
        border: 1.5px solid {PASTEL["border"]};
        background: {PASTEL["card"]};
        color: {PASTEL["text"]};
        padding: 12px 20px;
        transition: all 0.2s ease;
    }}
    .stButton > button:hover {{
        background: #FAF5FF;
        border-color: {PASTEL["lavender"]};
        color: {PASTEL["text"]};
    }}
    .stButton > button[kind="primary"] {{
        background: {PASTEL["lavender"]};
        color: white;
        border: none;
    }}
    .stButton > button[kind="primary"]:hover {{
        background: #B0A0F5;
        color: white;
    }}

    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
        background: transparent;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: {PASTEL["card"]};
        border-radius: 12px 12px 0 0;
        padding: 10px 18px;
        font-weight: 600;
        color: {PASTEL["text_soft"]};
    }}
    .stTabs [aria-selected="true"] {{
        background: {PASTEL["lavender"]} !important;
        color: white !important;
    }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 헤로
# =========================================================
st.markdown("""
<div class="main-hero">
  <span class="badge">DIGITAL LITERACY · AI ETHICS</span>
  <h1>🫧 알고리즘이 만든<br>나만의 작은 세상</h1>
  <p>매일 보는 유튜브 추천, SNS 피드, 뉴스 화면···<br>
  우리는 어쩌면 알고리즘이 만든 '거품' 속에 살고 있을지도 몰라요.<br>
  필터 버블이 무엇이고 왜 중요한지, 함께 이해해 봅시다.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 1) 필터 버블이란?
# =========================================================
st.markdown('<div class="section-title">📖 필터 버블이란 무엇일까요?</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="definition-card">
  <div class="term">FILTER BUBBLE</div>
  <div class="term-ko">필터 버블 (Filter Bubble)</div>
  <div class="term-def">
    인터넷 사용자의 검색 기록·클릭·시청 패턴을 학습한 알고리즘이,
    <b>사용자가 좋아할 만한 정보만 선별해 보여주는 현상</b>이에요.
    그 결과 우리는 자신도 모르는 사이에 <b>한쪽 시각의 정보만 보게 되는 투명한 거품</b> 속에 갇히게 됩니다.
  </div>
  <div class="term-source">— 엘리 프레이저(Eli Pariser), 『The Filter Bubble』(2011)</div>
</div>
""", unsafe_allow_html=True)

# 인용구
st.markdown("""
<div class="quote-box">
  <div class="quote-mark">"</div>
  <div class="quote-text">알고리즘은 우리에게 보여주고 싶은 것을 보여줍니다.<br>
  하지만 우리가 봐야 할 것을 보여주지는 않습니다.</div>
  <div class="quote-author">— Eli Pariser, TED 2011</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 2) 왜 만들어질까?
# =========================================================
st.markdown('<div class="section-title">⚙️ 필터 버블은 어떻게 만들어질까요?</div>', unsafe_allow_html=True)
st.markdown(f"""
<p style="font-size:14px; color:{PASTEL['text_soft']}; margin-bottom:18px;">
알고리즘이 우리를 거품 속에 가두는 과정은 4단계로 일어납니다.
</p>
""", unsafe_allow_html=True)

steps = [
    ("데이터 수집", "내가 클릭한 영상, 검색한 단어, 머문 시간, 좋아요 누른 게시물까지 — 거의 모든 행동이 데이터로 기록됩니다."),
    ("취향 분석", "AI는 이 데이터를 분석해 '이 사람은 어떤 분야를 좋아하는지'에 대한 프로필을 만듭니다."),
    ("맞춤 추천", "분석된 취향에 맞는 콘텐츠를 우선적으로 화면에 띄워줍니다. 클릭률이 높아지고 체류 시간이 늘어납니다."),
    ("버블 강화", "맞춤 콘텐츠를 더 많이 클릭할수록 AI는 더 확신을 갖고, 추천 폭은 점점 좁아지며 결국 다른 시각은 사라집니다.")
]

for i, (title, desc) in enumerate(steps, 1):
    st.markdown(f"""
    <div class="step-card">
      <span class="step-num">{i}</span>
      <span class="step-title">{title}</span>
      <div class="step-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# 3) 왜 위험할까? (✅ 카드 높이 통일)
# =========================================================
st.markdown('<div class="section-title">⚠️ 필터 버블이 왜 위험할까요?</div>', unsafe_allow_html=True)

dangers = [
    ("🎭", "확증 편향 강화", "내 생각과 비슷한 정보만 보다 보면, 내 의견이 절대 옳다고 믿게 됩니다."),
    ("🌫️", "정보 사각지대", "중요한 사회·정치·과학 이슈가 내 눈에는 보이지 않게 가려질 수 있어요."),
    ("🔥", "극단화 가속", "자극적이고 분노를 유발하는 콘텐츠가 더 많이 노출되어 사고가 극단으로 흐릅니다."),
    ("🧩", "사회 분열", "사람마다 다른 정보를 보게 되어, 공동의 대화와 토론이 어려워집니다."),
    ("🤖", "자율성 상실", "알고리즘이 정해주는 대로 보게 되어, 스스로 정보를 탐색하는 능력이 약해져요."),
    ("💸", "상업적 이용", "내 취향 데이터가 광고와 마케팅에 활용되어, 소비 결정도 조작될 수 있습니다.")
]

dcol1, dcol2, dcol3 = st.columns(3, gap="medium")
for i, (icon, title, desc) in enumerate(dangers):
    target = [dcol1, dcol2, dcol3][i % 3]
    with target:
        st.markdown(f"""
        <div class="danger-card">
          <div class="danger-icon">{icon}</div>
          <div class="danger-title">{title}</div>
          <div class="danger-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# 4) 실제 사례 (탭)
# =========================================================
st.markdown('<div class="section-title">🌍 우리 주변의 실제 사례</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📺 YouTube", "📱 SNS", "🛒 쇼핑", "📰 뉴스"])

with tab1:
    st.markdown(f"""
    <div class="case-card">
      <span class="case-platform" style="background:#FEE2E2; color:#9F1239;">YOUTUBE</span>
      <div class="case-text">
        축구 영상 하나를 클릭하면 다음 추천이 모두 축구로 채워집니다.
        해외 연구에 따르면 유튜브 추천 알고리즘은 사용자를
        <b>점점 더 자극적·극단적인 콘텐츠로 유도</b>하는 경향이 있다고 보고됐어요(Mozilla, 2021).
        '토끼 굴(Rabbit Hole) 효과'라고도 불립니다.
      </div>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown(f"""
    <div class="case-card">
      <span class="case-platform" style="background:#FCE7F3; color:#9D174D;">INSTAGRAM · TIKTOK</span>
      <div class="case-text">
        SNS 피드는 내가 오래 보거나 좋아요를 누른 게시물의 비중을 폭발적으로 늘립니다.
        그 결과 <b>같은 또래·같은 성향의 게시물만 보이는 '에코 챔버(메아리 방)'</b>가 만들어져,
        다양한 가치관에 대한 노출이 급격히 줄어듭니다.
      </div>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown(f"""
    <div class="case-card">
      <span class="case-platform" style="background:#E0E7FF; color:#4338CA;">AMAZON · COUPANG</span>
      <div class="case-text">
        쇼핑몰은 내 검색·구매 기록을 바탕으로 추천 상품을 띄웁니다.
        편리해 보이지만, <b>다른 브랜드·다른 가격대의 상품을 비교할 기회가 줄어들고</b>
        결국 알고리즘이 정해준 좁은 선택지 안에서만 구매하게 됩니다.
      </div>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.markdown(f"""
    <div class="case-card">
      <span class="case-platform" style="background:#D1FAE5; color:#065F46;">NEWS PORTAL</span>
      <div class="case-text">
        포털 뉴스는 내가 자주 클릭한 분야·논조의 기사를 상단에 배치합니다.
        진보 성향 기사를 자주 읽는 사람과 보수 성향 기사를 자주 읽는 사람은
        <b>같은 사건에 대해 완전히 다른 뉴스 화면</b>을 보게 됩니다. 같은 나라에 살아도 다른 세상을 보는 셈이죠.
      </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# 5) 관련 개념
# =========================================================
st.markdown('<div class="section-title">🔗 함께 알면 좋은 개념들</div>', unsafe_allow_html=True)

rcol1, rcol2 = st.columns(2, gap="medium")
with rcol1:
    st.markdown(f"""
    <div class="related-card">
      <div class="rel-title">🎯 확증 편향 (Confirmation Bias)</div>
      <div class="rel-desc">
        자신의 신념과 일치하는 정보만 받아들이고, 반대 정보는 무시하는 인지 경향.
        필터 버블이 이를 더욱 강화시켜요.
      </div>
    </div>
    <div class="related-card">
      <div class="rel-title">🔊 에코 챔버 (Echo Chamber)</div>
      <div class="rel-desc">
        같은 의견을 가진 사람들끼리만 소통하며 그 의견이 점점 더 강해지는 '메아리 방' 현상.
        SNS에서 가장 흔히 나타납니다.
      </div>
    </div>
    """, unsafe_allow_html=True)

with rcol2:
    st.markdown(f"""
    <div class="related-card">
      <div class="rel-title">📚 디지털 리터러시 (Digital Literacy)</div>
      <div class="rel-desc">
        디지털 정보를 비판적으로 분석하고, 출처를 검증하며, 책임감 있게 활용하는 능력.
        필터 버블 시대의 핵심 역량이에요.
      </div>
    </div>
    <div class="related-card">
      <div class="rel-title">⚖️ 알고리즘 윤리 (Algorithmic Ethics)</div>
      <div class="rel-desc">
        AI와 추천 시스템이 사회에 미치는 영향을 윤리적으로 고민하고,
        공정하고 투명한 알고리즘을 설계하려는 노력입니다.
      </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# 6) 탈출 체크리스트
# =========================================================
st.markdown('<div class="section-title">🛡️ 필터 버블 탈출 체크리스트</div>', unsafe_allow_html=True)
st.markdown(f"""
<p style="font-size:14px; color:{PASTEL['text_soft']}; margin-bottom:14px;">
일상에서 실천할 수 있는 작은 습관들이에요. 평소에 몇 가지나 하고 있는지 확인해 보세요.
</p>
""", unsafe_allow_html=True)

checks = [
    "주기적으로 검색 기록과 쿠키를 삭제한다",
    "시크릿(인코그니토) 모드로 정보를 검색해 본다",
    "내 의견과 다른 매체·관점의 콘텐츠도 의도적으로 찾아본다",
    "한 플랫폼만 쓰지 않고 여러 정보원을 비교한다",
    "기사·영상의 출처와 작성 의도를 한 번 더 확인한다",
    "추천된 콘텐츠를 클릭하기 전, '이게 정말 내가 원한 정보인가?' 잠시 생각한다"
]

ccol1, ccol2 = st.columns(2, gap="medium")
for i, c in enumerate(checks):
    target = ccol1 if i % 2 == 0 else ccol2
    with target:
        st.markdown(f"""
        <div class="check-item">
          <span class="check-mark">✓</span>{c}
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# 7) 수업 흐름 안내 (✅ 순서: 체험 → 지도 → 퀴즈)
# =========================================================
st.markdown('<div class="section-title">🚀 이제 직접 체험해 봐요</div>', unsafe_allow_html=True)
st.markdown(f"""
<p style="font-size:14px; color:{PASTEL['text_soft']}; margin-bottom:18px;">
개념을 이해했다면, 이제 알고리즘이 어떻게 나만의 거품을 만드는지 직접 체험해 볼 시간이에요.<br>
아래 3단계를 순서대로 진행해 보세요.
</p>
""", unsafe_allow_html=True)

f1, f2, f3 = st.columns(3, gap="medium")
with f1:
    st.markdown("""
    <div class="flow-card step1">
      <div class="flow-num">STEP 01</div>
      <div class="flow-emoji">🫧</div>
      <div class="flow-title">버블 체험하기</div>
      <div class="flow-desc">
        마음에 드는 기사를 클릭하면서<br>
        나만의 필터 버블이<br>
        만들어지는 과정을 관찰해요
      </div>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="flow-card step2">
      <div class="flow-num">STEP 02</div>
      <div class="flow-emoji">🗺️</div>
      <div class="flow-title">나의 버블 지도</div>
      <div class="flow-desc">
        네트워크 그래프로<br>
        내 정보 소비 패턴을<br>
        한눈에 확인해요
      </div>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="flow-card step3">
      <div class="flow-num">STEP 03</div>
      <div class="flow-emoji">🧠</div>
      <div class="flow-title">AI 윤리 퀴즈</div>
      <div class="flow-desc">
        체험 데이터를 바탕으로<br>
        맞춤형 퀴즈를 풀며<br>
        개념을 점검해요
      </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ✅ 이동 버튼 (순서: 체험 → 지도 → 퀴즈, 경로 수정)
b1, b2, b3 = st.columns(3, gap="medium")
with b1:
    if st.button("🫧 1단계 · 버블 체험 시작하기", type="primary", use_container_width=True):
        st.switch_page("pages/bubble2.py")
with b2:
    if st.button("🗺️ 2단계 · 지도로 이동", use_container_width=True):
        st.switch_page("pages/map.py")
with b3:
    if st.button("🧠 3단계 · 퀴즈로 이동", use_container_width=True):
        st.switch_page("pages/quiz.py")

# =========================================================
# 푸터
# =========================================================
st.write("")
st.markdown(f"""
<div style="text-align:center; padding: 30px 0 20px 0;
            color:{PASTEL['text_soft']}; font-size:12px; line-height:1.8;
            border-top: 1px solid {PASTEL['border']}; margin-top: 30px;">
  <b style="color:{PASTEL['text']};">🎓 디지털 리터러시 학습 프로그램</b><br>
  필터 버블 · 확증 편향 · 추천 알고리즘 윤리 · AI 사회적 영향<br>
  <span style="font-size:11px;">알고리즘을 이해하는 시민만이 알고리즘에 휘둘리지 않습니다.</span>
</div>
""", unsafe_allow_html=True)
