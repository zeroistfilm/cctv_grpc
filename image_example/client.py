import grpc
# import the generated classes
import image_procedure_pb2
import image_procedure_pb2_grpc
# data encoding
import numpy as np
import base64
import zlib
import time
import cv2
from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.responses import JSONResponse, Response
from typing import Optional, Any
import json

app = FastAPI()
channel = grpc.insecure_channel('192.168.2.1:5001')
stub = image_procedure_pb2_grpc.ImageServerStub(channel)
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

@app.get("/cctv/{farm}/{sector}/{isTIC}/{camidx}")
async def getframe(farm: str, sector:str,isTIC:str,  camidx:str):

    if farm=='dongilps':
        cap = cv2.VideoCapture(capDict[farm][sector][isTIC][camidx])
        ret1, img1 = cap.read()
        ret2, img2 = cap.read()
        cap.release()

        if img1.shape[1] != 1920 and isTIC == 'cctv':
            img1 = cv2.resize(img1, dsize=(1920, 1080), interpolation=cv2.INTER_CUBIC)
            img2 = cv2.resize(img2, dsize=(1920, 1080), interpolation=cv2.INTER_CUBIC)


        resized = cv2.imencode('.jpg', img1)
        img_base64_string1 = base64.b64encode(resized[1]).decode()

        resized = cv2.imencode('.jpg', img2)
        img_base64_string2 = base64.b64encode(resized[1]).decode()

        return JSONResponse({"img1": img_base64_string1, "img2": img_base64_string2})

    elif farm == 'deulpul':

        image_req = image_procedure_pb2.ImageRequest(farm=farm, sector=sector, hasTIC=isTIC,camIdx=camidx)
        response = stub.getImage(image_req)

        img1 = ByteWithZlibToImg(response.imgByte1)
        img2 = ByteWithZlibToImg(response.imgByte2)

        if img1.shape[1] != 1920 and isTIC == 'cctv':
            img1 = cv2.resize(img1, dsize=(1920, 1080), interpolation=cv2.INTER_CUBIC)
            img2 = cv2.resize(img2, dsize=(1920, 1080), interpolation=cv2.INTER_CUBIC)

        resized = cv2.imencode('.jpg', img1)
        img_base64_string1 = base64.b64encode(resized[1]).decode()

        resized = cv2.imencode('.jpg', img2)
        img_base64_string2 = base64.b64encode(resized[1]).decode()

        return JSONResponse({"img1": img_base64_string1, "img2": img_base64_string2})

