import os #librería para crear carpetas
import pandas as pd
from os import listdir
import random

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
        
        
    
