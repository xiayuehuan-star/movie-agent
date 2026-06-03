import json
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

FAVORITES_FILE = "favorites.json"
PROFILE_FILE = "profile.json"

class MovieRecommendationAgent:
    def __init__(self):
        self.tmdb_api_key = TMDB_API_KEY
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1"
        )
        self.favorites = self._load_favorites()
        self.profile = self._load_profile()
    
    def _load_favorites(self):
        if os.path.exists(FAVORITES_FILE):
            try:
                with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_favorites(self):
        with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.favorites, f, ensure_ascii=False, indent=2)
    
    def _load_profile(self):
        if os.path.exists(PROFILE_FILE):
            try:
                with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._create_default_profile()
        return self._create_default_profile()
    
    def _create_default_profile(self):
        return {
            "favorite_genres": [],
            "favorite_character_types": [],
            "favorite_countries": [],
            "favorite_actors": [],
            "favorite_directors": [],
            "watch_count": 0,
            "favorite_movies": []
        }
    
    def _save_profile(self):
        with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.profile, f, ensure_ascii=False, indent=2)
    
    def _call_ai(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"AI调用失败: {e}")
            return None
    
    def _tmdb_search_movies(self, query, page=1):
        url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            "api_key": self.tmdb_api_key,
            "query": query,
            "page": page,
            "language": "zh-CN"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"TMDB搜索失败: {e}")
            return None
    
    def _tmdb_search_tv(self, query, page=1):
        url = f"{TMDB_BASE_URL}/search/tv"
        params = {
            "api_key": self.tmdb_api_key,
            "query": query,
            "page": page,
            "language": "zh-CN"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"TMDB剧集搜索失败: {e}")
            return None
    
    def _tmdb_get_movie_details(self, movie_id):
        url = f"{TMDB_BASE_URL}/movie/{movie_id}"
        params = {
            "api_key": self.tmdb_api_key,
            "language": "zh-CN"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"TMDB获取电影详情失败: {e}")
            return None
    
    def _tmdb_get_tv_details(self, tv_id):
        url = f"{TMDB_BASE_URL}/tv/{tv_id}"
        params = {
            "api_key": self.tmdb_api_key,
            "language": "zh-CN"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"TMDB获取剧集详情失败: {e}")
            return None
    
    def _generate_tags_and_reason(self, movie_info, user_input):
        prompt = f"""
        请为以下影视作品生成推荐信息：
        
        作品名：{movie_info['title']}
        简介：{movie_info['overview']}
        
        用户输入：{user_input}
        
        请输出JSON格式，包含：
        {{
            "character_tags": ["人物标签1", "人物标签2", "人物标签3", "人物标签4", "人物标签5"],
            "story_tags": ["剧情标签1", "剧情标签2", "剧情标签3", "剧情标签4", "剧情标签5"],
            "reason": "推荐理由，100字以上，不剧透，说明为什么这部作品适合用户"
        }}
        
        只需输出JSON，不要包含其他内容。
        """
        
        try:
            result = self._call_ai(prompt)
            if result:
                if result.startswith("```json"):
                    result = result[7:]
                if result.endswith("```"):
                    result = result[:-3]
                return json.loads(result.strip())
        except Exception as e:
            print(f"生成标签和推荐理由失败: {e}")
        
        return {
            "character_tags": ["主角", "配角", "反派"],
            "story_tags": ["剧情", "情感", "成长"],
            "reason": f"《{movie_info['title']}》是一部精彩的影视作品，适合喜欢{user_input}类型的观众观看。"
        }
    
    def _get_mock_data(self, keyword):
        mock_data = [
            {
                "title": "盗梦空间",
                "year": "2010",
                "rating": "9.3",
                "overview": "道姆·柯布是一名专门从事意识深层盗窃的高手。在一次任务失败后，他接受了一项看似不可能完成的任务：在目标的潜意识中植入一个想法。",
                "poster": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
                "character_tags": ["梦境行者", "执念者", "领导者"],
                "story_tags": ["科幻", "悬疑", "意识探索"],
                "reason": "诺兰的这部科幻巨作重新定义了电影叙事的可能性。影片构建了一个多层梦境的世界，主角团队进入目标人物的潜意识窃取机密。电影不仅有令人叹为观止的视觉效果，更重要的是它提出了关于现实与梦境、记忆与创造的深刻哲学问题。这是一部兼具商业成功和艺术价值的杰作。",
                "source": "mock"
            },
            {
                "title": "消失的爱人",
                "year": "2014",
                "rating": "8.7",
                "overview": "一对夫妻在结婚五周年纪念日当天，妻子突然失踪。所有证据都指向丈夫就是凶手，但真相远比表面更加复杂。",
                "poster": "https://image.tmdb.org/t/p/w500/5EW4TR3fWEqpKsWysNcBM3geD08.jpg",
                "character_tags": ["腹黑", "高智商", "伪装者"],
                "story_tags": ["悬疑", "心理惊悚", "婚姻危机"],
                "reason": "这部电影以其精妙的叙事结构和出人意料的反转著称。故事讲述了一对夫妻在结婚五周年纪念日当天，妻子突然失踪，所有证据都指向丈夫就是凶手。影片通过交错的时间线，逐步揭示了一个关于爱情、婚姻和人性的黑暗真相。",
                "source": "mock"
            },
            {
                "title": "七宗罪",
                "year": "1995",
                "rating": "8.8",
                "overview": "一名即将退休的老警探和他的新搭档追踪一名连环杀手，凶手按照天主教七宗罪的顺序杀人。",
                "poster": "https://image.tmdb.org/t/p/w500/6y1kNqL0qQDkwu91Y1aG5EG7vXl.jpg",
                "character_tags": ["老警探", "热血新人", "变态杀手"],
                "story_tags": ["犯罪", "心理悬疑", "宗教隐喻"],
                "reason": "这部经典犯罪悬疑片以天主教七宗罪为框架，讲述了一个连环杀手按照暴食、贪婪、懒惰、嫉妒、骄傲、淫欲、愤怒的顺序杀人。影片氛围压抑黑暗，完美呈现了罪恶之城的景象。",
                "source": "mock"
            },
            {
                "title": "禁闭岛",
                "year": "2010",
                "rating": "8.8",
                "overview": "联邦探员泰迪前往一座孤岛精神病院调查失踪女患者，却发现整个岛上似乎都隐藏着不可告人的秘密。",
                "poster": "https://image.tmdb.org/t/p/w500/svIDTNUoajS8dLEo7EosxvyAsgJ.jpg",
                "character_tags": ["失忆侦探", "精神病患", "阴谋论者"],
                "story_tags": ["心理悬疑", "孤岛惊魂", "身份认同"],
                "reason": "马丁·斯科塞斯的这部心理惊悚片将观众带入一个充满迷雾和不确定性的世界。莱昂纳多·迪卡普里奥饰演的联邦探员前往一座孤岛精神病院调查失踪女患者，却发现整个岛上似乎都隐藏着不可告人的秘密。",
                "source": "mock"
            },
            {
                "title": "网络谜踪",
                "year": "2018",
                "rating": "8.5",
                "overview": "一位父亲通过女儿的社交账号、视频聊天和各种网络痕迹寻找失踪女儿的故事。",
                "poster": "https://image.tmdb.org/t/p/w500/86L8wqGMDbwURPni2t7FQ0nDjsH.jpg",
                "character_tags": ["焦虑父亲", "失踪少女", "技术高手"],
                "story_tags": ["桌面电影", "网络悬疑", "亲情救赎"],
                "reason": "这部创新的悬疑片全程通过电脑屏幕呈现，讲述了一位父亲通过女儿的社交账号、视频聊天和各种网络痕迹寻找失踪女儿的故事。这种独特的叙事方式不仅新颖，而且完美契合了数字时代的主题。",
                "source": "mock"
            }
        ]
        return mock_data
    
    def update_profile(self, movie):
        for tag in movie.get("story_tags", []):
            if tag not in self.profile["favorite_genres"]:
                self.profile["favorite_genres"].append(tag)
        
        for tag in movie.get("character_tags", []):
            if tag not in self.profile["favorite_character_types"]:
                self.profile["favorite_character_types"].append(tag)
        
        self.profile["watch_count"] += 1
        
        if movie.get("title") not in self.profile["favorite_movies"]:
            self.profile["favorite_movies"].append(movie.get("title"))
        
        self._save_profile()
    
    def add_favorite(self, movie):
        exists = False
        for fav in self.favorites:
            if fav.get("title") == movie.get("title"):
                exists = True
                break
        
        if not exists:
            self.favorites.append(movie)
            self._save_favorites()
            self.update_profile(movie)
            return True
        return False
    
    def remove_favorite(self, title):
        self.favorites = [f for f in self.favorites if f.get("title") != title]
        self._save_favorites()
        return True
    
    def is_favorite(self, title):
        return any(f.get("title") == title for f in self.favorites)
    
    def get_favorites(self):
        return self.favorites
    
    def get_profile(self):
        return self.profile
    
    def generate_recommendations(self, user_input):
        results = []
        tmdb_results = []
        
        profile_keywords = []
        if self.profile.get("favorite_genres"):
            profile_keywords.extend(self.profile["favorite_genres"][:3])
        
        search_queries = [user_input]
        if profile_keywords:
            search_queries.extend(profile_keywords)
        
        try:
            for query in search_queries[:2]:
                search_results = self._tmdb_search_movies(query)
                if search_results and search_results.get("results"):
                    for item in search_results["results"][:2]:
                        if item.get("title") and item.get("overview"):
                            details = self._tmdb_get_movie_details(item["id"])
                            if details:
                                tmdb_results.append({
                                    "title": details.get("title", item["title"]),
                                    "year": details.get("release_date", "")[:4] if details.get("release_date") else "",
                                    "rating": str(details.get("vote_average", 0)),
                                    "overview": details.get("overview", item.get("overview", "")),
                                    "poster": f"https://image.tmdb.org/t/p/w500{details.get('poster_path', item.get('poster_path', ''))}" if details.get("poster_path") or item.get("poster_path") else "",
                                    "source": "tmdb"
                                })
            
            tv_results = self._tmdb_search_tv(user_input)
            if tv_results and tv_results.get("results"):
                for item in tv_results["results"][:3]:
                    if item.get("name") and item.get("overview"):
                        details = self._tmdb_get_tv_details(item["id"])
                        if details:
                            tmdb_results.append({
                                "title": details.get("name", item["name"]),
                                "year": details.get("first_air_date", "")[:4] if details.get("first_air_date") else "",
                                "rating": str(details.get("vote_average", 0)),
                                "overview": details.get("overview", item.get("overview", "")),
                                "poster": f"https://image.tmdb.org/t/p/w500{details.get('poster_path', item.get('poster_path', ''))}" if details.get("poster_path") or item.get("poster_path") else "",
                                "source": "tmdb"
                            })
            
            seen_titles = set()
            filtered_results = []
            for item in tmdb_results:
                if item["title"] not in seen_titles:
                    seen_titles.add(item["title"])
                    filtered_results.append(item)
            tmdb_results = filtered_results[:5]
            
            for item in tmdb_results:
                ai_info = self._generate_tags_and_reason(item, user_input)
                item.update(ai_info)
                item["source"] = "tmdb"
                item["is_favorite"] = self.is_favorite(item["title"])
            results.extend(tmdb_results)
            
            if len(results) < 5:
                remaining = 5 - len(results)
                mock_data = self._get_mock_data(user_input)
                for item in mock_data[:remaining]:
                    item["source"] = "ai_supplement"
                    item["is_favorite"] = self.is_favorite(item["title"])
                    results.append(item)
            
        except Exception as e:
            print(f"推荐生成失败，使用模拟数据: {e}")
            results = self._get_mock_data(user_input)
            for item in results:
                item["source"] = "mock"
                item["is_favorite"] = self.is_favorite(item["title"])
        
        return {
            "success": len([r for r in results if r.get("source") == "tmdb"]) > 0,
            "error": None,
            "raw_response": None,
            "data": results,
            "using_mock": all(r.get("source") == "mock" for r in results)
        }

if __name__ == "__main__":
    agent = MovieRecommendationAgent()
    print("=== 用户画像 ===")
    print(json.dumps(agent.get_profile(), ensure_ascii=False, indent=2))
    print("\n=== 收藏列表 ===")
    print(json.dumps(agent.get_favorites(), ensure_ascii=False, indent=2))