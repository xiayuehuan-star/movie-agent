import streamlit as st

def apply_styles():
    st.set_page_config(
        page_title="今日片单",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    css = """
    <style>
    :root {
        --bg-color: #FAF8F5;
        --card-bg: #FFFFFF;
        --text-color: #2C2C2C;
        --subtext-color: #6B6B6B;
        --accent-color: #D4A574;
        --accent-light: #E8D4BC;
        --border-color: #E8E4DF;
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.06);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.08);
        --radius: 12px;
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Microsoft YaHei', 'PingFang SC', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: var(--bg-color);
        color: var(--text-color);
        line-height: 1.6;
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 700;
        color: var(--text-color);
        margin-bottom: 12px;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    
    .header-subtitle {
        font-size: 1.25rem;
        color: var(--subtext-color);
        font-weight: 400;
    }
    
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 24px;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid var(--border-color);
        position: sticky;
        top: 0;
        z-index: 100;
    }
    
    .navbar-brand {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-color);
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .nav-links {
        display: flex;
        gap: 20px;
    }
    
    .nav-link {
        font-size: 0.95rem;
        color: var(--subtext-color);
        text-decoration: none;
        padding: 8px 14px;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    .nav-link:hover {
        background-color: rgba(0, 0, 0, 0.05);
        color: var(--text-color);
    }
    
    .nav-link.active {
        color: var(--accent-color);
        font-weight: 600;
        background-color: rgba(212, 165, 116, 0.1);
    }
    
    .navbar-button {
        font-size: 0.95rem;
        color: var(--subtext-color);
        background: transparent;
        border: none;
        padding: 8px 14px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        font-family: inherit;
        text-align: center;
    }
    
    .navbar-button:hover {
        background-color: rgba(0, 0, 0, 0.05);
        color: var(--text-color);
    }
    
    .search-input {
        padding: 14px 24px;
        font-size: 16px;
        border: 1px solid var(--border-color);
        border-radius: 32px;
        background-color: var(--card-bg);
        width: 100%;
        max-width: 500px;
        outline: none;
        transition: all 0.3s ease;
    }
    
    .search-input:focus {
        border-color: var(--accent-color);
        box-shadow: 0 0 0 3px rgba(212, 165, 116, 0.1);
    }
    
    .search-btn {
        padding: 14px 32px;
        font-size: 16px;
        font-weight: 600;
        color: white;
        background-color: var(--text-color);
        border: none;
        border-radius: 32px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .search-btn:hover {
        background-color: #1a1a1a;
        transform: translateY(-1px);
    }
    
    .card {
        background: var(--card-bg);
        border-radius: var(--radius);
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }
    
    .card-poster {
        width: 100%;
        height: 200px;
        overflow: hidden;
        background: linear-gradient(135deg, #F5EEE6 0%, #E8E4DF 100%);
    }
    
    .card-poster.placeholder {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .poster-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
    }
    
    .card:hover .poster-img {
        transform: scale(1.02);
    }
    
    .poster-icon {
        font-size: 3.5rem;
        opacity: 0.5;
    }
    
    .card-content {
        padding: 20px;
    }
    
    .card-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-color);
        margin-bottom: 8px;
    }
    
    .card-meta {
        display: flex;
        gap: 12px;
        margin-bottom: 14px;
        font-size: 0.9rem;
        color: var(--subtext-color);
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
        color: var(--subtext-color);
        line-height: 1.65;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    
    .empty-state {
        text-align: center;
        padding: 60px 20px;
    }
    
    .empty-icon {
        font-size: 4rem;
        margin-bottom: 16px;
        opacity: 0.6;
    }
    
    .profile-section {
        background: var(--card-bg);
        border-radius: var(--radius);
        padding: 32px;
        margin-bottom: 24px;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
    }
    
    .profile-header {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 24px;
        padding-bottom: 20px;
        border-bottom: 1px solid var(--border-color);
    }
    
    .profile-avatar {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--accent-color), #C4956A);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
    }
    
    .profile-info h2 {
        font-size: 1.4rem;
        margin: 0 0 4px 0;
    }
    
    .profile-info p {
        color: var(--subtext-color);
        margin: 0;
        font-size: 0.95rem;
    }
    
    .stats-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        gap: 20px;
        margin-bottom: 24px;
    }
    
    .stat-card {
        background: var(--bg-color);
        border-radius: 8px;
        padding: 14px;
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--accent-color);
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: var(--subtext-color);
        margin-top: 4px;
    }
    
    .profile-tags-section {
        margin-bottom: 20px;
    }
    
    .profile-tags-title {
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 10px;
        color: var(--text-color);
    }
    
    .profile-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }
    
    .profile-tag {
        padding: 5px 12px;
        font-size: 0.85rem;
        background-color: rgba(212, 165, 116, 0.12);
        color: #8B6914;
        border-radius: 6px;
    }
    
    .footer {
        text-align: center;
        padding: 40px 20px;
        border-top: 1px solid var(--border-color);
        margin-top: 40px;
        color: var(--subtext-color);
        font-size: 0.9rem;
    }
    
    @media (max-width: 768px) {
        .header-title {
            font-size: 2.2rem;
        }
        
        .navbar {
            padding: 12px 16px;
        }
        
        .nav-links {
            gap: 12px;
        }
        
        .card-poster {
            height: 180px;
        }
    }
    
    @media (max-width: 480px) {
        .header-title {
            font-size: 1.8rem;
        }
    }
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)