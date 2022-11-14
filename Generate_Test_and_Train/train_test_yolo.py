#SI TODO ESTÁ EN ORDEN
import os #librería para crear carpetas
import cv2
import shutil #librería para copiar archivos
import random
carpetaPrincipal="Dataset_new"
carpetaImagenesGenerada="DB_YOLO_"+carpetaPrincipal

archivos=os.listdir(carpetaPrincipal) #extraemos todos los archivos
os.makedirs(carpetaImagenesGenerada) #creamos la carpeta

train=0.7
validation=0.2
test=0.1

countImageNombre=0
countSegundos=0

#carpetasDataset=["train","test"]
carpetasDataset=["images","labels"]
carpetasRaices=["train","val","test"]

for i in carpetasDataset:
    os.makedirs(carpetaImagenesGenerada+"/"+i) #creamos la carpeta
    for k in carpetasRaices:
        os.makedirs(carpetaImagenesGenerada+"/"+i+"/"+k) #creamos la carpeta
            
#Variable para la ruta al directorio
path = carpetaPrincipal

#Lista vacia para incluir los ficheros
lstFiles = []
 
#Lista con todos los ficheros del directorio:
lstDir = os.walk(path)   #os.walk()Lista directorios y ficheros

#Crea una lista de los ficheros jpg que existen en el directorio y los incluye a la lista.
 
for root, dirs, files in lstDir:
    for fichero in files:
        (nombreFichero, extension) = os.path.splitext(fichero)
        if(extension == ".jpg"):
            lstFiles.append(nombreFichero+extension)
            #print (nombreFichero+extension)
             

lstFiles=random.sample(lstFiles, len(lstFiles))                
print("Solo imagenes: ",len(lstFiles) )#SOLO JPG       
cantidadArchivos=len(archivos)/2 #cantidad de archivos en total


cantTrain=int(cantidadArchivos*train)
cantValidation=int(cantidadArchivos*validation)
cantTest=int(cantidadArchivos*test)

print("total imagenes en train: ",cantTrain)
print("total imagenes en validation: ",cantValidation)
print("total imagenes en test: ",cantTest)

countTrain=0
countValidation=0
counTest=0

flag=0
for i in lstFiles:
    imagen=i
    nombreTexto=imagen[:-4]+".txt"
    if(flag==0):
        if(countTrain<cantTrain):
            shutil.move(carpetaPrincipal+"/"+imagen, carpetaImagenesGenerada+"/images/train/"+imagen)
            shutil.move(carpetaPrincipal+"/"+nombreTexto, carpetaImagenesGenerada+"/labels/train/"+nombreTexto)
            countTrain=countTrain+1
        else:
            flag=1
            
    if(flag==1):
        if(countValidation<cantValidation):
            shutil.move(carpetaPrincipal+"/"+imagen, carpetaImagenesGenerada+"/images/val/"+imagen)
            shutil.move(carpetaPrincipal+"/"+nombreTexto, carpetaImagenesGenerada+"/labels/val/"+nombreTexto)
            countValidation=countValidation+1
        else:
            flag=2
    if(flag==2):
        if(counTest<cantTest):
            shutil.move(carpetaPrincipal+"/"+imagen, carpetaImagenesGenerada+"/images/test/"+imagen)
            shutil.move(carpetaPrincipal+"/"+nombreTexto, carpetaImagenesGenerada+"/labels/test/"+nombreTexto)
            counTest=counTest+1

print("terminó!")