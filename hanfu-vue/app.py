from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from neo4j import GraphDatabase
from datetime import datetime

app = Flask(__name__)
CORS(app)

MYSQL_PASSWORD = "123456"
NEO4J_PASSWORD = "12345678"

def get_mysql_data(season, scene, dynasty, gender):
    print(f"Querying: season={season}, scene={scene}, dynasty={dynasty}, gender={gender}")
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password=MYSQL_PASSWORD,
            database="hanfu_system"
        )
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM hanfu WHERE season=%s AND scene=%s AND dynasty=%s AND gender=%s"
        cursor.execute(sql, (season, scene, dynasty, gender))
        data = cursor.fetchall()
        conn.close()
        print(f"Results: {len(data)} rows")
        return data
    except Exception as e:
        print(f"MySQL error: {e}")
        return []

def fetch_meaning_from_node(label, name):
    """通用查询函数：根据标签(Style/Pattern)和名称查寓意"""
    if not name or name in ["无", "无纹", "纯色", "None"]:
        return None

    try:
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", NEO4J_PASSWORD))
        with driver.session(database="hanfu-knowledge") as session:
            query = f"""
                MATCH (n:{label} {{name: $name}})-[:HAS_MEANING]->(m:Meaning)
                RETURN m.meaning AS meaning
                LIMIT 1
            """
            result = session.run(query, name=name)
            record = result.single()
            return record["meaning"] if record else None
    except Exception as e:
        print(f"Neo4j 查询出错 ({label} - {name}): {e}")
        return None

@app.route('/')
def index():
    return "<h1>✅ 汉服推荐系统后端运行成功！</h1>"

@app.route('/api/season_info', methods=['GET'])
def season_info():
    now = datetime.now()
    month = now.month
    if month in [3, 4, 5]:
        season = '春'
        fabric = '真丝'
        layers = '2-3层'
        festival = None
    elif month in [6, 7, 8]:
        season = '夏'
        fabric = '纱'
        layers = '1-2层'
        festival = None
    elif month in [9, 10, 11]:
        season = '秋'
        fabric = '绸缎'
        layers = '3-4层'
        festival = None
    else:
        season = '冬'
        fabric = '棉麻'
        layers = '4-5层'
        festival = None

    return jsonify({
        'season': season,
        'fabric': fabric,
        'layers': layers,
        'festival': festival,
        'color_scheme': {
            'primary': '#f3efe7',
            'secondary': '#e8e0d5'
        }
    })

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    season = data.get('season', '春')
    raw_scene = data.get('scene', '日常')
    dynasty = data.get('dynasty', data.get('style', '唐'))
    gender = data.get('gender', '女')
    skin_tone = data.get('skin_tone', '')
    
    # 【新增】：获取前端或测试脚本传来的控制变量，默认开启图谱 
    use_kg = data.get('use_kg', True) 

    # 1. 场景映射逻辑保留
    if raw_scene in ['日常', '通勤', '出游']:
        mapped_scene = '日常'
    elif raw_scene in ['拍照', '礼仪', '祭祀']:
        mapped_scene = '拍照'
    elif raw_scene == '婚礼':
        mapped_scene = '婚礼'
    else:
        mapped_scene = '日常'

    # 2. 查询 MySQL（婚礼依然享受忽略季节特权）
    mysql_data = get_mysql_data(season, mapped_scene, dynasty, gender)
    print(f"从数据库中找到数据数量: {len(mysql_data)}")

    # 3. 数据组装（恢复前端认识的列表格式）
    res = []
    for item in mysql_data:
        style_name = item.get('style', '')
        pattern_name = item.get('pattern', '')
        item_name = item.get('name', style_name)
        item_color = item.get('color', '')
        
        # ================= 控制变量逻辑 =================
        if use_kg:
            # 实验组：调用 Neo4j 获取知识图谱数据
            s_meaning = fetch_meaning_from_node("Style", style_name)
            p_meaning = fetch_meaning_from_node("Pattern", pattern_name)
            item['style_meaning'] = s_meaning if s_meaning else f"暂未收录【{style_name}】的详细制式内涵"
            item['pattern_meaning'] = p_meaning if p_meaning else f"暂未收录【{pattern_name}】的详细纹样寓意"
            item['kg_status'] = 'success' # 打上图谱成功标记
        else:
            # 对照组：关闭图谱，返回简短信息，并降低文化匹配度
            item['style_meaning'] = "制式"
            item['pattern_meaning'] = "纹样"
            # 文化匹配度降低（缺乏图谱解析，无法提供文化内涵）
            item['culture_match'] = int(item.get('culture_match', 90) * 0.7)
            item['kg_status'] = 'disabled'
        # ================================================ 

        # 综合寓意生成
        if mapped_scene == '婚礼':
            item['meaning'] = f"此套【{item_name}】遵循{dynasty}代婚服礼制。" 
        else:
            item['meaning'] = f"为您推荐这套【{item_name}】。" 

        res.append(item)

    # 【核心修复】：直接返回列表，不要包在字典里，让前端能认出来！
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
