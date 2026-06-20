import streamlit as st
import random
import pandas as pd
import feedparser
import urllib.parse
import re

# -----------------------
# 페이지 설정 
# -----------------------
st.set_page_config(page_title="추천 알고리즘 버블 체험", page_icon="🫧", layout="wide")

# -----------------------
# 세션 상태 초기화 및 관리
# -----------------------
default_categories = ["스포츠", "정치", "게임", "연예", "사건사고", "교육"]

if "categories" not in st.session_state:
    st.session_state.categories = default_categories.copy()

if "weights" not in st.session_state:
    st.session_state.weights = {cat: 1 for cat in st.session_state.categories}

if "click_history" not in st.session_state:
    st.session_state.click_history = []

if "selected_article" not in st.session_state:
    st.session_state.selected_article = None

# --- 버튼 클릭 시 즉시 실행되는 콜백(Callback) 함수들 ---
def click_content(item):
    cat = item["category"]
    st.session_state.click_history.append(cat)
    st.session_state.weights[cat] += 3
    st.session_state.selected_article = item 

def close_article():
    st.session_state.selected_article = None

def reset_all():
    st.session_state.categories = default_categories.copy()
    st.session_state.weights = {cat: 1 for cat in st.session_state.categories}
    st.session_state.click_history = []
    st.session_state.selected_article = None

def break_bubble():
    kw = st.session_state.get("new_keyword", "").strip()
    sel = st.session_state.get("new_select", "선택안함")
    target = kw if kw else (sel if sel != "선택안함" else "")
    
    if target:
        if target not in st.session_state.categories:
            st.session_state.categories.append(target)
        
        st.session_state.weights = {cat: 1 for cat in st.session_state.categories}
        st.session_state.weights[target] = 5
        st.session_state.click_history = []
        st.session_state.selected_article = None
# --------------------------------------------------------

# -----------------------
# 구글 뉴스 RSS 연동 함수 (캐싱 적용)
# -----------------------
@st.cache_data(ttl=1800, show_spinner=False)
def fetch_google_news(category, is_extreme):
    search_query = category
    if is_extreme:
        search_query += " (논란 OR 충격 OR 분노 OR 단독 OR 의혹)"
    
    encoded_query = urllib.parse.quote(search_query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    
    try:
        feed = feedparser.parse(rss_url)
        news_data = []
        for entry in feed.entries[:20]:
            clean_title = re.sub(r' - .+$', '', entry.title)
            news_data.append({
                "title": clean_title,
                "link": entry.link
            })
        return news_data if news_data else None
    except Exception as e:
        return None

# -----------------------
# 기사 제목 데이터베이스 (안전장치용 더미 데이터)
# -----------------------
normal_titles = {
    "스포츠": ["⚽ 손흥민, 경기 MVP 선정", "🏀 NBA 플레이오프 명승부", "⚾ 프로야구 순위 경쟁 치열"],
    "정치": ["🗳️ 정책 토론 주요 쟁점", "📢 사회 현안 논의 확대", "🏛️ 정부 정책 발표"],
    "게임": ["🎮 신작 게임 출시 기대감", "🔥 인기 게임 e스포츠 대회 개최", "🕹️ 게이밍 트렌드 변화 분석"],
    "연예": ["🎤 인기 아이돌 성공적인 컴백", "🎬 화제의 웹드라마 전편 공개", "📺 주말 예능 프로그램 시청률 1위"],
    "교육": ["📚 AI 시대가 바꾸는 교실 풍경", "🧠 뇌과학 기반 효과적인 공부법 연구", "💡 10년 뒤 미래 직업 변화 전망"],
    "사건사고": ["경찰, 대규모 보이스피싱 일당 검거", "주말 고속도로 다중 추돌 사고", "전국적인 집중 호우 대비 태세"]
}

extreme_titles = {
    "스포츠": ["⚽ 충격! 대표팀 대참사", "🏀 역대급 오심 논란, 팬들 분노"],
    "정치": ["🚨 정치권 초비상 사태", "🔥 국민 여론 폭발, 대규모 시위 예고"],
    "게임": ["🎮 역대급 게임 중독 논란 확산", "🔥 서버 터짐! 유저들 분노 폭발"],
    "연예": ["😱 연예계 발칵 뒤집힌 충격 소식", "🔥 팬들 멘붕, 단독 열애설 포착"],
    "교육": ["🚨 AI가 모든 교사를 완전히 대체한다?", "😱 10년 후 완전히 멸종할 직업 리스트"],
    "사건사고": ["🚨 충격 단독! 전 국민이 속고 있었다", "😱 충격적인 흉악 범죄 발생, 시민들 불안"]
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
    for cat in st.session_state.categories:
        weighted_categories.extend([cat] * st.session_state.weights[cat])
    
    if not weighted_categories:
        return []

    chosen_categories = random.choices(weighted_categories, k=6)
    cat_counts = {cat: chosen_categories.count(cat) for cat in set(chosen_categories)}
    
    feed = []
    for cat, count in cat_counts.items():
        news_pool = fetch_google_news(cat, is_extreme)
        
        if not news_pool or len(news_pool) < count:
            if cat in normal_titles:
                titles_pool = extreme_titles[cat] if is_extreme else normal_titles[cat]
            else:
                titles_pool = [f"📰 [{cat}] 관련 최신 뉴스", f"🔍 [{cat}]에 대한 심층 분석", f"💡 [{cat}] 전문가 의견", f"📈 [{cat}] 관련 이슈 트렌드"]

            sampled_titles = random.sample(titles_pool, count) if count <= len(titles_pool) else random.choices(titles_pool, k=count)
            sampled_news = [{"title": t
