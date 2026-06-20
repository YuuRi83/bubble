import streamlit as st
import random

# =========================================================
# 페이지 설정
# =========================================================
st.set_page_config(
    page_title="AI 윤리 퀴즈",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 파스텔 디자인 시스템
# =========================================================
PASTEL = {
    "bg":        "#FFFBF5",   # 따뜻한 크림
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
    "muted":     "#D8D4E8",
    "correct":   "#A8E6CF",
    "wrong":     "#FFAAA5"
}

CAT_ICONS = {
    "스포츠": "⚽", "정치": "🗳️", "게임": "🎮",
    "연예": "🎤", "사건사고": "🚨", "교육": "📚"
}
categories = ["스포츠", "정치", "게임", "연예", "사건사고", "교육"]

# =========================================================
# 커스텀 CSS
# =========================================================
st.markdown(f"""
<style>
    .stApp {{ background-color: {PASTEL["bg"]}; }}
    .main .block-container {{ padding-top: 2rem; max-width: 900px; }}

    /* 헤로 */
    .quiz-hero {{
        background: linear-gradient(135deg, #FFE5A0 0%, #FFD3B6 50%, #FFC8DD 100%);
        padding: 28px 32px;
        border-radius: 20px;
        margin-bottom: 24px;
        border: 1px solid {PASTEL["border"]};
    }}
    .quiz-hero h1 {{
        color: {PASTEL["text"]} !important;
        font-size: 26px; font-weight: 700; margin: 0 0 8px 0;
        letter-spacing: -0.5px;
    }}
    .quiz-hero p {{
        color: {PASTEL["text"]}; font-size: 14px;
        margin: 0; line-height: 1.6; opacity: 0.85;
    }}

    /* 카드 */
    .pastel-card {{
        background: {PASTEL["card"]};
        border: 1px solid {PASTEL["border"]};
        border-radius: 18px;
        padding: 24px 26px;
        margin-bottom: 16px;
    }}

    /* 진행 바 */
    .progress-wrap {{
        background: {PASTEL["card"]};
        border: 1px solid {PASTEL["border"]};
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 18px;
    }}
    .progress-label {{
        display:flex; justify-content:space-between; align-items:center;
        font-size: 13px; font-weight: 600;
        color: {PASTEL["text"]}; margin-bottom: 8px;
    }}
    .progress-bar {{
        width: 100%; height: 10px;
        background: {PASTEL["border"]};
        border-radius: 5px; overflow: hidden;
    }}
    .progress-fill {{
        height: 100%;
        background: linear-gradient(90deg, {PASTEL["lavender"]}, {PASTEL["pink"]});
        border-radius: 5px;
        transition: width 0.5s ease;
    }}

    /* 문제 */
    .question-num {{
        display: inline-block;
        background: {PASTEL["lavender"]};
        color: white;
        font-size: 12px; font-weight: 700;
        padding: 4px 12px;
        border-radius: 10px;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
    }}
    .question-num.personal {{
        background: {PASTEL["coral"]};
    }}
    .question-text {{
        font-size: 18px; font-weight: 700;
        color: {PASTEL["text"]};
        line-height: 1.6;
        margin-bottom: 18px;
    }}

    /* 정답/오답 피드백 */
    .feedback-correct {{
        background: #F0FDF4;
        border-left: 4px solid {PASTEL["mint"]};
        border-radius: 12px;
        padding: 16px 18px;
        margin: 14px 0;
    }}
    .feedback-wrong {{
        background: #FEF2F2;
        border-left: 4px solid {PASTEL["coral"]};
        border-radius: 12px;
        padding: 16px 18px;
        margin: 14px 0;
    }}
    .feedback-title {{
        font-size: 15px; font-weight: 700;
        color: {PASTEL["text"]}; margin-bottom: 6px;
    }}
    .feedback-explain {{
        font-size: 13px; color: {PASTEL["text"]};
        line-height: 1.7;
    }}

    /* 결과 화면 */
    .result-hero {{
        background: linear-gradient(135deg, #A8E6CF 0%, #C7B8FF 100%);
        padding: 36px 32px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 20px;
    }}
    .result-hero .grade {{
        font-size: 64px;
        font-weight: 800;
        color: white;
        line-height: 1;
        margin-bottom: 8px;
    }}
    .result-hero .score {{
        font-size: 18px;
        color: white;
        font-weight: 600;
        opacity: 0.95;
    }}
    .result-hero .desc {{
        font-size: 14px;
        color: white;
        opacity: 0.9;
        margin-top: 10px;
        line-height: 1.6;
    }}

    .review-card {{
        background: {PASTEL["card"]};
        border: 1px solid {PASTEL["border"]};
        border-left: 4px solid {PASTEL["mint"]};
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }}
    .review-card.wrong {{
        border-left-color: {PASTEL["coral"]};
    }}
    .review-card .label {{
        font-size: 11px; font-weight: 700;
        letter-spacing: 0.5px;
    }}
    .review-card .label.ok {{ color: #047857; }}
    .review-card .label.no {{ color: #B91C1C; }}
    .review-card .q-text {{
        font-size: 14px; font-weight: 600;
        color: {PASTEL["text"]};
        margin: 4px 0 6px 0;
    }}
    .review-card .a-text {{
        font-size: 12px; color: {PASTEL["text_soft"]};
        line-height: 1.6;
    }}

    /* 버튼 */
    .stButton > button {{
        border-radius: 12px;
        font-weight: 600; font-size: 14px;
        border: 1.5px solid {PASTEL["border"]};
        background: {PASTEL["card"]};
        color: {PASTEL["text"]};
        padding: 10px 16px;
        transition: all 0.2s ease;
        text-align: left;
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

    /* 빈 상태 */
    .empty-state {{
        background: {PASTEL["card"]};
        border: 2px dashed {PASTEL["muted"]};
        border-radius: 20px;
        padding: 50px 30px;
        text-align: center;
        color: {PASTEL["text_soft"]};
    }}
    .empty-state .ico {{ font-size: 48px; margin-bottom: 12px; }}
    .empty-state .ttl {{ font-size: 17px; font-weight: 700; color: {PASTEL["text"]}; margin-bottom: 8px; }}
    .empty-state .msg {{ font-size: 13px; line-height: 1.6; }}

    /* 배지 */
    .tag {{
        display:inline-block;
        padding: 3px 10px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: 600;
        margin-right: 6px;
    }}
    .tag-general {{ background: #EDE9FE; color: #5B21B6; }}
    .tag-personal {{ background: #FEE2E2; color: #9F1239; }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 세션 상태
# =========================================================
if "weights" not in st.session_state:
    st.session_state.weights = {cat: 1 for cat in categories}
if "click_history" not in st.session_state:
    st.session_state.click_history = []

# 퀴즈 전용 상태
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []
if "quiz_current" not in st.session_state:
    st.session_state.quiz_current = 0
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = []
if "quiz_show_feedback" not in st.session_state:
    st.session_state.quiz_show_feedback = False
if "quiz_selected" not in st.session_state:
    st.session_state.quiz_selected = None

# =========================================================
# 문제 생성 함수
# =========================================================
def generate_questions():
    """체험 데이터 기반으로 8문제 생성 (공통 5 + 개인화 3)"""
    history = st.session_state.click_history
    counts = {c: history.count(c) for c in categories}
    dominant = max(counts, key=counts.get) if any(counts.values()) else "연예"
    diversity = sum(1 for v in counts.values() if v > 0)
    missed = [c for c in categories if counts[c] == 0]

    # ===== 공통 문제 (5개) =====
    general = [
        {
            "type": "general",
            "q": "필터 버블(Filter Bubble)이란 무엇일까요?",
            "options": [
                "인터넷 속도를 빠르게 해주는 캐싱 기술",
                "알고리즘이 사용자가 선호할 만한 정보만 보여주어 다른 시각이 차단되는 현상",
                "스팸 메일을 자동으로 걸러주는 보안 필터",
                "동영상 화질을 자동으로 조절하는 기능"
            ],
            "answer": 1,
            "explain": "필터 버블은 엘리 프레이저가 제시한 개념으로, 알고리즘이 사용자 취향에 맞는 정보만 선별해 보여줌으로써 다양한 관점이 차단되는 현상입니다."
        },
        {
            "type": "general",
            "q": "확증 편향(Confirmation Bias)에 대한 설명으로 가장 적절한 것은?",
            "options": [
                "새로운 정보를 끊임없이 탐색하는 적극적인 태도",
                "자신의 기존 신념과 일치하는 정보만 선택적으로 받아들이는 인지 경향",
                "타인의 의견을 항상 존중하는 마음가짐",
                "통계 데이터를 무조건 신뢰하는 습관"
            ],
            "answer": 1,
            "explain": "확증 편향은 자신의 믿음을 강화하는 정보만 받아들이는 인지 편향입니다. 필터 버블이 이를 심화시키는 주요 원인이 됩니다."
        },
        {
            "type": "general",
            "q": "유튜브·SNS 추천 알고리즘이 '자극적인 콘텐츠'를 더 많이 추천하는 이유는?",
            "options": [
                "자극적인 콘텐츠가 사회에 더 유익하기 때문에",
                "체류 시간과 클릭률이 높아 광고 수익 극대화에 유리하기 때문에",
                "AI가 윤리적으로 자극적인 것을 선호하기 때문에",
                "법적으로 강제되어 있기 때문에"
            ],
            "answer": 1,
            "explain": "플랫폼은 사용자 체류 시간을 늘릴수록 광고 수익이 증가합니다. 분노·충격·논란을 유발하는 콘텐츠가 클릭률이 높기 때문에 알고리즘이 우선 추천하게 됩니다."
        },
        {
            "type": "general",
            "q": "디지털 리터러시(Digital Literacy)에 포함되지 않는 것은?",
            "options": [
                "정보의 출처와 신뢰성을 검증하는 능력",
                "여러 관점의 정보를 비교하며 판단하는 능력",
                "알고리즘이 추천하는 내용을 그대로 믿고 따르는 습관",
                "개인정보와 디지털 흔적을 안전하게 관리하는 능력"
            ],
            "answer": 2,
            "explain": "디지털 리터러시는 정보를 비판적으로 분석하고 검증하는 능력입니다. 알고리즘의 추천을 무비판적으로 수용하는 것은 오히려 디지털 리터러시 부족의 신호입니다."
        },
        {
            "type": "general",
            "q": "필터 버블에서 벗어나기 위한 실천 방법으로 가장 적절하지 않은 것은?",
            "options": [
                "주기적으로 검색 기록과 쿠키를 삭제한다",
                "내 의견과 다른 관점의 매체도 의도적으로 찾아본다",
                "시크릿 모드로 다양한 정보를 탐색해 본다",
                "한 플랫폼만 깊이 사용하여 알고리즘 신뢰도를 높인다"
            ],
            "answer": 3,
            "explain": "한 플랫폼만 사용할수록 알고리즘은 더 좁고 강한 필터 버블을 만듭니다. 다양한 매체와 관점을 의도적으로 접하는 것이 탈출의 핵심입니다."
        }
    ]

    # ===== 개인화 문제 (3개) =====
    personal = []

    # P1. 우세 카테고리 인식
    personal.append({
        "type": "personal",
        "q": f"이번 체험에서 당신은 {CAT_ICONS.get(dominant,'')} '{dominant}' 카테고리를 가장 많이({counts[dominant]}회) 클릭했습니다. 이 결과가 의미하는 바는?",
        "options": [
            "특별한 의미는 없다 — 좋아하는 분야를 보는 건 개인의 자유다",
            f"알고리즘이 '{dominant}' 관련 콘텐츠 비중을 급격히 늘려, 다른 분야의 정보가 시야에서 사라지게 된다",
            "데이터 사용량이 평소보다 늘어난다",
            "광고가 더 많이 노출되어 불편해진다"
        ],
        "answer": 1,
        "explain": f"한 분야에 클릭이 집중되면 알고리즘은 그 분야의 가중치를 폭발적으로 높입니다. 그 결과 다른 카테고리의 중요한 뉴스나 다른 시각이 추천 피드에서 자연스럽게 밀려나게 됩니다."
    })

    # P2. 다양성 진단
    if diversity <= 2:
        div_q = f"체험 중 당신은 6개 카테고리 중 {diversity}개만 클릭했습니다. 이런 정보 소비 패턴은 어떤 위험이 있을까요?"
        div_opts = [
            "전혀 위험하지 않다 — 관심 있는 것만 봐도 충분하다",
            "사각지대가 커져, 사회의 중요한 이슈를 놓치거나 한쪽 시각에만 익숙해질 수 있다",
            "인터넷 속도가 느려진다",
            "스마트폰 배터리가 빨리 닳는다"
        ]
        div_ans = 1
        div_exp = f"단 {diversity}개 카테고리만 소비하면 나머지 {6-diversity}개 분야의 중요한 정보가 가려집니다. 이는 사회 전체를 균형 있게 이해하는 데 큰 장애가 됩니다."
    else:
        div_q = f"체험 중 당신은 {diversity}가지 카테고리를 탐색했습니다. 다양성을 유지하는 것이 왜 중요할까요?"
        div_opts = [
            "다양한 콘텐츠를 봐야 데이터 요금제를 다 쓸 수 있어서",
            "다양한 관점에 노출될수록 비판적 사고와 균형 잡힌 판단이 가능해지기 때문에",
            "알고리즘이 더 정확한 추천을 하기 위해서",
            "특별한 이유 없이 그냥 보기 좋아서"
        ]
        div_ans = 1
        div_exp = "다양한 정보에 노출되면 여러 시각을 비교·검증할 수 있어 비판적 사고력과 균형 잡힌 판단력이 길러집니다. 이것이 민주 사회의 핵심 역량입니다."

    personal.append({
        "type": "personal",
        "q": div_q, "options": div_opts, "answer": div_ans, "explain": div_exp
    })

    # P3. 사각지대 또는 자극적 콘텐츠
    if missed:
        missed_str = ", ".join([f"{CAT_ICONS[c]} {c}" for c in missed[:3]])
        personal.append({
            "type": "personal",
            "q": f"체험 중 당신이 한 번도 클릭하지 않은 분야: {missed_str}. 이런 '알고리즘 사각지대'의 문제점은?",
            "options": [
                "문제없다 — 안 본 분야는 어차피 나와 관련 없는 것들이다",
                "그 분야의 중요한 사회·생활 정보가 의도치 않게 가려져, 균형 잡힌 세상 이해가 어려워진다",
                "해당 분야 기자들이 일자리를 잃는다",
                "검색 엔진의 처리 속도가 느려진다"
            ],
            "answer": 1,
            "explain": "안 본 분야라고 해서 나와 무관한 것은 아닙니다. 정치·교육·사건사고 등은 일상에 직접적인 영향을 미치며, 이런 정보가 가려지면 중요한 결정을 내릴 때 정보 부족 상태가 됩니다."
        })
    else:
        personal.append({
            "type": "personal",
            "q": "체험 후반부에는 '충격', '단독', '논란' 같은 자극적 단어의 기사가 늘어났습니다. 이런 현상의 핵심 원인은?",
            "options": [
                "기자들이 갑자기 자극적인 글쓰기를 좋아하게 되어서",
                "버블이 깊어질수록 알고리즘이 클릭률 높은 자극적 콘텐츠를 우선 노출하기 때문에",
                "사용자의 화면 밝기가 자동으로 변해서",
                "AI가 윤리적으로 자극을 선호해서"
            ],
            "answer": 1,
            "explain": "알고리즘은 사용자의 체류 시간을 늘리도록 학습됩니다. 일반 정보보다 자극적 콘텐츠가 클릭률이 훨씬 높기 때문에, 버블이 심화될수록 자극적 기사 비중이 가파르게 증가합니다."
        })

    # 최종 8문제 — 공통 5 + 개인화 3
    questions = general + personal
    return questions

# =========================================================
# 헤로
# =========================================================
st.markdown("""
<div class="quiz-hero">
  <h1>🧠 AI 윤리 퀴즈</h1>
  <p>방금 체험한 필터 버블 시뮬레이션 결과를 바탕으로, 나만의 맞춤 문제가 출제됩니다.<br>
  총 8문제 · 정답을 맞히지 못해도 친절한 해설로 함께 배워가요.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 1) 시작 전 화면
# =========================================================
if not st.session_state.quiz_started:
    total_clicks = len(st.session_state.click_history)

    if total_clicks == 0:
        st.markdown("""
        <div class="empty-state">
          <div class="ico">🌱</div>
          <div class="ttl">먼저 체험을 시작해 주세요</div>
          <div class="msg">
            메인 페이지에서 기사를 몇 개 클릭해 보세요.<br>
            체험 데이터가 쌓이면 맞춤형 퀴즈가 생성됩니다.
          </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🫧 체험하러 가기", type="primary", use_container_width=True):
            st.switch_page("pages/bubble2.py")
    else:
        # 시작 안내 카드
        st.markdown(f"""
        <div class="pastel-card">
          <h3 style="margin-top:0; color:{PASTEL['text']};">🎯 퀴즈 구성</h3>
          <div style="font-size:14px; color:{PASTEL['text']}; line-height:2;">
            <span class="tag tag-general">공통</span> AI 윤리·필터 버블 기본 개념 <b>5문제</b><br>
            <span class="tag tag-personal">맞춤</span> 나의 체험 데이터를 바탕으로 한 분석 문제 <b>3문제</b>
          </div>
          <hr style="border:none; border-top:1px solid {PASTEL['border']}; margin:16px 0;">
          <div style="font-size:13px; color:{PASTEL['text_soft']}; line-height:1.7;">
            💡 객관식 4지선다 · 정답 확인 후 해설 제공<br>
            📊 마지막에 등급과 함께 오답 리뷰가 표시됩니다
          </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("🚀 퀴즈 시작하기", type="primary", use_container_width=True):
                st.session_state.quiz_questions = generate_questions()
                st.session_state.quiz_current = 0
                st.session_state.quiz_answers = []
                st.session_state.quiz_started = True
                st.session_state.quiz_show_feedback = False
                st.session_state.quiz_selected = None
                st.rerun()
        with c2:
            if st.button("🫧 체험으로 돌아가기", use_container_width=True):
                st.switch_page("pages/bubble2.py")

# =========================================================
# 2) 퀴즈 진행 중
# =========================================================
elif st.session_state.quiz_current < len(st.session_state.quiz_questions):
    qs = st.session_state.quiz_questions
    idx = st.session_state.quiz_current
    q = qs[idx]
    total_q = len(qs)
    progress_pct = int(((idx) / total_q) * 100)

    # 진행 바
    st.markdown(f"""
    <div class="progress-wrap">
      <div class="progress-label">
        <span>📝 진행도</span>
        <span style="color:{PASTEL['lavender']};">{idx + 1} / {total_q}</span>
      </div>
      <div class="progress-bar">
        <div class="progress-fill" style="width:{progress_pct}%;"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 문제 카드
    badge_class = "personal" if q["type"] == "personal" else ""
    badge_label = "맞춤 문제" if q["type"] == "personal" else "공통 문제"
    st.markdown(f"""
    <div class="pastel-card">
      <span class="question-num {badge_class}">Q{idx+1} · {badge_label}</span>
      <div class="question-text">{q["q"]}</div>
    </div>
    """, unsafe_allow_html=True)

    # 선택지 — 아직 답을 안 골랐으면 선택 버튼, 골랐으면 피드백
    if not st.session_state.quiz_show_feedback:
        for i, opt in enumerate(q["options"]):
            if st.button(f"  {chr(65+i)}.  {opt}", key=f"opt_{idx}_{i}",
                         use_container_width=True):
                st.session_state.quiz_selected = i
                st.session_state.quiz_show_feedback = True
                st.session_state.quiz_answers.append({
                    "q": q["q"], "type": q["type"],
                    "selected": i, "answer": q["answer"],
                    "options": q["options"], "explain": q["explain"],
                    "correct": i == q["answer"]
                })
                st.rerun()
    else:
        selected = st.session_state.quiz_selected
        is_correct = (selected == q["answer"])

        # 선택지 결과 표시
        for i, opt in enumerate(q["options"]):
            if i == q["answer"]:
                style = f"background:#F0FDF4; border:2px solid {PASTEL['mint']};"
                mark = "✅"
            elif i == selected and not is_correct:
                style = f"background:#FEF2F2; border:2px solid {PASTEL['coral']};"
                mark = "❌"
            else:
                style = f"background:{PASTEL['card']}; border:1px solid {PASTEL['border']};"
                mark = "　"
            st.markdown(f"""
            <div style="{style} border-radius:12px; padding:12px 16px; margin-bottom:8px;
                        font-size:14px; color:{PASTEL['text']};">
              {mark} {chr(65+i)}. {opt}
            </div>
            """, unsafe_allow_html=True)

        # 피드백
        if is_correct:
            st.markdown(f"""
            <div class="feedback-correct">
              <div class="feedback-title">🎉 정답입니다!</div>
              <div class="feedback-explain">{q["explain"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="feedback-wrong">
              <div class="feedback-title">💡 아쉽지만 정답은 <b>{chr(65+q["answer"])}</b>번이에요</div>
              <div class="feedback-explain">{q["explain"]}</div>
            </div>
            """, unsafe_allow_html=True)

        # 다음 버튼
        next_label = "🏁 결과 보기" if idx == total_q - 1 else "다음 문제 →"
        if st.button(next_label, type="primary", use_container_width=True):
            st.session_state.quiz_current += 1
            st.session_state.quiz_show_feedback = False
            st.session_state.quiz_selected = None
            st.rerun()

# =========================================================
# 3) 결과 화면
# =========================================================
else:
    answers = st.session_state.quiz_answers
    total_q = len(answers)
    correct_count = sum(1 for a in answers if a["correct"])
    score_pct = int((correct_count / total_q) * 100) if total_q else 0

    # 등급 산정
    if score_pct >= 90:
        grade, grade_desc = "A+", "AI 윤리 마스터! 알고리즘 사회를 비판적으로 바라볼 준비가 되었어요."
    elif score_pct >= 75:
        grade, grade_desc = "A", "훌륭해요! 디지털 리터러시가 매우 탄탄합니다."
    elif score_pct >= 60:
        grade, grade_desc = "B", "잘했어요! 몇 가지 개념만 더 다듬으면 완벽해요."
    elif score_pct >= 40:
        grade, grade_desc = "C", "기본기는 갖췄어요. 오답 해설을 꼼꼼히 살펴보세요."
    else:
        grade, grade_desc = "D", "괜찮아요, 처음엔 누구나 어려워요. 해설과 함께 다시 도전해 봐요!"

    # 결과 헤로
    st.markdown(f"""
    <div class="result-hero">
      <div class="grade">{grade}</div>
      <div class="score">{correct_count} / {total_q} 정답 · {score_pct}점</div>
      <div class="desc">{grade_desc}</div>
    </div>
    """, unsafe_allow_html=True)

    # 통계
    general_correct = sum(1 for a in answers if a["correct"] and a["type"] == "general")
    personal_correct = sum(1 for a in answers if a["correct"] and a["type"] == "personal")
    general_total = sum(1 for a in answers if a["type"] == "general")
    personal_total = sum(1 for a in answers if a["type"] == "personal")

    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(f"""
        <div class="pastel-card" style="text-align:center;">
          <div style="font-size:12px; color:{PASTEL['text_soft']}; font-weight:600;">총점</div>
          <div style="font-size:32px; color:{PASTEL['text']}; font-weight:700; margin-top:4px;">{score_pct}점</div>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
        <div class="pastel-card" style="text-align:center;">
          <div style="font-size:12px; color:{PASTEL['text_soft']}; font-weight:600;">공통 문제</div>
          <div style="font-size:24px; color:{PASTEL['text']}; font-weight:700; margin-top:4px;">{general_correct} / {general_total}</div>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown(f"""
        <div class="pastel-card" style="text-align:center;">
          <div style="font-size:12px; color:{PASTEL['text_soft']}; font-weight:600;">맞춤 문제</div>
          <div style="font-size:24px; color:{PASTEL['text']}; font-weight:700; margin-top:4px;">{personal_correct} / {personal_total}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # 오답 리뷰
    wrong_answers = [a for a in answers if not a["correct"]]
    if wrong_answers:
        st.markdown(f"""
        <div style="font-size:16px; font-weight:700; color:{PASTEL['text']};
                    margin: 14px 0 10px 0;">📝 오답 리뷰</div>
        """, unsafe_allow_html=True)
        for i, a in enumerate(wrong_answers):
            st.markdown(f"""
            <div class="review-card wrong">
              <div class="label no">틀린 문제</div>
              <div class="q-text">{a["q"]}</div>
              <div class="a-text">
                ❌ 내 선택: {chr(65+a["selected"])}. {a["options"][a["selected"]]}<br>
                ✅ 정답: {chr(65+a["answer"])}. {a["options"][a["answer"]]}<br>
                <br>💡 {a["explain"]}
              </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="pastel-card" style="text-align:center; background:#F0FDF4;
                    border-color:{PASTEL['mint']};">
          <div style="font-size:36px;">🏆</div>
          <div style="font-size:16px; font-weight:700; color:#047857; margin-top:6px;">
            완벽! 모든 문제를 맞혔어요
          </div>
          <div style="font-size:13px; color:{PASTEL['text_soft']}; margin-top:6px;">
            AI 윤리에 대한 이해도가 매우 높습니다.
          </div>
        </div>
        """, unsafe_allow_html=True)

    # 핵심 메시지
    st.markdown(f"""
    <div class="pastel-card" style="background:#FAF5FF; border-color:{PASTEL['lavender']};">
      <div style="font-size:14px; font-weight:700; color:{PASTEL['text']}; margin-bottom:8px;">
        🌱 오늘 배운 것을 기억해 주세요
      </div>
      <div style="font-size:13px; color:{PASTEL['text']}; line-height:1.8;">
        ✓ 알고리즘은 <b>나에게 맞춰진 도구</b>이지만, 동시에 <b>나의 시야를 좁히는 함정</b>이 될 수 있어요.<br>
        ✓ 의식적으로 <b>다른 시각의 정보</b>를 찾아보는 것이 필터 버블 탈출의 시작이에요.<br>
        ✓ 디지털 리터러시는 <b>비판적 사고</b>에서 시작합니다.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 액션 버튼
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("🔁 퀴즈 다시 풀기", use_container_width=True):
            st.session_state.quiz_started = False
            st.session_state.quiz_questions = []
            st.session_state.quiz_current = 0
            st.session_state.quiz_answers = []
            st.rerun()
    with b2:
        if st.button("🗺️ 내 지도 보기", use_container_width=True):
            st.switch_page("pages/map.py")
    with b3:
        if st.button("🫧 체험으로 돌아가기", type="primary", use_container_width=True):
            st.switch_page("pages/bubble2.py")

