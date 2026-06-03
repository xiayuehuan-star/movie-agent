import streamlit as st
import os
import json

st.set_page_config(
    page_title="今日片单",
    page_icon="🎬",
    layout="wide"
)

def load_session_state():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "favorites" not in st.session_state:
        st.session_state.favorites = load_json("favorites.json", [])
    if "history" not in st.session_state:
        st.session_state.history = load_json("history.json", [])
    if "profile" not in st.session_state:
        st.session_state.profile = load_json("profile.json", {
            "favorite_genres": [],
            "favorite_character_types": [],
            "favorite_countries": [],
            "favorite_actors": [],
            "favorite_directors": [],
            "watch_count": 0,
            "favorite_movies": []
        })

def load_json(filepath, default):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return default
    return default

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    load_session_state()
    
    st.sidebar.title("🎬 今日片单")
    st.sidebar.markdown("---")
    
    pages = {
        "首页": "home",
        "我的收藏": "favorites",
        "用户画像": "profile",
        "浏览历史": "history"
    }
    
    for page_name, page_key in pages.items():
        if st.sidebar.button(page_name, key=f"nav_{page_key}", use_container_width=True):
            st.session_state.page = page_key
            save_json("favorites.json", st.session_state.favorites)
            save_json("history.json", st.session_state.history)
            save_json("profile.json", st.session_state.profile)
    
    if st.session_state.page == "home":
        from pages import home
        home.render()
    elif st.session_state.page == "favorites":
        from pages import favorites
        favorites.render()
    elif st.session_state.page == "profile":
        from pages import profile
        profile.render()
    elif st.session_state.page == "history":
        from pages import history
        history.render()

if __name__ == "__main__":
    main()