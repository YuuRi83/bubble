import streamlit as st
import random
import pandas as pd

# -----------------------
# 페이지 설정 
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
# 기사 제목 데이터베이스 (다양성 대폭 확대)
# -----------------------
normal_titles = {
    "스포츠": [
        "⚽ 손흥민, 경기 MVP 선정", "🏀 NBA 플레이오프 명승부", "⚾ 프로야구 순위 경쟁 치열", 
        "🏐 V리그 챔피언 결정전 프리뷰", "🏃 전국 체전, 학생부 신기록 달성", "🏟️ 주말 K리그 관전 포인트", 
        "🎾 테니스 메이저 대회 이변 발생", "🏊 세계 수영 선수권 대회 개막"
    ],
    "정치": [
        "🗳️ 정책 토론 주요 쟁점", "📢 사회 현안 논의 확대", "🏛️ 정부 정책 발표", 
        "🤝 여야, 민생 법안 합의 시도", "📊 이번 주 정당 지지율 여론조사", "🌐 국제 외교 회담 성공적 마무리", 
        "🏫 청소년 참정권 관련 토론회", "📉 내년 국가 예산안 편성 심사"
    ],
    "게임": [
        "🎮 신작 게임 출시 기대감", "🔥 인기 게임 e스포츠 대회 개최", "🕹️ 게이밍 트렌드 변화 분석", 
        "💻 모바일 게임 매출 순위 업데이트", "🎧 인기 스트리머 합방 소식", "🏆 글로벌 게임 대회 결승전 일정", 
        "🧩 인디 게임 페스티벌 성황리 종료", "🛠️ 대규모 패치노트: 캐릭터 밸런스 조정"
    ],
    "연예": [
        "🎤 인기 아이돌 성공적인 컴백", "🎬 화제의 웹드라마 전편 공개", "📺 주말 예능 프로그램 시청률 1위", 
        "🎵 K팝 아티스트 빌보드 차트 진입", "📸 유명 배우 화보 촬영 현장 비하인드", "🍿 주말 박스오피스 예매율 1위 영화는?", 
        "✨ 대국민 오디션 프로그램 우승자 발표", "🎧 이번 주 음악방송 1위 후보 라인업"
    ],
    "교육": [
        "📚 AI 시대가 바꾸는 교실 풍경", "🧠 뇌과학 기반 효과적인 공부법 연구", "💡 10년 뒤 미래 직업 변화 전망", 
        "🏫 새 학기 달라지는 중학교 학교 규정", "📖 문해력 쑥쑥 향상시키는 10분 독서법", "📝 바뀌는 대입 제도 심층 분석", 
        "🎓 대학생 선배들이 추천하는 유망 전공", "🧪 전국 학생 과학 발명품 경진대회"
    ],
    "자극": [
        "😱 전문가들도 놀란 충격적인 사건", "🚨 지금 당장 확인 안 하면 손해", "🔥 모두가 경악한 오늘의 핫이슈", 
        "👀 이것만 알면 당신의 인생이 바뀐다", "😲 아무도 몰랐던 소름 돋는 숨겨진 비밀", "🤔 99%가 틀리는 논란의 문제", 
        "🤫 상위 1%만 안다는 은밀한 꿀팁", "💸 하루 10분 투자로 한 달 용돈 버는 법"
    ]
}

extreme_titles = {
    "스포츠": [
        "⚽ 충격! 대표팀 대참사", "🏀 역대급 오심 논란, 팬들 분노", "⚾ 벤치클리어링 발발, 난장판 된 경기장", 
        "🤬 감독 전격 경질설, 팀 내분 심각", "🚨 핵심 에이스 치명적 부상, 시즌 아웃 위기"
    ],
    "정치": [
        "🚨 정치권 초비상 사태", "🔥 국민 여론 폭발, 대규모 시위 예고", "😱 막말 논란에 정치권 발칵", 
        "💥 국회 파행, 육탄전 직전의 상황", "🚨 지지율 곤두박질, 비상대책위 전격 가동"
    ],
    "게임": [
        "🎮 역대급 게임 중독 논란 확산", "🔥 서버 터짐! 유저들 분노 폭발", "🤬 심각한 과금 유도 논란, 불매 운동 시작", 
        "🚨 유저 기만 논란, 트럭 시위 예고", "😱 전설의 프로게이머, 갑작스러운 은퇴 선언"
    ],
    "연예": [
        "😱 연예계 발칵 뒤집힌 충격 소식", "🔥 팬들 멘붕, 단독 열애설 포착", "🚨 소속사 분쟁 심화, 진흙탕 법적 공방", 
        "🤬 과거 인성 논란 폭로글 등장, 진실 공방", "💔 믿었던 스타의 배신, 팬클럽 단체 탈퇴"
    ],
    "교육": [
        "🚨 AI가 모든 교사를 완전히 대체한다?", "😱 10년 후 완전히 멸종할 직업 리스트", "💥 수능 전면 폐지론 대두, 학생들 대혼란", 
        "🤬 미친 학원비 폭등, 학부모들 등골 휜다", "🚨 학교 폭력 실태조사, 경악스러운 결과"
    ],
    "자극": [
        "🚨 충격 단독! 전 국민이 속고 있었다", "😱 지금 당장 클릭 안 하면 평생 후회", "💥 전 국민 경악하게 만든 유출된 cctv 영상", 
        "🤬 절대 입에 대면 안 되는 최악의 음식 TOP 3", "🚨 당장 스마트폰에서 삭제해야 할 앱 리스트"
    ]
}

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
    
    # 1. 가중치를 기반으로 뽑을 6개의 카테고리 선정
    weighted_categories = []
    for cat in categories:
        weighted_categories.extend([cat] * st.session_state.weights[cat])
    
    chosen_categories = random.choices(weighted_categories, k=6)
    
    # 2. 선택된 카테고리의 개수 세기 (예: 스포츠 3개, 게임 2개, 정치 1개)
    cat_counts = {cat: chosen_categories.count(cat) for cat in set(chosen_categories)}
    
    feed = []
    for cat, count in cat_counts.items():
        # 버블 단계에 따라 일반 제목 or 극단적(자극적) 제목 선택
        titles_pool = normal_titles[cat] if bubble_level < 3 else extreme_titles[cat]
        
        # 같은 화면에서 제목이 중복되지 않도록 random.sample 사용
        # (만약 뽑아야 할 개수가 제목 풀보다 많으면 어쩔 수 없이 중복 허용)
        if count <= len(titles_pool):
            sampled_titles = random.sample(titles_pool, count)
        else:
            sampled_titles = random.choices(titles_pool, k=count)
            
        for title in sampled_titles:
            feed.append({"title": title, "category": cat})
            
    # 기사들의 순서를 랜덤으로 한 번 섞어줌
    random.shuffle(feed)
    return feed

def click_content(item):
    cat = item["category"]
    st.session_state.click_history.append(cat)
    # 선택한 콘텐츠의 가중치는 대폭 늘림
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
st.write("") 

left_col, right_col = st.columns([1.2, 1])

# --- 좌측: 맞춤형 추천 피드 ---
with left_col:
    st.subheader("📰 맞춤형 추천 피드")
    feed = get_feed()
    
    feed_col1, feed_col2 = st.columns(2)
    
    for i, item in enumerate(feed):
        target_col = feed_col1 if i % 2 == 0 else feed_col2
        with target_col:
            with st.container(border=True):
                st.markdown(f"#### {item['title']}")
                st.caption(f"📂 카테고리: {item['category']}")
                
                if st.button("클릭하여 보기", key=f"btn_{i}", use_container_width=True):
                    click_content(item)
                    st.rerun()

# --- 우측: 실시간 분석 대시보드 ---
with right_col:
    st.subheader("🤖 실시간 AI 분석")
    total_clicks = len(st.session_state.click_history)
    bubble_level = get_bubble_level()

    if bubble_level == 1:
        st.success("🟢 **1단계: 균형 상태**\n\n다양한 정보가 고르게 추천되고 있습니다.")
    elif bubble_level == 2:
        st.warning("🟡 **2단계: 버블 형성 시작**\n\n특정 분야의 추천 비율이 슬슬 늘어나고 있습니다.")
    elif bubble_level == 3:
        st.error("🟠 **3단계: 버블 심화 (주의!)**\n\n자극적인 기사가 늘고, 다른 분야의 정보가 사라지고 있습니다.")
    else:
        st.error("🔴 **4단계: 필터 버블 고착화 (확증 편향)**\n\n완전히 갇혔습니다! 내가 좋아하는 정보만 보입니다.")

    ptype, desc = analyze_personality()
    with st.expander("📋 나의 디지털 성향 분석 결과", expanded=True):
        st.markdown(f"### {ptype}")
        st.write(desc)
        
        if total_clicks >= 5:
            dominant = max(st.session_state.weights, key=st.session_state.weights.get)
            st.warning(f"🚨 경고: 정보 환경이 **{dominant}** 위주로 좁아지고 있습니다.")

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
    st.write("") 
    if st.button("🔄 전체 초기화 및 다시 시작", type="primary", use_container_width=True):
        st.session_state.weights = {cat: 1 for cat in categories}
        st.session_state.click_history = []
        st.rerun()
