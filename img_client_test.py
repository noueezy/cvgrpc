import cv2
import numpy as np
import base64
import grpc
import cvimg_pb2
import cvimg_pb2_grpc

def get_img_from_jetson(port):
    with grpc.insecure_channel(port) as channel:
        stub = cvimg_pb2_grpc.cvimgServiceStub(channel)

        response = stub.SendImage(cvimg_pb2.cvimgRequest())
        print(type(response))
        print('text:', response.meta)
        #base64 -> jpg
        jpg = base64.b64decode(response.data)
        jpg = np.frombuffer(jpg, dtype=np.uint8)
        #jpg -> raw image
        img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)
        return img

try:
    while True:
        cvimg = get_img_from_jetson('TARGET_IP_ADDRESS:50051')
        h, w = cvimg.shape[:2]
        size = (w//4, h//4)
        resizeImg = cv2.resize(cvimg, size)
        cv2.imshow('image', resizeImg)
        cv2.waitKey(100)
except KeyboardInterrupt:
    print('end.')
