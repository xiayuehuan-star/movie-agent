import streamlit as st

def render_header():
    st.markdown("""
    <div style="padding: 60px 20px 40px; text-align: center;">
        <h1 class="header-title">妈妈，我想看这个！</h1>
        <p class="header-subtitle">发现下一部属于你的好作品</p>
    </div>
    """, unsafe_allow_html=True)