import streamlit as st
import random
import pandas as pd

# -----------------------
# 페이지 설정 (가장 먼저 실행되어야 함)
# -----------------------
st.set_page_config(page_title="추천 알고리즘 버블 체험", page_icon="🫧", layout="wide")

categories = ["스포츠", "정치", "게임", "연예", "자극", "교육"]

# -----------------------
# 세션 상태 초기화
# -----------------------
if "weights" not in st.session_state:
    st.session_state.weights = {cat: 1 for cat in categories}

if "click_history" not in st.session_state:
    st.session_state.click_history = []

# -----------------------
# AI 기사 제목 생성
# -----------------------
def generate_title(category, bubble_level):
    normal_titles = {
        "스포츠": ["⚽ 손흥민, 경기 MVP 선정", "🏀 NBA 플레이오프 명승부", "⚾ 프로야구 순위 경쟁 치열"],
        "정치": ["🗳️ 정책 토론 주요 쟁점", "📢 사회 현안 논의 확대", "🏛️ 정부 정책 발표"],
        "게임": ["🎮 신작 게임 출시", "🔥 인기 게임 대회 개최", "🕹️ 게이밍 트렌드 변화"],
        "연예": ["🎤 인기 아이돌 컴백", "🎬 화제의 드라마 공개", "📺 예능 프로그램 인기 상승"],
        "교육": ["📚 AI가 바꾸는 교육", "🧠 효과적인 공부법 연구", "💡 미래 직업 변화 전망"],
        "자극": ["😱 충격적인 사건 발생", "🚨 지금 안 보면 손해", "🔥 모두가 놀란 소식"]
    }

    extreme_titles = {
        "스포츠": ["⚽ 충격! 대표팀 대참사", "🏀 역대급 논란 발생"],
        "정치": ["🚨 정치권 초비상", "🔥 여론 폭발"],
        "게임": ["🎮 역대급 게임 중독 논란", "🔥 유저들 분노 폭발"],
        "연예": ["😱 연예계 충격 소식", "🔥 팬들 충격"],
        "교육": ["🚨 AI가 교사를 대체한다?", "😱 10년 후 사라질 직업"],
        "자극": ["🚨 충격! 모두가 속고 있었다", "😱 지금 클릭 안 하면 후회"]
    }

    if bubble_level >= 3:
        return random.choice(extreme_titles[category])
    return random.choice(normal_titles[category])

# -----------------------
# 추천 알고리즘 로직
# -----------------------
def get_bubble_level():
    clicks = len(st.session_state.click_history)
    if clicks <= 2: return 1
    elif clicks <= 5: return 2
    elif clicks <= 9: return 3
    return 4

def get_feed():
    bubble_level = get_bubble_level()
    weighted_categories = []
    for cat in categories:
        weighted_categories.extend([cat] * st.session_state.weights[cat])

    feed = []
    for _ in range(6):
        cat = random.choice(weighted_categories)
        feed.append({
            "title": generate_title(cat, bubble_level),
            "category": cat
        })
    return feed

def click_content(item):
    cat = item["category"]
    st.session_state.click_history.append(cat)
    st.session_state.weights[cat] += 3

def analyze_personality():
    history = st.session_state.click_history
    if len(history) == 0:
        return "분석 대기 중 ⏳", "콘텐츠를 클릭하면 분석이 시작됩니다."

    counts = {cat: history.count(cat) for cat in categories}
    dominant = max(counts, key=counts.get)

    if len(set(history)) >= 4:
        return "균형 탐색형 🌍", "다양한 분야의 관점을 고르게 탐색하는 건강한 성향입니다."

    labels = {
        "스포츠": "스포츠 몰입형 ⚽",
        "정치": "이슈 집중형 🗳️",
        "게임": "몰입형 게이머 🎮",
        "연예": "트렌드 민감형 🎤",
        "자극": "도파민 추구형 🚨",
        "교육": "지식 탐구형 📚"
    }
    return labels[dominant], f"현재 **{dominant}** 콘텐츠를 집중적으로 소비하고 있습니다."

# -----------------------
# 메인 UI 구성
# -----------------------
st.title("📱 추천 알고리즘과 필터 버블 체험")
st.markdown("**마음에 드는 기사를 계속 클릭해 보세요. AI가 여러분의 취향을 학습하여 화면을 바꿉니다!**")
st.write("") # 간격 띄우기

# 좌측(피드)과 우측(대시보드)으로 화면 분할 (비율 6:4)
left_col, right_col = st.columns([1.2, 1])

# --- 좌측: 맞춤형 추천 피드 ---
with left_col:
    st.subheader("📰 맞춤형 추천 피드")
    feed = get_feed()
    
    # 기사를 2열 카드 형태로 배치
    feed_col1, feed_col2 = st.columns(2)
    
    for i, item in enumerate(feed):
        # 짝수 인덱스는 왼쪽, 홀수 인덱스는 오른쪽에 배치
        target_col = feed_col1 if i % 2 == 0 else feed_col2
        
        with target_col:
            # 테두리가 있는 컨테이너(카드) 생성
            with st.container(border=True):
                st.markdown(f"#### {item['title']}")
                st.caption(f"📂 카테고리: {item['category']}")
                
                # 버튼을 카드 너비에 꽉 차게 설정
                if st.button("클릭하여 보기", key=f"btn_{i}", use_container_width=True):
                    click_content(item)
                    st.rerun()

# --- 우측: 실시간 분석 대시보드 ---
with right_col:
    st.subheader("🤖 실시간 AI 분석")
    total_clicks = len(st.session_state.click_history)
    bubble_level = get_bubble_level()

    # 1. 버블 심화 단계 알림창
    if bubble_level == 1:
        st.success("🟢 **1단계: 균형 상태**\n\n다양한 정보가 고르게 추천되고 있습니다.")
    elif bubble_level == 2:
        st.warning("🟡 **2단계: 버블 형성 시작**\n\n특정 분야의 추천 비율이 슬슬 늘어나고 있습니다.")
    elif bubble_level == 3:
        st.error("🟠 **3단계: 버블 심화 (주의!)**\n\n자극적인 기사가 늘고, 다른 분야의 정보가 사라지고 있습니다.")
    else:
        st.error("🔴 **4단계: 필터 버블 고착화 (확증 편향)**\n\n완전히 갇혔습니다! 내가 좋아하는 정보만 보입니다.")

    # 2. 디지털 성향 분석 리포트 (아코디언 메뉴 활용)
    ptype, desc = analyze_personality()
    with st.expander("📋 나의 디지털 성향 분석 결과", expanded=True):
        st.markdown(f"### {ptype}")
        st.write(desc)
        
        if total_clicks >= 5:
            dominant = max(st.session_state.weights, key=st.session_state.weights.get)
            st.warning(f"🚨 경고: 정보 환경이 **{dominant}** 위주로 좁아지고 있습니다.")

    # 3. 추천 강도 실시간 그래프
    st.markdown(f"**📊 카테고리별 AI 추천 가중치 (총 클릭: {total_clicks}회)**")
    df = pd.DataFrame({
        "카테고리": list(st.session_state.weights.keys()),
        "추천 강도": list(st.session_state.weights.values())
    })
    st.bar_chart(df.set_index("카테고리"), height=250)

# -----------------------
# 하단 푸터 (학습 포인트 & 초기화)
# -----------------------
st.divider()
bottom_col1, bottom_col2 = st.columns([3, 1])

with bottom_col1:
    st.markdown("#### 🎓 수업 핵심 키워드")
    st.info("✅ **필터 버블 (Filter Bubble)** | ✅ **확증 편향 (Confirmation Bias)** | ✅ **추천 알고리즘의 윤리** | ✅ **디지털 리터러시**")

with bottom_col2:
    st.write("") # 버튼 위치를 맞추기 위한 빈 공간
    if st.button("🔄 전체 초기화 및 다시 시작", type="primary", use_container_width=True):
        st.session_state.weights = {cat: 1 for cat in categories}
        st.session_state.click_history = []
        st.rerun()
