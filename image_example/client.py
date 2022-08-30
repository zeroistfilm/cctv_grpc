import grpc
# import the generated classes
import image_procedure_pb2
import image_procedure_pb2_grpc
# data encoding
import numpy as np
import base64
import zlib
import time

from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.responses import JSONResponse, Response
from typing import Optional, Any

app = FastAPI()
channel = grpc.insecure_channel('192.168.2.1:5001')
stub = image_procedure_pb2_grpc.ImageServerStub(channel)


@app.get("/cctv/{farm}/{sector}/{isTIC}/{camidx}")
async def getframe():

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
        url = f'http://192.168.2.1:8000/cctv/{farm}/{sector}/{isTIC}/{camidx}'

        image_req = image_procedure_pb2.ImageRequest(farm='deulpul', sector='1', camIdx='1-1')
        response = stub.getImage(image_req)
        print(type(response.imageString))
        return Response(response.imageString)

        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(url) as resp:
                respCompImg = await resp.read()
                decompimg = zlib.decompress(respCompImg).decode("utf-8")
                decompimg = json.loads(decompimg)

                img1 = getImageFromString(decompimg['img1'])
                img2 = getImageFromString(decompimg['img2'])

                if img1.shape[1] != 1920 and isTIC == 'cctv':
                    img1 = cv2.resize(img1, dsize=(1920, 1080), interpolation=cv2.INTER_CUBIC)
                    img2 = cv2.resize(img2, dsize=(1920, 1080), interpolation=cv2.INTER_CUBIC)

                resized = cv2.imencode('.jpg', img1)
                img_base64_string1 = base64.b64encode(resized[1]).decode()

                resized = cv2.imencode('.jpg', img2)
                img_base64_string2 = base64.b64encode(resized[1]).decode()

                return JSONResponse({"img1": img_base64_string1, "img2": img_base64_string2})



