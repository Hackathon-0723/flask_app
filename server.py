# すること1：jsでカメラからの読み込み、表示
# すること2：modelへの画像渡し
# すること3：必要ならDBとのリンク

from flask import Flask, render_template, Response, request
from camera import VideoCamera
import numpy as np
import cv2
from datetime import datetime
import os
import string
from PIL import Image
import pymysql
#import object_detection_api

from src.model import MLModel

mymodel = MLModel('./test.pt')

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['SECRET_KEY'] = os.urandom(24)

# MySQLに接続
def getConnection():
    return pymysql.connect(
        host='localhost',
        db='test',
        user='root',
        password='',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )


# カメラ画像の取得処理ページ
# APIに画像を流す
@app.route("/img", methods=["POST","GET"])
def img():
    if request.method == "POST":
        print('here')
        img = request.files["video"].read()
        # pillow から opencvに変換
        imgPIL = Image.open(io.BytesIO(img))
        imgCV = np.asarray(imgPIL)
        print(imgCV.shape)
        cv2.imwrite('./templates/dst/test.jpg', imgCV)
        imgCV = cv2.bitwise_not(imgCV)
        # 好きな処理を入れる
        return render_template('index.html')
    if request.method == "GET":
        return render_template('front_page/index.html')


# ログイン表示用ページ
@app.route('/')
def index():
    return render_template('front_page/index.html')
    # "/" を呼び出したときには、indexが表示される。

def gen(camera):
    while True:
        image = camera.get_frame()
        mymodel.predict(image)
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# testモデルページ
@app.route('/video_feed')
def video_feed():
    #return "gen start"
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
# '/video_feed'にアクセスするとストリーミング開始

'''
# returnではなくジェネレーターのyieldで逐次出力。
# Generatorとして働くためにgenとの関数名にしている
# Content-Type（送り返すファイルの種類として）multipart/x-mixed-replace を利用。
# HTTP応答によりサーバーが任意のタイミングで複数の文書を返し、紙芝居的にレンダリングを切り替えさせるもの。
'''



if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug=True)
    app.run(host='0.0.0.0', port=5000, ssl_context=('openssl/server.crt', 'openssl/server.key'), threaded=True, debug=True)
# 0.0.0.0はすべてのアクセスを受け付ける    
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
