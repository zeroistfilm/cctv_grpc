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
from starlette.responses import JSONResponse
from typing import Optional, Any

app = FastAPI()
channel = grpc.insecure_channel('192.168.2.1:5001')
stub = image_procedure_pb2_grpc.ImageServerStub(channel)



@app.get('/api/getframe')
async def getframe():
    image_req = image_procedure_pb2.ImageRequest(farm='deulpul', sector='1', camIdx='1-2')
    response = stub.getImage(image_req)
    print(response)
