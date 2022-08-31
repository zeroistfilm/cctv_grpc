
import grpc
# import the generated classes
import image_procedure_pb2
import image_procedure_pb2_grpc

channel = grpc.insecure_channel('192.168.2.1:5001')
stub = image_procedure_pb2_grpc.ImageServerStub(channel)

image_req = image_procedure_pb2.ImageRequest(farm='deulpul', sector='1', hasTIC='cctv', camIdx='1-1')
response = stub.getImage(image_req)
print(response)