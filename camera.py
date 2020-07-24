import cv2

class VideoCamera(object):
    def __init__(self):
        # self.video = cv2.VideoCapture(-1)
        self.video = cv2.VideoCapture('../ml/dataset/trimed/oyayubi_left/0.mp4')
        # Opencvのカメラをセットします。(0)はノートパソコンならば組み込まれているカメラ

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        return image
        # print(image.shape)
        # ret, jpeg = cv2.imencode('.jpg', image)
        # return jpeg.tobytes()

        # read()は、二つの値を返すので、success, imageの2つ変数で受けています。
        # OpencVはデフォルトでは raw imagesなので JPEGに変換
        # ファイルに保存する場合はimwriteを使用、メモリ上に格納したい時はimencodeを使用
        # cv2.imencode() は numpy.ndarray() を返すので .tobytes() で bytes 型に変換

'''
from time import time, sleep
import cv2

class Camera(object):
    def __init__(self):
        self.frames = []
        self.files = ['1', '2', '3', '4', '5']

        for f in self.files:
            self.frames.append(open('./static/img/' + f + '.jpg', 'rb').read())

    def get_frame(self):
        return self.frames[int(time()) % len(self.files)]

cam = Camera()

if __name__=='__main__':
    cam.open_camera()

# VideoCameraを追加
class VideoCamera():
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        # Opencvのカメラをセットします。(0)はノートパソコンならば組み込まれているカメラ
        self.frames = []
        self.files = []
        self.MAX_FRAME_NUM = 10 # 撮影枚数を指定
        self.RECORD_INTERVAL = 1 # 撮影のインターバルを指定

        self.record()

    def get_frame(self):
        # 撮影された画像を順に返す
        for file in self.files:
            self.frames.append(open(file, 'rb').read())
        return self.frames[int(time()) % len(self.frames)]
        # read()は、二つの値を返すので、success, imageの2つ変数で受けています。
        # OpencVはデフォルトでは raw imagesなので JPEGに変換
        # ファイルに保存する場合はimwriteを使用、メモリ上に格納したい時はimencodeを使用
        # cv2.imencode() は numpy.ndarray() を返すので .tobytes() で bytes 型に変換

    def record(self):
        self.cap = cv2.VideoCapture(0)

        cnt = 0
        while True:
            # 撮影したファイルの保存先を指定
            path = './static/img/img' + str(cnt) + '.jpg'
            ret, frame = self.cap.read()
            self.files.append(path)

            cv2.imwrite(path, frame)

            # ESCキーで停止する
            k = cv2.waitKey(1)
            if k == 27:
                break

            # 指定した枚数を撮影したら停止する
            cnt += 1
            if cnt == self.MAX_FRAME_NUM:
                break

            # 撮影のインターバルを取る
            sleep(self.RECORD_INTERVAL)

        self.cap.release()
        cv2.destroyAllWindows()
        '''
