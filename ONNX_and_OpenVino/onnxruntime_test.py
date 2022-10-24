import onnxruntime as rt
import numpy as np
import time 
from tqdm import tqdm
import cv2


limit = 5
# MODEL
size=[1,160,160,3]
device = 'CPU_FP32'
model_file_path = 'face_landmark_160x160.onnx'
image_test="datasets/face_paul.jpg"
image = cv2.imread(image_test).astype(np.float32)  #np.random.rand(1, 3, 160, 160).astype(np.float32)

#image =np.random.rand(1, 3, 160, 160).astype(np.float32)
image = cv2.resize(image, (size[1], size[2]))
#rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image=image.T
image= np.expand_dims(image, 0)
print("image size: ", image.shape)
# OnnxRuntime
print("OnnxRuntime ")
sess = rt.InferenceSession(model_file_path, providers=['CPUExecutionProvider'], provider_options=[{'device_type' : device}])
input_name = sess.get_inputs()[0].name

start = time.time()
for i in tqdm(range(limit)):
    out = sess.run(None, {input_name: image})
    #out = sess.run(None, {input_name: [image]})
end = time.time()
inference_time = end - start
print(inference_time)
print("output_prediction: ",out)
print()
print()
print("OnnxRuntime + OpenVinoEP")

# OnnxRuntime + OpenVinoEP
sess = rt.InferenceSession(model_file_path, providers=['OpenVINOExecutionProvider'], provider_options=[{'device_type' : device}])
input_name = sess.get_inputs()[0].name

start = time.time()
for i in tqdm(range(limit)):
    out = sess.run(None, {input_name: image})
end = time.time()
inference_time = end - start
print(inference_time)
print("output_prediction: ",out)