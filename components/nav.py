import streamlit as st

def render_nav(current_page):
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown('<span class="navbar-brand">🎬 今日片单</span>', unsafe_allow_html=True)
    
    with col2:
        nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])
        
        with nav_col1:
            if st.button("首页", key="nav_home", use_container_width=True):
                st.session_state.page = "home"
                st.rerun()
        
        with nav_col2:
            if st.button("我的收藏", key="nav_favorites", use_container_width=True):
                st.session_state.page = "favorites"
                st.rerun()
        
        with nav_col3:
            if st.button("用户画像", key="nav_profile", use_container_width=True):
                st.session_state.page = "profile"
                st.rerun()