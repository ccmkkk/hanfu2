from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import io
from PIL import Image

app = Flask(__name__)
CORS(app)

def detect_skin_tone(image_data):
    """
    使用OpenCV进行面部检测和肤色分析
    """
    try:
        # 解码base64图片
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # 将base64转换为字节
        image_bytes = base64.b64decode(image_data)
        
        # 转换为numpy数组
        nparr = np.frombuffer(image_bytes, np.uint8)
        
        # 读取图片
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return {'error': '无法解析图片'}
        
        # 加载面部检测器
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 检测面部
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            # 如果没有检测到面部，使用中心区域
            height, width = img.shape[:2]
            x = width // 2 - 100
            y = height // 2 - 100
            w = h = 200
            # 确保在图片范围内
            x = max(0, min(x, width - 200))
            y = max(0, min(y, height - 200))
            face_detected = False
        else:
            # 使用最大的面部
            largest_face = max(faces, key=lambda f: f[2] * f[3])
            x, y, w, h = largest_face
            face_detected = True
        
        # 提取面部区域
        face_region = img[y:y+h, x:x+w]
        
        if face_region.size == 0:
            return {'error': '面部区域提取失败'}
        
        # 分析肤色
        # 转换到HSV颜色空间
        hsv = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)
        
        # 计算平均HSV值
        avg_hsv = cv2.mean(hsv)[:3]
        
        # 判断肤色类型
        # HSV中Hue: 0-180, Saturation: 0-255, Value: 0-255
        h, s, v = avg_hsv
        
        # 归一化到0-1范围
        h_norm = h / 180.0
        s_norm = s / 255.0
        v_norm = v / 255.0
        
        # 肤色判断逻辑
        if h_norm > 0.08 and h_norm < 0.25 and s_norm > 0.15:
            skin_type = '暖黄皮'
        elif h_norm > 0 and h_norm < 0.12 and v_norm > 0.65:
            skin_type = '冷白皮'
        else:
            skin_type = '通用'
        
        return {
            'skin_tone': skin_type,
            'hsv_values': {
                'hue': round(h_norm, 3),
                'saturation': round(s_norm, 3),
                'value': round(v_norm, 3)
            },
            'face_detected': face_detected,
            'face_area': {
                'x': x,
                'y': y,
                'width': w,
                'height': h
            }
        }
        
    except Exception as e:
        return {'error': f'肤色检测失败: {str(e)}'}

@app.route('/api/skin_detection', methods=['POST'])
def skin_detection():
    """
    肤色检测API接口
    """
    try:
        data = request.json
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'error': '未提供图片数据'}), 400
        
        result = detect_skin_tone(image_data)
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': '肤色检测服务运行正常'})

if __name__ == '__main__':
    print("肤色检测服务启动中...")
    print("服务地址: http://127.0.0.1:5001")
    app.run(host="127.0.0.1", port=5001, debug=True)