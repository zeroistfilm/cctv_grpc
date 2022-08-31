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
import logging
import asyncio
from grpc import aio

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


def imgToByteWithZlib(img):
    imgEncoded = cv2.imencode('.jpg', img)[1]
    imgBytes = imgEncoded.tobytes()
    compImgByte = zlib.compress(imgBytes)
    return compImgByte

def ByteWithZlibToImg(byteZlib):
    decompimg = zlib.decompress(byteZlib)
    decompjpg = np.frombuffer(decompimg, dtype=np.uint8)
    img = cv2.imdecode(decompjpg, cv2.IMREAD_COLOR)
    return img


class ImageServer(image_procedure_pb2_grpc.ImageServerServicer):
    async def getImage(self, request, context):
        print(request.farm, request.sector, request.hasTIC,  request.camIdx)
        cap = cv2.VideoCapture(capDict[request.farm][request.sector][request.hasTIC][request.camIdx])
        ret1, img1 = cap.read()
        ret2, img2 = cap.read()
        cap.release()
        return image_procedure_pb2.ImageResponse(imgByte1=imgToByteWithZlib(img1), imgByte2=imgToByteWithZlib(img2),)


async def serve():
    # create a gRPC server
    server = aio.server()       #grpc.server(futures.ThreadPoolExecutor(max_workers=20))

    # add the defined class to the server
    image_procedure_pb2_grpc.add_ImageServerServicer_to_server(ImageServer(), server)

    # listen on port 5005
    print('Starting server. Listening on port 5001.')
    server.add_insecure_port('0.0.0.0:5001')
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
