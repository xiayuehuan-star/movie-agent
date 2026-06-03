import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "9b80341cb9048da39b7c897fdf43b024")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def search_tmdb_movies(query):
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "zh-CN",
        "page": 1
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception as e:
        print(f"TMDB电影搜索失败: {e}")
        return []

def search_tmdb_tv(query):
    url = f"{TMDB_BASE_URL}/search/tv"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "zh-CN",
        "page": 1
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception as e:
        print(f"TMDB剧集搜索失败: {e}")
        return []

def get_movie_details(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "zh-CN"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"获取电影详情失败: {e}")
        return None

def get_tv_details(tv_id):
    url = f"{TMDB_BASE_URL}/tv/{tv_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "zh-CN"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"获取剧集详情失败: {e}")
        return None

def generate_recommendations(user_input):
    results = []
    
    movie_results = search_tmdb_movies(user_input)
    tv_results = search_tmdb_tv(user_input)
    
    all_results = []
    
    for item in movie_results[:6]:
        details = get_movie_details(item["id"])
        if details:
            poster_url = f"https://image.tmdb.org/t/p/w500{details.get('poster_path', '')}" if details.get('poster_path') else ""
            all_results.append({
                "title": details.get("title", item.get("title", "未知")),
                "year": details.get("release_date", "")[:4] if details.get("release_date") else "",
                "rating": str(round(details.get("vote_average", 0), 1)),
                "poster": poster_url,
                "overview": details.get("overview", ""),
                "type": "movie",
                "source": "tmdb"
            })
    
    for item in tv_results[:6]:
        details = get_tv_details(item["id"])
        if details:
            poster_url = f"https://image.tmdb.org/t/p/w500{details.get('poster_path', '')}" if details.get('poster_path') else ""
            all_results.append({
                "title": details.get("name", item.get("name", "未知")),
                "year": details.get("first_air_date", "")[:4] if details.get("first_air_date") else "",
                "rating": str(round(details.get("vote_average", 0), 1)),
                "poster": poster_url,
                "overview": details.get("overview", ""),
                "type": "tv",
                "source": "tmdb"
            })
    
    seen_titles = set()
    filtered_results = []
    for item in all_results:
        if item["title"] not in seen_titles:
            seen_titles.add(item["title"])
            filtered_results.append(item)
    
    results = filtered_results[:10]
    
    for item in results:
        item["character_tags"] = generate_character_tags(item, user_input)
        item["story_tags"] = generate_story_tags(item, user_input)
        item["reason"] = generate_reason(item, user_input)
    
    if len(results) < 10:
        remaining = 10 - len(results)
        mock_data = get_fallback_recommendations(user_input, remaining)
        results.extend(mock_data)
    
    return results

def generate_character_tags(item, user_input):
    keywords = ["主角", "反派", "英雄", "侦探", "警察", "医生", "普通人"]
    if "悬疑" in user_input or "破案" in user_input:
        return ["侦探", "罪犯", "目击者"]
    elif "爱情" in user_input:
        return ["恋人", "追求者", "情敌"]
    elif "喜剧" in user_input:
        return ["搞笑担当", "笨角色", "机智者"]
    elif "动作" in user_input:
        return ["硬汉", "特工", "反派Boss"]
    else:
        return ["主角", "配角", "关键人物"]

def generate_story_tags(item, user_input):
    if "悬疑" in user_input or "烧脑" in user_input:
        return ["悬疑推理", "谜团", "反转"]
    elif "治愈" in user_input or "温暖" in user_input:
        return ["治愈系", "温情", "成长"]
    elif "喜剧" in user_input or "搞笑" in user_input:
        return ["喜剧", "搞笑", "轻松"]
    elif "动作" in user_input or "冒险" in user_input:
        return ["动作", "冒险", "刺激"]
    elif "爱情" in user_input:
        return ["爱情", "浪漫", "情感"]
    elif "恐怖" in user_input:
        return ["恐怖", "惊悚", "悬疑"]
    else:
        return ["剧情", "情感", "人生"]

def generate_reason(item, user_input):
    title = item.get("title", "这部作品")
    overview = item.get("overview", "")
    
    if "悬疑" in user_input or "烧脑" in user_input:
        reason = f"《{title}》是一部扣人心弦的悬疑作品。{overview[:50]}... 剧情层层递进，充满悬念和反转，非常适合喜欢烧脑推理的观众。"
    elif "治愈" in user_input or "温暖" in user_input:
        reason = f"《{title}》是一部温暖治愈的作品。{overview[:50]}... 剧情温馨感人，充满正能量，能给人带来心灵的慰藉。"
    elif "喜剧" in user_input or "搞笑" in user_input:
        reason = f"《{title}》是一部轻松搞笑的喜剧。{overview[:50]}... 笑点密集，轻松愉快，是放松心情的好选择。"
    elif "动作" in user_input or "冒险" in user_input:
        reason = f"《{title}》是一部刺激的动作冒险作品。{overview[:50]}... 场面宏大，动作戏精彩，让人热血沸腾。"
    elif "爱情" in user_input:
        reason = f"《{title}》是一部浪漫的爱情作品。{overview[:50]}... 情感真挚动人，是一部值得一看的爱情佳作。"
    else:
        reason = f"《{title}》是一部优秀的影视作品。{overview[:80]}... 剧情精彩，制作精良，值得一看。"
    
    return reason

def get_fallback_recommendations(user_input, count):
    fallback_data = [
        {
            "title": "盗梦空间",
            "year": "2010",
            "rating": "9.3",
            "poster": "https://neeko-copilot.bytedance.net/api/text_to_image?prompt=inception%20movie%20poster%20dream%20sci-fi%20cinematic&image_size=portrait_4_3",
            "character_tags": ["梦境行者", "执念者", "领导者"],
            "story_tags": ["科幻", "悬疑", "意识探索"],
            "reason": f"《盗梦空间》是诺兰的科幻巨作。如果你喜欢{user_input}类型的作品，这部电影将带你进入一个多层梦境的世界，挑战你的想象力和逻辑思维能力。",
            "source": "fallback"
        },
        {
            "title": "肖申克的救赎",
            "year": "1994",
            "rating": "9.7",
            "poster": "https://neeko-copilot.bytedance.net/api/text_to_image?prompt=shawshank%20redemption%20prison%20hope%20cinematic&image_size=portrait_4_3",
            "character_tags": ["囚徒", "智者", "希望追寻者"],
            "story_tags": ["救赎", "希望", "友情"],
            "reason": f"《肖申克的救赎》是影史经典。这部电影讲述了一个关于希望和救赎的故事，即使在最黑暗的环境中，也能找到光明。非常适合喜欢{user_input}题材的观众。",
            "source": "fallback"
        },
        {
            "title": "阿甘正传",
            "year": "1994",
            "rating": "9.5",
            "poster": "https://neeko-copilot.bytedance.net/api/text_to_image?prompt=forrest%20gump%20running%20life%20journey%20cinematic&image_size=portrait_4_3",
            "character_tags": ["纯真者", "奋斗者", "幸运儿"],
            "story_tags": ["成长", "励志", "人生"],
            "reason": f"《阿甘正传》是一部温暖人心的作品。阿甘用他的纯真和坚持，创造了一个又一个奇迹。这部电影充满正能量，适合喜欢{user_input}类型的观众。",
            "source": "fallback"
        },
        {
            "title": "星际穿越",
            "year": "2014",
            "rating": "9.4",
            "poster": "https://neeko-copilot.bytedance.net/api/text_to_image?prompt=interstellar%20space%20black%20hole%20sci-fi%20cinematic&image_size=portrait_4_3",
            "character_tags": ["宇航员", "科学家", "父亲"],
            "story_tags": ["科幻", "亲情", "时空"],
            "reason": f"《星际穿越》是一部震撼的科幻史诗。诺兰再次展现了他对宏大叙事的掌控力，影片探讨了爱与时间的关系，视觉效果令人叹为观止。",
            "source": "fallback"
        },
        {
            "title": "千与千寻",
            "year": "2001",
            "rating": "9.4",
            "poster": "https://neeko-copilot.bytedance.net/api/text_to_image?prompt=spirited%20away%20anime%20fantasy%20bathhouse%20studio%20ghibli&image_size=portrait_4_3",
            "character_tags": ["少女", "妖怪", "守护者"],
            "story_tags": ["奇幻", "成长", "冒险"],
            "reason": f"《千与千寻》是宫崎骏的经典动画。这部电影充满想象力，讲述了少女千寻在神灵世界的冒险故事，画面精美，寓意深刻。",
            "source": "fallback"
        }
    ]
    
    return fallback_data[:count]