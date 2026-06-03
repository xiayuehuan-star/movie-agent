import streamlit as st

def main():
    st.markdown("""
    <style>
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
        height: 180px;
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
        padding: 18px;
    }
    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2C2C2C;
        margin-bottom: 8px;
    }
    .card-meta {
        display: flex;
        gap: 12px;
        margin-bottom: 12px;
        font-size: 0.85rem;
        color: #6B6B6B;
    }
    .card-rating {
        padding: 3px 8px;
        background-color: rgba(212, 165, 116, 0.15);
        color: #8B6914;
        border-radius: 5px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .tags-container {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        margin-bottom: 12px;
    }
    .tag {
        padding: 3px 8px;
        font-size: 0.75rem;
        border-radius: 3px;
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
        font-size: 0.85rem;
        color: #6B6B6B;
        line-height: 1.6;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("❤️ 我的收藏")
    st.write(f"共收藏了 {len(st.session_state.favorites)} 部作品")
    
    if st.session_state.favorites:
        cols = st.columns(3)
        for idx, movie in enumerate(st.session_state.favorites):
            with cols[idx % 3]:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                
                poster_url = movie.get("poster", "")
                if poster_url and poster_url.startswith("https://"):
                    st.markdown(f'<div class="card-poster"><img src="{poster_url}" alt="海报" onError="this.style.display=\'none\'; this.parentElement.innerHTML=\'<span style=font-size:3rem;opacity:0.5;>🎬</span>\'"></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="card-poster"><span style="font-size: 3rem; opacity: 0.5;">🎬</span></div>', unsafe_allow_html=True)
                
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
                
                if st.button('🗑️ 移除收藏', key=f"remove_{movie.get('title', idx)}", use_container_width=True):
                    st.session_state.favorites = [f for f in st.session_state.favorites if f.get("title") != movie.get("title")]
                    st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 80px 20px;">
            <span style="font-size: 5rem; opacity: 0.5;">📭</span>
            <h3 style="margin-top: 20px; color: #2C2C2C;">还没有收藏</h3>
            <p style="color: #6B6B6B;">去发现精彩作品并收藏吧</p>
        </div>
        """, unsafe_allow_html=True)