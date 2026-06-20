import streamlit as st
import random
import pandas as pd
import requests
import html
import re

# -----------------------
# 페이지 설정 
# -----------------------
st.set_page_config(page_title="추천 알고리즘 버블 체험", page_icon="🫧", layout="wide")

categories = ["스포츠", "정치", "게임", "연예", "사건사고", "교육"] # '자극'을 네이버 검색에 유리한 '사건사고'로 변경

# -----------------------
# 세션 상태 초기화
# -----------------------
if "weights" not in st.session_state:
    st.session_state.weights = {cat: 1 for cat in categories}

if "click_history" not in st.session_state:
    st.session_state.click_history = []

# -----------------------
# 네이버 뉴스 API 연동 함수 (캐싱 적용)
# -----------------------
# API 호출을 최소화하고 속도를 높이기 위해 1시간(3600초) 동안 결과를 저장(캐싱)합니다.
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_naver_news(category, is_extreme):
    # Streamlit Secrets에서 API 키 가져오기 (키가 없으면 빈 문자열 반환)
    client_id = st.secrets.get("NAVER_CLIENT_ID", "")
    client_secret = st.secrets.get("NAVER_CLIENT_SECRET", "")
    
    if not client_id or not client_secret:
        return None # 키가 없으면 안전장치(더미 데이터) 발동

    url = "https://openapi.naver.com/v1/search/news.json"
    
    # 버블 단계에 따라 검색어 조정 (자극적인 기사 유도)
    search_query = category
    if is_extreme:
        search_query += " (논란|충격|분노|단독|의혹)"
        
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    params = {
        "query": search_query,
        "display": 20, # 넉넉하게 20개 추출
        "sort": "sim"  # 정확도순
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            items = response.json().get("items", [])
            titles = []
            for item in items:
                # <b> 태그 등 HTML 찌꺼기 제거 및 특수문자 변환
                clean_title = re.sub(r'<[^>]+>', '', item['title'])
                clean_title = html.unescape(clean_title)
                titles.append(clean_title)
            return titles if titles else None
        else:
            return None
    except:
        return None

# -----------------------
# 기사 제목 데이터베이스 (안전장치용 더미 데이터)
# -----------------------
normal_titles = {
    "스포츠": ["⚽ 손흥민, 경기 MVP 선정", "🏀 NBA 플레이오프 명승부", "⚾ 프로야구 순위 경쟁 치열", "🏐 V리그 챔피언 결정전 프리뷰", "🏃 전국 체전, 학생부 신기록 달성"],
    "정치": ["🗳️ 정책 토론 주요 쟁점", "📢 사회 현안 논의 확대", "🏛️ 정부 정책 발표", "🤝 여야, 민생 법안 합의 시도", "📊 이번 주 정당 지지율 여론조사"],
    "게임": ["🎮 신작 게임 출시 기대감", "🔥 인기 게임 e스포츠 대회 개최", "🕹️ 게이밍 트렌드 변화 분석", "💻 모바일 게임 매출 순위 업데이트", "🎧 인기 스트리머 합방 소식"],
    "연예": ["🎤 인기 아이돌 성공적인 컴백", "🎬 화제의 웹드라마 전편 공개", "📺 주말 예능 프로그램 시청률 1위", "🎵 K팝 아티스트 빌보드 차트 진입"],
    "교육": ["📚 AI 시대가 바꾸는 교실 풍경", "🧠 뇌과학 기반 효과적인 공부법 연구", "💡 10년 뒤 미래 직업 변화 전망", "🏫 새 학기 달라지는 중학교 학교 규정"],
    "사건사고": ["경찰, 대규모 보이스피싱 일당 검거", "주말 고속도로 다중 추돌 사고", "전국적인 집중 호우 대비 태세", "건조한 날씨 산불 주의보 발령"]
}

extreme_titles = {
    "스포츠": ["⚽ 충격! 대표팀 대참사", "🏀 역대급 오심 논란, 팬들 분노", "⚾ 벤치클리어링 발발, 난장판 된 경기장"],
    "정치": ["🚨 정치권 초비상 사태", "🔥 국민 여론 폭발, 대규모 시위 예고", "😱 막말 논란에 정치권 발칵"],
    "게임": ["🎮 역대급 게임 중독 논란 확산", "🔥 서버 터짐! 유저들 분노 폭발", "🤬 심각한 과금 유도 논란, 불매 운동 시작"],
    "연예": ["😱 연예계 발칵 뒤집힌 충격 소식", "🔥 팬들 멘붕, 단독 열애설 포착", "🚨 소속사 분쟁 심화, 진흙탕 법적 공방"],
    "교육": ["🚨 AI가 모든 교사를 완전히 대체한다?", "😱 10년 후 완전히 멸종할 직업 리스트", "💥 수능 전면 폐지론 대두, 학생들 대혼란"],
    "사건사고": ["🚨 충격 단독! 전 국민이 속고 있었다", "😱 충격적인 흉악 범죄 발생, 시민들 불안", "💥 전 국민 경악하게 만든 유출된 cctv 영상"]
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
    is_extreme = bubble_level >= 3
    
    weighted_categories = []
    for cat in categories:
        weighted_categories.extend([cat] * st.session_state.weights[cat])
    
    chosen_categories = random.choices(weighted_categories, k=6)
    cat_counts = {cat: chosen_categories.count(cat) for cat in set(chosen_categories)}
    
    feed = []
    for cat, count in cat_counts.items():
        # 1. 네이버 뉴스 API 호출 시도
        titles_pool = fetch_naver_news(cat, is_extreme)
        
        # 2. API 실패 또는 데이터 부족 시 더미 데이터로 대체
        if not titles_pool or len(titles_pool) < count:
            titles_pool = extreme_titles[cat] if is_extreme else normal_titles[cat]
            
        # 중복 방지를 위한 샘플링
        if count <= len(titles_pool):
            sampled_titles = random.sample(titles_pool, count)
        else:
            sampled_titles = random.choices(titles_pool, k=count)
            
        for title in sampled_titles:
            # API에서 가져온 기사는 앞에 아이콘 추가 (구분용)
            display_title = title if (" " in title and title.startswith("🚨")) else f"🗞️ {title}"
            feed.append({"title": display_title, "category": cat})
            
    random.shuffle(feed)
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
        "사건사고": "도파민 추구형 🚨",
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
    st.subheader("📰 맞춤형 실시간 추천 피드")
    feed = get_feed()
    
    feed_col1, feed_col2 = st.columns(2)
    
    for i, item in enumerate(feed):
        target_col = feed_col1 if i % 2 == 0 else feed_col2
        with target_col:
            with st.container(border=True):
                st.markdown(f"**{item['title']}**")
                st.caption(f"📂 카테고리: {item['category']}")
                
                if st.button("클릭하여 보기", key=f"btn_{i}_{len(st.session_state.click_history)}", use_container_width=True):
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
# 하단: 해결책 및 교육 포인트
# -----------------------
st.divider()

st.subheader("🛡️ 필터 버블에서 탈출하는 방법 3가지")
st.markdown("내가 갇힌 버블(거품)을 터뜨리고 더 넓은 세상을 보려면 어떻게 해야 할까요?")

escape_col1, escape_col2, escape_col3 = st.columns(3)
with escape_col1:
    st.info("🗑️ **1. 시청/검색 기록 지우기**\n\n주기적으로 유튜브나 포털의 검색 기록과 쿠키를 지워서 AI 알고리즘을 초기화하세요.")
with escape_col2:
    st.info("🕵️‍♂️ **2. 시크릿 모드 사용하기**\n\n나의 과거 데이터가 반영되지 않는 '시크릿 브라우징'을 통해 새로운 정보를 탐색하세요.")
with escape_col3:
    st.info("⚖️ **3. 반대 의견 찾아보기**\n\n내가 좋아하는 기사만 보지 말고, 일부러 나와 다른 시각을 가진 영상이나 글을 클릭해 보세요.")

st.write("") 

bottom_col1, bottom_col2 = st.columns([3, 1])
with bottom_col1:
    st.markdown("#### 🎓 수업 핵심 키워드")
    st.success("✅ **필터 버블 (Filter Bubble)** | ✅ **확증 편향 (Confirmation Bias)** | ✅ **추천 알고리즘 윤리** | ✅ **디지털 리터러시**")

with bottom_col2:
    st.write("") 
    if st.button("🔄 시청 기록 삭제 (버블 탈출!)", type="primary", use_container_width=True):
        st.session_state.weights = {cat: 1 for cat in categories}
        st.session_state.click_history = []
        st.rerun()
