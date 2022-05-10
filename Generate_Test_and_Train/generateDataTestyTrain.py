import os #librería para crear carpetas
import pandas as pd
from os import listdir
import random
import shutil
from sklearn.model_selection import train_test_split
from glob import glob

#os.mkdir("Nivel_2") #creamos la carpeta para las imágenes
carpetaN1="Nivel_1"
carpetaN3="Nivel_3"
carpetaN1New="Nivel_1_temp"
os.mkdir(carpetaN1New) #creamos la carpeta para las imágenes
cantidadN3=len(os.listdir(carpetaN3))
cantidadN1=len(os.listdir(carpetaN1))
segmentar=cantidadN1-cantidadN3

#agregamos las imágenes faltantes
imagenes=os.listdir(carpetaN1)

while(True):
    imageRan=random.choice(imagenes)
    shutil.copy(carpetaN1+"/"+imageRan,carpetaN1New)
    cantidadTemp=len(os.listdir(carpetaN1New))
    if (cantidadTemp==cantidadN3):
        print("cantidad Creada: ",cantidadTemp)
        break

despierto = glob(carpetaN1New+'/*.jpg')
dormido= glob(carpetaN3+'/*.jpg')
despierto_train, despierto_test = train_test_split(despierto, test_size=0.2)
dormido_train, dormido_test = train_test_split(dormido, test_size=0.2)

carpetas= ["TRAIN","TEST"]
clases=["despierto", "dormido"]

for i in carpetas:
    os.mkdir(i)
    for j in clases:
        os.mkdir(i+"/"+j)
        if(i=="TRAIN"):
            if(j=="despierto"):
                imageRan=random.sample(despierto_train,len(despierto_train))
                for k in imageRan:
                    shutil.copy(k,i+"/"+j)
            if(j=="dormido"):
                imageRan=random.sample(dormido_train,len(dormido_train))
                for k in imageRan:
                    shutil.copy(k,i+"/"+j)

        if(i=="TEST"):
            if(j=="despierto"):
                imageRan=random.sample(despierto_test,len(despierto_test))
                for k in imageRan:
                    shutil.copy(k,i+"/"+j)
            if(j=="dormido"):
                imageRan=random.sample(dormido_test,len(dormido_test))
                for k in imageRan:
                    shutil.copy(k,i+"/"+j)