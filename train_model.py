import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sqlalchemy import create_engine

# 1. 连接MySQL
engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/hanfu_system")
df = pd.read_sql("SELECT * FROM hanfu", engine)

# 2. 6个特征：朝代、款式、颜色、纹样、性别、肤色
features = ["dynasty", "style", "color", "pattern", "gender", "skin_tone"]
X = df[features].copy()

# 3. 编码所有6个特征
label_encoders = {}
for col in features:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    label_encoders[f"top_{col}"] = le
    label_encoders[f"bottom_{col}"] = le

# 4. 标签：朝代兼容分
y = df["dynasty_compatibility"]

# 5. 训练随机森林
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)

# 6. 保存模型和编码器
joblib.dump(rf, "hanfu_model_6features.pkl")
joblib.dump(label_encoders, "label_encoders_6features.pkl")

print("✅ 6特征模型训练完成！支持性别+肤色推荐！")