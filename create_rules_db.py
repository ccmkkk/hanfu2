# 自动创建汉服规则库（SQLite，Python自带，无需安装任何软件）
import sqlite3

# 连接数据库（自动生成 hanfu_rules.db 文件）
conn = sqlite3.connect("hanfu_rules.db")
cursor = conn.cursor()

# ============= 1. 创建季节色板表 =============
cursor.execute('''
CREATE TABLE IF NOT EXISTS season_color (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    season TEXT NOT NULL,
    scene TEXT NOT NULL,
    color_list TEXT NOT NULL
)
''')

# 插入季节色板数据
season_data = [
    ("春","日常","柳绿,桃红,芽黄"),
    ("春","拍照","樱粉,天青,月牙白"),
    ("春","结婚","绯红,鎏金,牙白"),
    ("夏","日常","月白,薄荷绿,浅粉"),
    ("夏","拍照","冰蓝,竹青,霜白"),
    ("夏","结婚","水红,银白,翡翠"),
    ("秋","日常","杏黄,赭石,墨绿"),
    ("秋","拍照","橙红,驼色,苍青"),
    ("秋","结婚","枣红,赤金,墨黑"),
    ("冬","日常","墨黑,朱砂,象牙白"),
    ("冬","拍照","玄色,正红,霜灰"),
    ("冬","结婚","正红,明黄,玄黑")
]
cursor.executemany("INSERT INTO season_color (season, scene, color_list) VALUES (?,?,?)", season_data)

# ============= 2. 创建色彩配伍表 =============
cursor.execute('''
CREATE TABLE IF NOT EXISTS color_match (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    main_color TEXT NOT NULL,
    match_color TEXT NOT NULL,
    is_match INTEGER NOT NULL
)
''')

color_data = [
    ("金","玄",1), ("赤","青",1), ("白","蓝",1),
    ("绿","米白",1), ("赤","黑",1), ("金","赤",1),
    ("赤","白",1), ("金","绿",0)
]
cursor.executemany("INSERT INTO color_match (main_color, match_color, is_match) VALUES (?,?,?)", color_data)

# ============= 3. 创建纹样适配表 =============
cursor.execute('''
CREATE TABLE IF NOT EXISTS pattern_match (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    main_pattern TEXT NOT NULL,
    match_pattern TEXT NOT NULL,
    is_match INTEGER NOT NULL,
    meaning TEXT NOT NULL
)
''')

pattern_data = [
    ("牡丹","凤凰",1,"富贵吉祥、盛世荣华"),
    ("牡丹","寒梅",0,"寓意冲突，不宜搭配"),
    ("云纹","所有",1,"祥云瑞气，百搭纹样"),
    ("缠枝莲","牡丹",1,"清廉富贵、吉祥连绵"),
    ("凤凰","梅花",0,"纹样气场不合，传统禁忌"),
    ("竹纹","兰草",1,"君子气节、清雅淡泊")
]
cursor.executemany("INSERT INTO pattern_match (main_pattern, match_pattern, is_match, meaning) VALUES (?,?,?,?)", pattern_data)

# ============= 4. 新增：肤色 + 性别 适配表 =============
cursor.execute('''
CREATE TABLE IF NOT EXISTS skin_gender_match (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skin_tone TEXT NOT NULL,
    gender TEXT NOT NULL,
    suit_color TEXT NOT NULL,
    suit_style TEXT NOT NULL
)
''')

skin_gender_data = [
    ("冷皮", "女", "月白,冰蓝,霜灰,薄荷绿,樱粉", "齐胸襦裙,诃子裙,大袖衫,褙子"),
    ("暖皮", "女", "绯红,杏黄,橙红,枣红,驼色", "齐腰襦裙,袄裙,圆领袍,披风"),
    ("冷皮", "男", "月白,玄黑,冰蓝,竹青,霜灰", "圆领袍,直裾,道袍,幞头袍衫"),
    ("暖皮", "男", "赤金,赭石,正红,墨绿,玄黑", "圆领袍,直裾,大袖衫,曳撒")
]

cursor.executemany('''
INSERT INTO skin_gender_match (skin_tone, gender, suit_color, suit_style)
VALUES (?,?,?,?)
''', skin_gender_data)

# 提交并关闭
conn.commit()
conn.close()
print("✅ 汉服规则库创建完成！生成 hanfu_rules.db 文件")