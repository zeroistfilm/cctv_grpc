import cv2
import zlib
import numpy as np
import sys
# img->jpg->byte->zib


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



img1 = cv2.imread('3.jpg')
compByte = imgToByteWithZlib(img1)
img =ByteWithZlibToImg(compByte)


cv2.imshow('1',img)
cv2.waitKey(0)



