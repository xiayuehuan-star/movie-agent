import streamlit as st

def render_cards(movie_list, show_fav_button=True):
    if not movie_list:
        st.markdown("""
        <div class="empty-state">
            <span class="empty-icon">🍿</span>
            <h3>还没有推荐内容</h3>
            <p>输入关键词开始探索</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    cols = st.columns(3)
    
    for idx, movie in enumerate(movie_list):
        with cols[idx % 3]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            poster_url = movie.get("poster", "")
            has_poster = poster_url and poster_url.startswith("https://")
            
            if has_poster:
                st.markdown(f'''
                <div class="card-poster">
                    <img src="{poster_url}" alt="{movie.get("title", "海报")}" class="poster-img" onError="this.style.display='none'; this.parentElement.classList.add('placeholder'); this.parentElement.innerHTML='<span class=\'poster-icon\'>🎬</span>';">
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown('''
                <div class="card-poster placeholder">
                    <span class="poster-icon">🎬</span>
                </div>
                ''', unsafe_allow_html=True)
            
            st.markdown(f'<h3 class="card-title">{movie.get("title", "未知")}</h3>', unsafe_allow_html=True)
            
            year = movie.get("year", "")
            rating = movie.get("rating", "")
            
            meta_parts = []
            if year:
                meta_parts.append(f"📅 {year}")
            if rating:
                meta_parts.append(f'<span class="card-rating">⭐ {rating}</span>')
            
            if meta_parts:
                meta_html = ' '.join(meta_parts)
                st.markdown(f'<div class="card-meta">{meta_html}</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="tags-container">', unsafe_allow_html=True)
            for tag in movie.get("character_tags", []):
                st.markdown(f'<span class="tag tag-character">{tag}</span>', unsafe_allow_html=True)
            for tag in movie.get("story_tags", []):
                st.markdown(f'<span class="tag tag-story">{tag}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            reason = movie.get("reason", "")
            st.markdown(f'<p class="card-reason">{reason}</p>', unsafe_allow_html=True)
            
            if show_fav_button:
                is_fav = movie.get("is_favorite", False)
                fav_key = f"fav_{movie.get('title', idx)}"
                if st.button('❤️' if is_fav else '🤍', key=fav_key, use_container_width=True):
                    st.session_state.fav_action = {
                        'title': movie.get('title'),
                        'movie': movie,
                        'action': 'remove' if is_fav else 'add'
                    }
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)