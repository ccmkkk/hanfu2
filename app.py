from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_file
import mysql.connector
from neo4j import GraphDatabase
import pandas as pd
import numpy as np
import joblib
import sqlite3
import warnings
import datetime
import requests
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ---------------------- 配置 ----------------------
MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_DB = "hanfu_system"

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678"
NEO4J_DATABASE = "hanfu-knowledge"

RECOMMEND_TOP_N = 3
MODEL_FEATURES = ["dynasty", "style", "color", "pattern", "gender", "skin_tone"]
# ----------------------------------------------------

# ===================== 新增：纹样寓意映射表 =====================
PATTERN_MEANING = {
    "海棠": "海棠寓意玉堂富贵、温和美丽",
    "梅花": "梅花象征高洁坚毅、傲雪迎春",
    "荷花": "荷花代表清廉纯洁、和和美美",
    "菊花": "菊花寓意长寿吉祥、隐逸高洁",
    "云纹": "云纹象征高升如意、吉祥云端",
    "缠枝莲": "缠枝莲寓意生生不息、连绵不断",
    "竹": "竹子代表正直谦虚、节节高升",
    "牡丹": "牡丹象征富贵荣华、国色天香",
    "凤凰": "凤凰寓意吉祥太平、高贵非凡",
    "莲花": "莲花同荷花，代表纯洁与和谐",
    "回纹": "回纹象征富贵不断头、连绵不绝",
    "石榴花": "石榴花寓意多子多福、红红火火",
    "仙鹤": "仙鹤象征长寿高雅、一品当朝",
    "龙纹": "龙纹代表尊贵权威、吉祥瑞兽",
    "无": "素雅无纹，体现古朴简约之美",
    "回字纹": "回字纹寓意富贵绵长、连绵不绝",
    "竹叶纹": "竹叶纹象征清雅高洁、坚韧不拔",
    "暗格": "暗格纹寓意严谨有序、内敛含蓄",
    "几何纹": "几何纹代表秩序与和谐",
    "素面": "素面无纹，彰显材质本身的质感",
    "细菱纹": "细菱纹寓意精致细腻、吉祥如意",
    "宝相花纹": "宝相花象征圣洁庄严、圆满吉祥",
    "团窠纹": "团窠纹寓意团圆美满、富贵环绕",
    "瑞兽纹": "瑞兽纹代表辟邪纳福、祥瑞降临",
    "暗花": "暗花纹若隐若现，寓意低调奢华",
    "菱格": "菱格纹象征稳固与韵律",
    "暗纹": "暗纹含蓄典雅，寓意内藏锦绣",
    "云气纹": "云气纹寓意仙气缭绕、升腾如意",
    "卷草纹": "卷草纹象征生机勃勃、连绵不绝",
    "狩猎纹": "狩猎纹体现勇猛果敢、游猎之乐",
    "鹿纹": "鹿纹寓意福禄双全、长寿吉祥",
    "连珠纹": "连珠纹象征圆满连贯、珠联璧合",
    "云肩纹": "云肩纹寓意云肩如意、福运当头",
    "织金": "织金纹样象征富贵华丽、金玉满堂",
    "暗八仙": "暗八仙寓意仙家庇佑、神通广大",
    "江崖海水纹": "江崖海水纹象征江山永固、福山寿海"
}

# ===================== 新增：制式场景映射表 =====================
STYLE_SCENE = {
    "齐胸襦裙": "适宜日常、出游，尽显灵动柔美",
    "圆领袍": "适宜通勤、正式场合，彰显干练威仪",
    "半臂襦裙": "适宜夏季日常，清新活泼",
    "诃子裙": "适宜宴会、典礼，雍容华贵",
    "幞头袍衫": "适宜官场、通勤，庄重得体",
    "袒领襦裙": "适宜闺阁、雅集，温婉大方",
    "大袖衫": "适宜典礼、婚庆，大气华贵",
    "褙子": "适宜日常、文人雅集，清雅娴静",
    "交领襦裙": "适宜日常、礼仪，端庄典雅",
    "旋裙": "适宜日常出行，便捷灵动",
    "直裰": "适宜文人日常，洒脱儒雅",
    "抹胸": "内搭或夏季单穿，清凉含蓄",
    "比甲": "适宜春秋叠穿，实用美观",
    "襦裙": "通用日常，温婉古典",
    "交领短袄": "适宜秋冬日常，保暖干练",
    "披风": "适宜秋冬外出，大气保暖",
    "马面裙": "适宜礼仪、婚庆，端庄喜庆",
    "交领长袄": "适宜冬季正式场合，华贵保暖",
    "曳撒": "适宜骑射、出游，英武飒爽",
    "道袍": "适宜日常、雅集，洒脱清高",
    "霞帔": "礼服配饰，象征尊贵吉祥",
    "曲裾": "适宜礼仪、祭祀，庄重古雅",
    "直裾": "适宜正式场合，儒雅正直",
    "杂裾垂髾服": "适宜宴会、仙侠主题，飘逸出尘",
    "袴褶": "适宜骑射、劳作，便捷实用",
    "质孙服": "适宜宴会、典礼，华丽大气",
    "裳": "下装，搭配上衣，庄重典雅",
    "袴": "下装，日常行动便捷",
    "帷裳": "下装，礼仪场合，庄重",
    "裤": "下装，日常便服",
    "裈": "内搭，不单独外穿",
    "裙": "下装，通用搭配",
    "宋裤": "下装，宋制日常，清凉便捷"
}

# ===================== 1. 加载模型（6特征） =====================
rf_model = None
label_encoders = None
try:
    rf_model = joblib.load("hanfu_model_6features.pkl")
    label_encoders = joblib.load("label_encoders_6features.pkl")
    print("✅ 6特征模型加载成功！")
except Exception as e:
    print(f"❌ 模型加载失败: {e}")
    rf_model = None
    label_encoders = None

# ===================== 2. 加载MySQL数据 =====================
def load_hanfu_dataset():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB
        )
        df = pd.read_sql("SELECT * FROM hanfu", conn)
        conn.close()

        df = df.fillna({
            "dynasty": "未知", "style": "未知", "color": "未知", "pattern": "未知",
            "dynasty_compatibility": 80, "culture_match": 80,
            "season": "", "scene": "", "gender": "", "skin_tone": ""
        })
        str_cols = ["dynasty", "style", "color", "pattern", "season", "scene", "gender", "skin_tone"]
        for col in str_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        df["dynasty_compatibility"] = pd.to_numeric(df["dynasty_compatibility"], errors="coerce").fillna(80.0)
        df["culture_match"] = pd.to_numeric(df["culture_match"], errors="coerce").fillna(80.0)
        return df
    except Exception as e:
        print(f"❌ MySQL加载失败: {e}")
        return pd.DataFrame()

hanfu_dataset = load_hanfu_dataset()
print(f"✅ 已加载 {len(hanfu_dataset)} 条汉服数据")

# ===================== 3. SQLite规则库函数 =====================
def get_rule_db():
    return sqlite3.connect("hanfu_rules.db")

def get_season_colors(season, scene):
    db = get_rule_db()
    c = db.cursor()
    c.execute("SELECT color_list FROM season_color WHERE season=? AND scene=?", (season, scene))
    res = c.fetchone()
    db.close()
    return res[0].split(",") if res else []

def is_color_match(main, sub):
    db = get_rule_db()
    c = db.cursor()
    c.execute("SELECT is_match FROM color_match WHERE main_color=? AND match_color=?", (main, sub))
    res = c.fetchone()
    ok = res[0] if res else 1
    db.close()
    return ok == 1

def get_skin_gender_rules(skin, gender):
    db = get_rule_db()
    c = db.cursor()
    c.execute("SELECT suit_color, suit_style FROM skin_gender_match WHERE skin_tone=? AND gender=?", (skin, gender))
    res = c.fetchone()
    db.close()
    if res:
        return res[0].split(","), res[1].split(",")
    return [], []

# ===================== 4. 兼容分预测 =====================
def predict_single_compatibility(item):
    """预测单条汉服的朝代兼容分"""
    if rf_model is not None and label_encoders is not None:
        try:
            input_data = {
                "dynasty": str(item["dynasty"]).strip(),
                "style": str(item["style"]).strip(),
                "color": str(item["color"]).strip(),
                "pattern": str(item["pattern"]).strip(),
                "gender": str(item["gender"]).strip(),
                "skin_tone": str(item["skin_tone"]).strip()
            }
            df_input = pd.DataFrame([input_data], columns=MODEL_FEATURES, dtype=object)
            encoded_features = np.zeros(len(MODEL_FEATURES), dtype=int)
            for i, col in enumerate(MODEL_FEATURES):
                le = label_encoders[f"top_{col}"]
                val = df_input.at[0, col]
                val = str(val).strip() or "未知"
                if val not in le.classes_:
                    val = le.classes_[0]
                encoded_features[i] = le.transform([val])[0]
            proba = rf_model.predict_proba(encoded_features.reshape(1, -1))[0][1]
            base_score = float(item.get("dynasty_compatibility", 80))
            score = round(base_score * 0.7 + float(proba) * 100 * 0.3, 2)
            return max(score, 60)
        except Exception as e:
            print(f"⚠️ 单条预测异常: {e}")
    return round(float(item.get("dynasty_compatibility", 80)), 2)

def predict_compatibility(top, bottom):
    """计算上下装的组合兼容分，增加朝代一致性校验"""
    top_score = predict_single_compatibility(top)
    bottom_score = predict_single_compatibility(bottom)
    base_avg = round((top_score + bottom_score) / 2, 2)
    if top["dynasty"] == bottom["dynasty"]:
        return round(base_avg * 1.1, 2)
    else:
        return round(base_avg * 0.7, 2)

# ===================== 5. 推荐函数 =====================
def recommend_hanfu_set(season, scene, target_dynasty, gender="", skin_tone=""):
    if hanfu_dataset.empty:
        return []

    df = hanfu_dataset.copy()
    if target_dynasty:
        df = df[df["dynasty"] == target_dynasty]

    if gender == "女":
        df = df[df["gender"].isin(["女", "通用"])]
    elif gender == "男":
        df = df[df["gender"].isin(["男", "通用"])]

    if len(df) < 2:
        return []

    season_colors = get_season_colors(season, scene)
    suit_colors, suit_styles = get_skin_gender_rules(skin_tone, gender)

    top_keywords = ["襦裙", "衫", "袄", "大袖衫", "圆领袍", "褙子", "比甲", "曲裾", "直裰", "诃子", "半臂", "袒领",
                    "披风", "交领", "霞帔", "曳撒", "道袍", "质孙服", "袴褶"]
    bottom_keywords = ["裙", "马面", "百迭", "旋裙", "宋裤",
                       "裳", "裤", "袴", "裈", "帷裳"]

    tops = df[df["style"].apply(lambda x: any(kw in x for kw in top_keywords))].to_dict("records")
    bottoms = df[df["style"].apply(lambda x: any(kw in x for kw in bottom_keywords))].to_dict("records")

    if not tops or not bottoms:
        return []

    results = []
    for t in tops:
        for b in bottoms:
            if t["dynasty"] != b["dynasty"]:
                continue
            t_g = t["gender"]
            b_g = b["gender"]
            if t_g == "男" and b_g == "女":
                continue
            dynasty_score = predict_compatibility(t, b)
            culture_score = round((t["culture_match"] + b["culture_match"]) / 2, 2)
            score = dynasty_score * 0.6 + culture_score * 0.2

            extra = 0
            if season_colors and t["color"] in season_colors:
                extra += 6
            if suit_colors and t["color"] in suit_colors:
                extra += 6
            if suit_styles and t["style"] in suit_styles:
                extra += 18
            if is_color_match(t["color"], b["color"]):
                extra += 5
            if season and t["season"] == season:
                extra += 3
            if scene and t["scene"] == scene:
                extra += 3

            total = round(score + extra, 2)
            results.append({
                "套装": f"{t['name']} + {b['name']}",
                "上衣": t["name"], "下装": b["name"],
                "颜色": f"{t['color']}/{b['color']}",
                "纹样": f"{t['pattern']}/{b['pattern']}",
                "朝代": t["dynasty"],
                "朝代兼容分": t["dynasty_compatibility"],
                "文化匹配度": culture_score,
                "综合评分": total,
                "top_style": t["style"], "bottom_style": b["style"]
            })

    df_res = pd.DataFrame(results)
    df_res = df_res.sort_values("综合评分", ascending=False).head(RECOMMEND_TOP_N)
    return df_res.to_dict("records")

# ===================== 6. 寓意查询（增强版：Neo4j优先 + 本地纹样+制式兜底） =====================
def get_meaning(style_name, dynasty, top_pattern="", bottom_pattern=""):
    """
    返回字典: {'pattern_meaning': str, 'style_meaning': str, 'overall_meaning': str}
    """
    clean_style = str(style_name).strip()
    clean_dynasty = str(dynasty).strip()
    if not clean_style or clean_style == "未知":
        return {
            'pattern_meaning': '传统纹样',
            'style_meaning': '传统汉服',
            'overall_meaning': '传统汉服，蕴含中华传统文化之美'
        }

    # 1. 优先 Neo4j 查询整体寓意
    neo4j_meaning = None
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        with driver.session(database=NEO4J_DATABASE) as session:
            res = session.run("""
                MATCH (s:Style)-[:HAS_MEANING]->(m:Meaning)
                WHERE s.name = $style AND s.dynasty = $dynasty
                RETURN m.meaning AS meaning LIMIT 1
            """, style=clean_style, dynasty=clean_dynasty)
            record = res.single()
        driver.close()
        if record and record["meaning"]:
            neo4j_meaning = record["meaning"]
    except Exception as e:
        print(f"⚠️ Neo4j查询异常: {e}")

    # 2. 本地生成纹样寓意（上下装合并）
    # 上衣纹样
    clean_top = str(top_pattern).strip()
    if clean_top in PATTERN_MEANING:
        top_desc = PATTERN_MEANING[clean_top]
    elif clean_top == "无" or clean_top == "":
        top_desc = "素雅无纹"
    else:
        top_desc = "传统吉祥纹样"
    # 下装纹样
    clean_bottom = str(bottom_pattern).strip()
    if clean_bottom in PATTERN_MEANING:
        bottom_desc = PATTERN_MEANING[clean_bottom]
    elif clean_bottom == "无" or clean_bottom == "":
        bottom_desc = "素雅无纹"
    else:
        bottom_desc = "传统吉祥纹样"

    # 合并纹样寓意
    if clean_top and clean_bottom and clean_top != clean_bottom:
        pattern_meaning = f"上衣{clean_top}：{top_desc}；下装{clean_bottom}：{bottom_desc}"
    elif clean_top:
        pattern_meaning = f"{clean_top}：{top_desc}"
    elif clean_bottom:
        pattern_meaning = f"{clean_bottom}：{bottom_desc}"
    else:
        pattern_meaning = "无纹样，素雅古朴"

    # 制式解读
    if clean_style in STYLE_SCENE:
        style_meaning = STYLE_SCENE[clean_style]
    else:
        style_meaning = "适宜多种场合，体现传统之美"

    # 3. 综合寓意：优先 Neo4j，否则组合
    if neo4j_meaning:
        overall = neo4j_meaning
    else:
        overall = f"【纹样寓意】{pattern_meaning}。【制式解读】{style_meaning}。【整体寓意】吉祥典雅，气质出众。"

    return {
        'pattern_meaning': pattern_meaning,
        'style_meaning': style_meaning,
        'overall_meaning': overall
    }
# ===================== 7. 接口 =====================
@app.route('/')
def index():
    return "<h1>✅ 汉服推荐系统运行成功（已集成智能规则）</h1>"


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    season = data.get("season", "")
    scene = data.get("scene", "")
    dynasty = data.get("dynasty", "")
    gender = data.get("gender", "")
    skin_tone = data.get("skin_tone", "")
    res_list = recommend_hanfu_set(season, scene, dynasty, gender, skin_tone)
    if not res_list:
        return jsonify({"推荐方案": []})
    for item in res_list:
        patterns = item.get("纹样", "")
        if '/' in patterns:
            top_pattern, bottom_pattern = patterns.split('/', 1)
        else:
            top_pattern, bottom_pattern = patterns, ""
        meanings = get_meaning(item["top_style"], item["朝代"], top_pattern, bottom_pattern)
        item["纹样寓意"] = meanings['pattern_meaning']
        item["制式解读"] = meanings['style_meaning']
        item["寓意"] = meanings['overall_meaning']
    format_data = [{
        "套装": i["套装"], "颜色": i["颜色"], "纹样": i["纹样"],
        "朝代": i["朝代"], "朝代兼容分": i["朝代兼容分"],
        "文化匹配度": i["文化匹配度"],
        "纹样寓意": i["纹样寓意"],
        "制式解读": i["制式解读"],
        "寓意": i["寓意"]
    } for i in res_list]
    return jsonify({"推荐方案": format_data})


def get_client_ip():
    """获取客户端真实IP（考虑代理）"""
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        ip = request.remote_addr
    return ip


def get_location_by_ip(ip):
    """通过ip-api.com获取地理位置信息"""
    try:
        # 使用免费API，不需要key
        url = f"http://ip-api.com/json/{ip}?fields=status,countryCode,city,lat,lon"
        resp = requests.get(url, timeout=3)
        data = resp.json()
        if data.get('status') == 'success':
            return data
        else:
            return None
    except:
        return None


def get_season_by_location(lat, month):
    """根据纬度判断季节（北半球：3-5春，6-8夏，9-11秋，12-2冬；南半球相反）"""
    if lat > 0:  # 北半球
        if 3 <= month <= 5:
            return '春'
        elif 6 <= month <= 8:
            return '夏'
        elif 9 <= month <= 11:
            return '秋'
        else:
            return '冬'
    else:  # 南半球
        if 3 <= month <= 5:
            return '秋'
        elif 6 <= month <= 8:
            return '冬'
        elif 9 <= month <= 11:
            return '春'
        else:
            return '夏'


def get_fabric_and_layers(season):
    """根据季节返回推荐面料和层数"""
    fabrics = {
        '春': {'fabric': '真丝', 'layers': '2-3层', 'color_primary': '#d4e6c3', 'color_secondary': '#fce6b4'},
        '夏': {'fabric': '纱/罗', 'layers': '单层', 'color_primary': '#b3e0e5', 'color_secondary': '#f5f5dc'},
        '秋': {'fabric': '织锦缎', 'layers': '3层', 'color_primary': '#e8d5b7', 'color_secondary': '#c49a6c'},
        '冬': {'fabric': '夹棉', 'layers': '4层+', 'color_primary': '#d9b8a4', 'color_secondary': '#a65d3d'}
    }
    return fabrics.get(season, fabrics['春'])


def get_festival(month, day):
    """简单判断节日（仅演示中秋和春节）"""
    if month == 9 and (15 <= day <= 17):  # 农历八月十五左右，公历9-10月，简化
        return '中秋'
    elif (month == 1 and day <= 15) or (month == 2 and day <= 15):  # 春节前后
        return '春节'
    return None


@app.route('/season_info', methods=['GET'])
def season_info():
    now = datetime.datetime.now()
    month = now.month
    # 直接按北半球判断，不依赖IP
    if 3 <= month <= 5:
        season = '春'
    elif 6 <= month <= 8:
        season = '夏'
    elif 9 <= month <= 11:
        season = '秋'
    else:
        season = '冬'

    info = get_fabric_and_layers(season)
    festival = get_festival(month, now.day)
    return jsonify({
        'season': season,
        'fabric': info['fabric'],
        'layers': info['layers'],
        'color_scheme': {'primary': info['color_primary'], 'secondary': info['color_secondary']},
        'festival': festival
    })
 #===================== 论坛数据库初始化 =====================
# 在 app.py 中添加（如果还没有）
def init_forum_db():
    conn = get_rule_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS forum_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT DEFAULT '匿名',
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_forum_db()

@app.route('/api/posts', methods=['GET'])
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    conn = get_rule_db()
    c = conn.cursor()
    c.execute('''
        SELECT id, nickname, content, created_at 
        FROM forum_posts 
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
    ''', (per_page, offset))
    rows = c.fetchall()
    posts = [{'id': row[0], 'nickname': row[1], 'content': row[2], 'time': row[3]} for row in rows]
    conn.close()
    return jsonify({'posts': posts, 'has_more': len(posts) == per_page})

@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.json
    nickname = data.get('nickname', '匿名').strip()[:20]
    content = data.get('content', '').strip()
    if not content:
        return jsonify({'error': '内容不能为空'}), 400
    ip = request.remote_addr
    conn = get_rule_db()
    c = conn.cursor()
    c.execute('INSERT INTO forum_posts (nickname, content, ip) VALUES (?, ?, ?)',
              (nickname, content, ip))
    conn.commit()
    post_id = c.lastrowid
    conn.close()
    return jsonify({'id': post_id, 'message': '发布成功'}), 201

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)


