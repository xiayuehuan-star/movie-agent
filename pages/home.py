import streamlit as st
from utils.tmdb_api import generate_recommendations

def main():
    st.markdown("""
    <style>
    .hero-section {
        text-align: center;
        padding: 60px 20px 40px;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        color: #2C2C2C;
        margin-bottom: 12px;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        font-size: 1.25rem;
        color: #6B6B6B;
        font-weight: 400;
    }
    .card {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #E8E4DF;
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }
    .card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    .card-poster {
        width: 100%;
        height: 200px;
        background: linear-gradient(135deg, #F5EEE6 0%, #E8E4DF 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }
    .card-poster img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .card-content {
        padding: 20px;
    }
    .card-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #2C2C2C;
        margin-bottom: 8px;
    }
    .card-meta {
        display: flex;
        gap: 12px;
        margin-bottom: 14px;
        font-size: 0.9rem;
        color: #6B6B6B;
    }
    .card-rating {
        padding: 4px 10px;
        background-color: rgba(212, 165, 116, 0.15);
        color: #8B6914;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .tags-container {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 14px;
    }
    .tag {
        padding: 4px 10px;
        font-size: 0.78rem;
        border-radius: 4px;
        font-weight: 500;
    }
    .tag-character {
        background-color: #F5EEE6;
        color: #8B6914;
    }
    .tag-story {
        background-color: #E8F0F5;
        color: #2C5F7C;
    }
    .card-reason {
        font-size: 0.9rem;
        color: #6B6B6B;
        line-height: 1.65;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">妈妈，我想看这个！</h1>
        <p class="hero-subtitle">发现下一部属于你的好作品</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "",
            placeholder="输入关键词，如：悬疑、治愈、烧脑...",
            label_visibility="hidden"
        )
    
    with col2:
        search_btn = st.button("获取推荐", use_container_width=True)
    
    if search_btn and user_input:
        with st.spinner("正在搜索..."):
            results = generate_recommendations(user_input)
            
            if results:
                if "history" not in st.session_state:
                    st.session_state.history = []
                st.session_state.history.insert(0, {
                    "keyword": user_input,
                    "timestamp": st.session_state.get("history_timestamp", 0),
                    "results_count": len(results)
                })
                if len(st.session_state.history) > 20:
                    st.session_state.history = st.session_state.history[:20]
            
            st.session_state.recommendations = results
    
    if "recommendations" in st.session_state and st.session_state.recommendations:
        cols = st.columns(3)
        for idx, movie in enumerate(st.session_state.recommendations):
            with cols[idx % 3]:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                
                poster_url = movie.get("poster", "")
                if poster_url and poster_url.startswith("https://"):
                    st.markdown(f'<div class="card-poster"><img src="{poster_url}" alt="海报" onError="this.style.display=\'none\'; this.parentElement.innerHTML=\'<span style=font-size:3.5rem;opacity:0.5;>🎬</span>\'"></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="card-poster"><span style="font-size: 3.5rem; opacity: 0.5;">🎬</span></div>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="card-content">', unsafe_allow_html=True)
                st.markdown(f'<h3 class="card-title">{movie.get("title", "未知")}</h3>', unsafe_allow_html=True)
                
                year = movie.get("year", "")
                rating = movie.get("rating", "")
                meta_parts = []
                if year:
                    meta_parts.append(f"📅 {year}")
                if rating:
                    meta_parts.append(f'<span class="card-rating">⭐ {rating}</span>')
                if meta_parts:
                    st.markdown(f'<div class="card-meta">{" ".join(meta_parts)}</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="tags-container">', unsafe_allow_html=True)
                for tag in movie.get("character_tags", []):
                    st.markdown(f'<span class="tag tag-character">{tag}</span>', unsafe_allow_html=True)
                for tag in movie.get("story_tags", []):
                    st.markdown(f'<span class="tag tag-story">{tag}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown(f'<p class="card-reason">{movie.get("reason", "")}</p>', unsafe_allow_html=True)
                
                col_fav, col_info = st.columns([1, 2])
                with col_fav:
                    is_fav = any(f.get("title") == movie.get("title") for f in st.session_state.favorites)
                    if st.button('❤️' if is_fav else '🤍', key=f"fav_{movie.get('title', idx)}", use_container_width=True):
                        if is_fav:
                            st.session_state.favorites = [f for f in st.session_state.favorites if f.get("title") != movie.get("title")]
                        else:
                            st.session_state.favorites.append(movie)
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 80px 20px;">
            <span style="font-size: 5rem; opacity: 0.5;">🍿</span>
            <h3 style="margin-top: 20px; color: #2C2C2C;">还没有推荐内容</h3>
            <p style="color: #6B6B6B;">输入关键词开始探索</p>
        </div>
        """, unsafe_allow_html=True)