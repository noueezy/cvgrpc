#Jetson Nano上で動作
import cv2
import datetime
import time
import base64
from concurrent import futures
import grpc
import cvimg_pb2
import cvimg_pb2_grpc
import jetson_nano_camera as jnc
import sys

class JetsonNanoCameraServer(cvimg_pb2_grpc.cvimgServiceServicer):

    def __init__(self):
        self.camera = jnc.JetsonNanoCamera()
        self.camera.start()

    def __del__(self):
        self.camera.stop()
        self.camera.join()

    def SendImage(self, request, context):
        img = self.camera.retrieve()
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        meta = now.strftime('%Y%m%d_%H%M%S')

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
        result, encimg = cv2.imencode('.jpg', img, encode_param)
        b64e = base64.b64encode(encimg)
        print(sys.getsizeof(b64e))
        return cvimg_pb2.cvimgResponse(meta = meta,data = b64e)

#grpcサーバ起動
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
cvimg_pb2_grpc.add_cvimgServiceServicer_to_server(JetsonNanoCameraServer(), server)
server.add_insecure_port('[::]:50051')
server.start()
print('start server')

try:
    while True:
        time.sleep(1)
        print('running.')
except KeyboardInterrupt:
    print('!!! keyboard interrupt')
    server.stop(0)
    del server