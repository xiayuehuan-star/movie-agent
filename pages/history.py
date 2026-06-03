import streamlit as st

def main():
    st.markdown("""
    <style>
    .history-item {
        background: white;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        border: 1px solid #E8E4DF;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.2s ease;
    }
    .history-item:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .history-keyword {
        font-size: 1rem;
        font-weight: 500;
        color: #2C2C2C;
    }
    .history-meta {
        font-size: 0.85rem;
        color: #6B6B6B;
        margin-top: 4px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("📖 浏览历史")
    
    if st.session_state.history:
        for idx, item in enumerate(st.session_state.history):
            st.markdown('<div class="history-item">', unsafe_allow_html=True)
            st.markdown(f"""
                <div>
                    <div class="history-keyword">🔍 {item.get('keyword', '')}</div>
                    <div class="history-meta">返回 {item.get('results_count', 0)} 条结果</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button('搜索', key=f"history_search_{idx}", use_container_width=False):
                st.session_state.recommendations = []
                from utils.tmdb_api import generate_recommendations
                results = generate_recommendations(item.get('keyword', ''))
                st.session_state.recommendations = results
                st.session_state.page = "home"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 80px 20px;">
            <span style="font-size: 5rem; opacity: 0.5;">📜</span>
            <h3 style="margin-top: 20px; color: #2C2C2C;">还没有浏览记录</h3>
            <p style="color: #6B6B6B;">开始搜索影视推荐吧</p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.history:
        if st.button("清空历史", use_container_width=True):
            st.session_state.history = []
            st.rerun()