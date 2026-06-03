import streamlit as st

def render_search():
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "",
            placeholder="输入关键词，如：悬疑、治愈、烧脑...",
            label_visibility="hidden"
        )
    
    with col2:
        search_btn = st.button("获取推荐", use_container_width=True)
    
    return user_input if search_btn else None