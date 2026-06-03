import streamlit as st

def main():
    st.markdown("""
    <style>
    .profile-section {
        background: white;
        border-radius: 12px;
        padding: 32px;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #E8E4DF;
    }
    .profile-header {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 24px;
        padding-bottom: 20px;
        border-bottom: 1px solid #E8E4DF;
    }
    .profile-avatar {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: linear-gradient(135deg, #D4A574, #C4956A);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
    }
    .stats-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        gap: 20px;
        margin-bottom: 24px;
    }
    .stat-card {
        background: #FAF8F5;
        border-radius: 8px;
        padding: 14px;
        text-align: center;
    }
    .stat-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #D4A574;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #6B6B6B;
        margin-top: 4px;
    }
    .tags-section {
        margin-bottom: 20px;
    }
    .tags-title {
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 10px;
        color: #2C2C2C;
    }
    .tags {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }
    .tag {
        padding: 5px 12px;
        font-size: 0.85rem;
        background-color: rgba(212, 165, 116, 0.12);
        color: #8B6914;
        border-radius: 6px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    profile = st.session_state.profile
    
    st.markdown('<div class="profile-section">', unsafe_allow_html=True)
    st.markdown("""
        <div class="profile-header">
            <div class="profile-avatar">👤</div>
            <div>
                <h2 style="font-size: 1.4rem; margin: 0 0 4px 0;">我的影视画像</h2>
                <p style="color: #6B6B6B; margin: 0; font-size: 0.95rem;">基于您的收藏和浏览记录生成</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-value">{}</div>
                <div class="stat-label">收藏作品</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{}</div>
                <div class="stat-label">搜索次数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{}</div>
                <div class="stat-label">喜欢题材</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{}</div>
                <div class="stat-label">人物类型</div>
            </div>
        </div>
    """.format(
        len(st.session_state.favorites),
        len(st.session_state.history),
        len(profile.get("favorite_genres", [])),
        len(profile.get("favorite_character_types", []))
    ), unsafe_allow_html=True)
    
    st.markdown('<div class="tags-section">', unsafe_allow_html=True)
    st.markdown('<div class="tags-title">🎬 喜欢的题材</div>', unsafe_allow_html=True)
    st.markdown('<div class="tags">', unsafe_allow_html=True)
    genres = profile.get("favorite_genres", [])
    if genres:
        for genre in genres:
            st.markdown(f'<span class="tag">{genre}</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span style="color: #6B6B6B;">暂无</span>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="tags-section">', unsafe_allow_html=True)
    st.markdown('<div class="tags-title">👥 喜欢的人物类型</div>', unsafe_allow_html=True)
    st.markdown('<div class="tags">', unsafe_allow_html=True)
    chars = profile.get("favorite_character_types", [])
    if chars:
        for char in chars:
            st.markdown(f'<span class="tag">{char}</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span style="color: #6B6B6B;">暂无</span>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="tags-section">', unsafe_allow_html=True)
    st.markdown('<div class="tags-title">🌍 喜欢的国家地区</div>', unsafe_allow_html=True)
    st.markdown('<div class="tags">', unsafe_allow_html=True)
    countries = profile.get("favorite_countries", [])
    if countries:
        for country in countries:
            st.markdown(f'<span class="tag">{country}</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span style="color: #6B6B6B;">暂无</span>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="tags-section">', unsafe_allow_html=True)
    st.markdown('<div class="tags-title">🎭 喜欢的演员</div>', unsafe_allow_html=True)
    st.markdown('<div class="tags">', unsafe_allow_html=True)
    actors = profile.get("favorite_actors", [])
    if actors:
        for actor in actors:
            st.markdown(f'<span class="tag">{actor}</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span style="color: #6B6B6B;">暂无</span>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="tags-section">', unsafe_allow_html=True)
    st.markdown('<div class="tags-title">🎬 喜欢的导演</div>', unsafe_allow_html=True)
    st.markdown('<div class="tags">', unsafe_allow_html=True)
    directors = profile.get("favorite_directors", [])
    if directors:
        for director in directors:
            st.markdown(f'<span class="tag">{director}</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span style="color: #6B6B6B;">暂无</span>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)