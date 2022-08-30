import grpc
from concurrent import futures
import time

# import the generated classes
import image_procedure_pb2
import image_procedure_pb2_grpc

import numpy as np
import base64
import zlib
import cv2
import sys
import queue
import threading
import json

capDict={}
with open("cctv_config.json", 'r', encoding='UTF-8') as f:
    caminfo = json.load(f)

for farm in caminfo.keys():
    capDict[farm] = {}
    for sector in caminfo[farm].keys():
        capDict[farm][sector] = {}
        for cam in caminfo[farm][sector].keys():
            capDict[farm][sector][cam] = {}
            for position in caminfo[farm][sector][cam].keys():
                capDict[farm][sector][cam][position] = {}
                if caminfo[farm][sector][cam][position].split('://')[0] == "rtsp":
                    # print(caminfo[farm][sector][cam][position])
                    try:
                        capDict[farm][sector][cam][position] = caminfo[farm][sector][cam][position]
                    except Exception as e:
                        capDict[farm][sector][cam][position] = "Error check RTSP address"

# based on .proto service
class ImageServer(image_procedure_pb2_grpc.ImageServerServicer):
    def getImage(self, request, context):
        print(request.farm, request.sector, request.camIdx)
        cap = cv2.VideoCapture(capDict[request.farm][request.sector]['cctv'][request.camIdx])
        ret, img1 = cap.read()

        resized = cv2.imencode('.jpg', img1)
        print(type(resized))
        encoded = resized[1].tobytes()
        img_base64_string1 = base64.b64encode(resized[1]).decode('utf-8')

        compImgSting1 = zlib.compress(encoded, -1)
        compImgSting2 = zlib.compress(bytearray(img_base64_string1, encoding='utf-8'), -1)

        print('img', type(img1), sys.getsizeof(img1))
        print('encode', type(resized[1]), sys.getsizeof(resized[1]))
        print('encode -> base64',type(img_base64_string1), sys.getsizeof(img_base64_string1))
        print('encode -> byte', type(encoded), sys.getsizeof(encoded))
        print('byte -> zlib', type(compImgSting1), sys.getsizeof(compImgSting1))
        print('base64 -> zlib',type(compImgSting2), sys.getsizeof(compImgSting2))


        response = image_procedure_pb2.ImageResponse()
        response.imageString = encoded
        cap.release()
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))

# add the defined class to the server
image_procedure_pb2_grpc.add_ImageServerServicer_to_server(ImageServer(), server)

# listen on port 5005
print('Starting server. Listening on port 5001.')
server.add_insecure_port('0.0.0.0:5001')
server.start()
server.wait_for_termination()
