#Jetson Nano上で動作
import cv2
import datetime
import time
import threading

GST_STR = 'nvarguscamerasrc \
    ! video/x-raw(memory:NVMM), width=3264, height=2464, format=(string)NV12, framerate=(fraction)21/1 \
    ! nvvidconv ! video/x-raw, width=(int)3264, height=(int)2464, format=(string)BGRx \
    ! videoconvert \
    ! appsink'

class JetsonNanoCamera(threading.Thread):

    def __init__(self):
        print('init')
        super(JetsonNanoCamera, self).__init__()
        self.stop_event = threading.Event()
        self.count = 0
        self.lock = threading.Lock()
        self.cap = cv2.VideoCapture(GST_STR, cv2.CAP_GSTREAMER)
        time.sleep(1)


    def stop(self):
        """
        撮影スレッドを停止する
        """
        self.stop_event.set()

    def run(self):
        """
        撮影スレッド
        """
        print('Running start')
        while not self.stop_event.is_set():
            self.lock.acquire()
            ret, self.img = self.cap.read()
            self.lock.release()
            if ret == False:
                raise ValueError('capture error')
            self.count += 1
        print('Running end')
    
    def retrieve(self):
        """
        撮影した最新の画像を取得
        """
        self.lock.acquire()
        img = self.img.copy()
        self.lock.release()
        return img

