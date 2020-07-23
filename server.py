# すること1：jsでカメラからの読み込み、表示
# すること2：modelへの画像渡し
# すること3：必要ならDBとのリンク


from flask import Flask, render_template, Response
from camera import VideoCamera
import numpy as np
import cv2
from datetime import datetime
import os
import string
#from PIL import Image
import pymysql

from src.model import MLModel

mymodel = MLModel('../ml/test.pt')

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['SECRET_KEY'] = os.urandom(24)

# MySQLに接続
def getConnection():
    return pymysql.connect(
        host='localhost',
        db='mydb',
        user='root',
        password='',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )

# モデルによって合わせる
def load_model():
    global recognizer
    print(" * Loading pre-trained model ...")
    cascadePath = './haarcascade_frontalface_alt.xml'
    faceCascade = cv2.CascadeClassifier(cascadePath)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    # recognizer = cv2.face.createLBPHFaceRecognizer()
    # recognizer = cv2.face.LBPHFaceRecognizer.create()
    recognizer.read('./sample_model.yml')
    print(' * Loading end')


# コピペ https://qiita.com/kagami-r0927/items/3d426997467f0a975143
# PILを使ってる
@app.route('/result', methods=['POST'])
def result():
    # submitした画像が存在したら処理する
    if request.files['image']:
        # 白黒画像として読み込み
        image_pil = Image.open(request.files['image']).convert('L')
        image = np.array(image_pil, 'uint8')
        # 類似度を出力
        label, predict_Confidence = recognizer.predict(image)
        predict_Confidence = str(predict_Confidence)
        # render_template('./result.html')
        return render_template('./result.html', title='類似度', predict_Confidence=predict_Confidence)


# 表示用ページ
@app.route('/view')
def index():
    return render_template('index.html')
    # "/view" を呼び出したときには、indexが表示される。

def gen(camera):
    while True:
        image = camera.get_frame()
        mymodel.predict(image)
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        #return 1
# returnではなくジェネレーターのyieldで逐次出力。
# Generatorとして働くためにgenとの関数名にしている
# Content-Type（送り返すファイルの種類として）multipart/x-mixed-replace を利用。
# HTTP応答によりサーバーが任意のタイミングで複数の文書を返し、紙芝居的にレンダリングを切り替えさせるもの。
#（※以下に解説参照あり）


# ストリーミングサンプル用ページ
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
# '/video_feed'にアクセスするとストリーミング開始

# あとでfilename追加する
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=6006)
# 0.0.0.0はすべてのアクセスを受け付けます。
# webブラウザーには、「localhost:5000」と入力



'''
from flask import Flask, render_template, Response
# from camera import Camera
# VideoCameraに変更
from camera import VideoCamera 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate(camera):
    while True:
        frame=camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/feed')
def feed():
    # generateメソッドの引数をVideoCameraに変更 
    return Response(generate(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
'''
