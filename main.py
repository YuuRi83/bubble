# API 실패 시 더미 데이터로 대체
        if not news_pool or len(news_pool) < count:
            if cat in normal_titles:
                titles_pool = extreme_titles[cat] if is_extreme else normal_titles[cat]
            else:
                titles_pool = [f"📰 [{cat}] 관련 최신 뉴스", f"🔍 [{cat}]에 대한 심층 분석", f"💡 [{cat}] 전문가 의견", f"📈 [{cat}] 관련 이슈 트렌드"]

            sampled_titles = random.sample(titles_pool, count) if count <= len(titles_pool) else random.choices(titles_pool, k=count)
            
            # 👇 바로 이 부분입니다! 끝에 닫는 괄호(])까지 잘 들어가야 합니다.
            sampled_news = [{"title": t, "link": "https://news.google.com"} for t in sampled_titles]
        else:
            sampled_news = random.sample(news_pool, count) if count <= len(news_pool) else random.choices(news_pool, k=count)
