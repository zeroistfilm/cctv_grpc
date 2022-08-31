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
        ret1, img1 = cap.read()
        ret2, img2 = cap.read()
        imgEncoded1 = cv2.imencode('.jpg', img1)
        imgEncoded2 = cv2.imencode('.jpg', img2)
        imgBytes1 = imgEncoded1[1].tobytes()
        imgBytes2 = imgEncoded2[1].tobytes()
        compImgByte1 = zlib.compress(imgBytes1)
        compImgByte2 = zlib.compress(imgBytes2)

        response = image_procedure_pb2.ImageResponse()
        response.imgByte1 = compImgByte1
        response.imgByte2 = compImgByte2
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


