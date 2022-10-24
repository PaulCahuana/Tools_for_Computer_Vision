import cv2
import numpy as np
size=[1,160,160,3]
img = cv2.imread("datasets/face_paul.jpg").astype(np.float32)
img = cv2.resize(img,None,None,2.5,2.5,cv2.INTER_LINEAR)
image = cv2.resize(img, (size[1], size[2]))
#rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image=image.T
image= np.expand_dims(image, 0)

net = cv2.dnn.readNetFromONNX("face_landmark_160x160.onnx")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableBackend(cv2.dnn.DNN_TARGET_CPU)

blobImage = cv2.dnn.blobFromImage(image,1.0,(img.shape[1],img.shape[0]))
outNames = net.getUnconnectedOutLayersNames()
net.setInput(blobImage)
outs = net.forward(outNames)
print("outs: ",outs)