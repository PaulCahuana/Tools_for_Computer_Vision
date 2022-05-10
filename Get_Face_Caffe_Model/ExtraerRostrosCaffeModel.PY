from PIL import Image,ImageOps
import os #librería para crear carpetas
import shutil # librería para copiar archivos
import numpy as np
import argparse
import cv2
from matplotlib import cm

def carpetaCNNFace(direccionA, direccionB):
    #shutil.rmtree(direccionB)
    imagenes=os.listdir(direccionA)
    os.mkdir(direccionB) #creamos la carpeta para las imágenes
    direccionA=direccionA+"/"
    direccionN=direccionB+"/"
    for i in imagenes:
        imagenT=direccionA+i
        image=cnnFace(direccionN+i,imagenT)
    return    

def cnnFace(direccionN,pathImage):
    protoxt="deploy.prototxt.txt"
    model="res10_300x300_ssd_iter_140000.caffemodel"
    confidence_=0.5
    try:
        net = cv2.dnn.readNetFromCaffe(protoxt, model)
        # load the input image and construct an input blob for the image
        # by resizing to a fixed 300x300 pixels and then normalizing it
        image = cv2.imread(pathImage)        
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0))
        # pass the blob through the network and obtain the detections and
        net.setInput(blob)
        detections = net.forward()
        # loop over the detections
        imagenN=0
        for i in range(0,detections.shape[2]):
            confidence=detections[0,0,i,2]
            # filter out weak detections by ensuring the `confidence` is
            if(confidence > confidence_):
                # compute the (x, y)-coordinates of the bounding box for the
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                
                
                faceWidth=endX-startX                
                # draw the bounding box of the face along with the associated
                text = "{:.2f}%".format(confidence * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                #cv2.rectangle(image, (startX-100, startY-100), (endX+100, endY+100),(0, 0, 255), 2)
                #cv2.putText(image, text, (startX-100, y-100),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                #cv2.rectangle(image, (startX-100, startY-100), (endX+100, endY+100),(0, 0, 255), 2)
              
                pad=int(0.25*faceWidth)
                #print("pad: ",pad) # pad que se ajusta a la imágen para extraer solo rostro
                
                y1 = startY - pad if startY - pad > 0 else 0
                y2 =endY  + pad if endY + pad < h else h
                x1 = startX - pad if startX - pad > 0 else 0
                x2 = endX + pad if endX + pad < w else w                 
                imagenN=image[y1:y2, x1:x2]
                imagenN=cv2.cvtColor(imagenN, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(direccionN,imagenN)
    except:
        pass

    # show the output image
    #cv2.imshow("Output", imagenN)
    #cv2.waitKey(0)
    
    return 

carpetaCNNFace("N3", "N3_ROSTROS")