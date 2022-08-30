import grpc

# import the generated classes
import image_procedure_pb2
import image_procedure_pb2_grpc

# data encoding

import numpy as np
import base64
import zlib
import time

# open a gRPC channel
channel = grpc.insecure_channel('192.168.2.1:5001')

# create a stub (client)
stub = image_procedure_pb2_grpc.ImageServerStub(channel)

# encoding image/numpy array

t1 = time.time()
image_req = image_procedure_pb2.ImageRequest(farm='deulpul', sector='1', camIdx='1-1')
response = stub.getImage(image_req)
print(response)
t2 = time.time()
print(t2 - t1)
