
import os
import cv2
import argparse
import shutil
import random

def pascal_voc_to_yolo(image,line):
    """ This function will convert from voc to yolo format
    Args:
        image: Image to get shapes of the current line 
        line: Coordinates of the bbox in voc format (list of words from a line of the voc format)
    Returns:
            Returns a string of the coordinates of the bbox in yolo format
    """
    image_h= int(image.shape[0])
    image_w= int(image.shape[1])

    words=line.split()
    x1=int(float(words[0]))
    y1=int(float(words[1]))
    x2=int(float(words[2]))
    y2=int(float(words[3]))
    x1, y1, x2, y2, image_w, image_h
    result_pascal_voc_to_yolo=[((x2 + x1)/(2*image_w)), ((y2 + y1)/(2*image_h)), (x2 - x1)/image_w, (y2 - y1)/image_h]
    result_pascal_voc_to_yolo=" ".join(str(x) for x in result_pascal_voc_to_yolo)
    return result_pascal_voc_to_yolo


def get_iou(bb1,bb2):
    """ This function will get the IoU (Intersection over Union) from 2 bboxes
    Args:
        bb1: First bbox to be processed
        bb2: Second bbox to be processed
    Returns:
            Returns a string of the coordinates of the bbox in yolo format
    """
    assert bb1[0] < bb1[2]
    assert bb1[1] < bb1[3]
    assert bb2[0] < bb2[2]
    assert bb2[1] < bb2[3]

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1[0], bb2[0])
    y_top = max(bb1[1], bb2[1])
    x_right = min(bb1[2], bb2[2])
    y_bottom = min(bb1[3], bb2[3])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (bb1[2] - bb1[0]) * (bb1[3] - bb1[1])
    bb2_area = (bb2[2] - bb2[0]) * (bb2[3] - bb2[1])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou


def get_clean_values(labels):
    """ This function will change only the first word of each label,
        this procees is neccesary to  avoid problems with yolo format
    Args:
        labels: list of lists that contains whole the lines of the file of the label
    Returns:
            Returns a list of lists with the values necessary to do the preprocessing
    """
    list_b_decoded_main=[]
    for line in labels:
        words=line.split()
        x1=int(float(words[2]))
        y1=int(float(words[3]))
        x2=int(float(words[4]))
        y2=int(float(words[5]))

        value_label=words[1]
        line_temp = value_label + " "+ str(x1)+ " "+ str(y1)+ " "+ str(x2)+ " "+ str(y2) 
        list_b_decoded_main.append(line_temp.split())
    return list_b_decoded_main

def get_values_necessarily(list_b_decoded_main):
    """ This function will work geting the IoU with 2 bboxes
    Args:
        list_b_decoded_main: list of lists that contains whole the lines of the file of the label
    Returns:
        Returns a list of lists with the values necessary
    """
    
    for i in list_b_decoded_main:
        bb_main=list(map(int, i[1:]))
        bb_main_class=i[0]
        for j in list_b_decoded_main:

            bb_temp=list(map(int, j[1:]))
            bb_temp_class=j[0]

            b1 = set(bb_main)
            b2 = set(bb_temp)
            if b1!=b2:
                result_iou=get_iou(bb_main,bb_temp)                
                if(result_iou>0):
                    if bb_main_class==class_iou and i in list_b_decoded_main:
                        list_b_decoded_main.remove(i)
                    if bb_temp_class==class_iou and j in list_b_decoded_main:
                        list_b_decoded_main.remove(j)
    return list_b_decoded_main

def dataimage_to_yolo(image,line):
    """ This function will iterate line by line, in order to get the yolo format
    Args:
        line: list that contains the label
    Returns:
        Returns a list of lists with the values already converted
    """
    list_result=[]
    for i in line:
        line_temp=i[1]+" "+i[2]+" "+i[3]+" "+i[4]
        result_yolo="0 "+pascal_voc_to_yolo( image,line_temp)
        list_result.append(result_yolo)
    return list_result

def transform_data(arr):
    """ This function will manage all the pipeline to do the convertions
    Args:
        arr: list that contains whole the labels in raw format
    """
    for x in arr:
        labels = open(path_labels+x, "r")        
        images=path_main+"/"+x[:-3]+"jpg"
        image = cv2.imread(images)
        image_raw=cv2.imread(images)
        list_b_decoded_main=get_clean_values(labels)
        if(iou):
            list_b_decoded_main=get_values_necessarily(list_b_decoded_main)
        list_b_decoded_main=dataimage_to_yolo(image,list_b_decoded_main)
        new_labels=open(destination+"/"+x, "a")
        line=""
        for i in list_b_decoded_main:
            line= i
            new_labels.write(line+"\n")
        new_labels.close()

parser = argparse.ArgumentParser(description='OpenImage preprocessing for YOLO Training')
parser.add_argument('--data_path', default='Dataset', type=str, help='path of the file "Dataset"')
parser.add_argument('--iou', default=1, type=int, help=" '1' If we will use IoU or '0' if we won't use it")
parser.add_argument('--iou_class', default='-', type=str, help="Class that we will give less importance, using iou")
print("Dataset path: ",parser.parse_args().data_path)

path_main=parser.parse_args().data_path
iou=parser.parse_args().iou
class_iou=parser.parse_args().iou_class


path_main_backup_to_delete=path_main
class_unique=(os.listdir(path_main+"/train"))[0]
carpet=class_unique
destination=path_main+"_new"
destination_labels=path_main+"_new/"+"Label"
destination_labels_cleaned=path_main+"_new/"+"labels"
os.mkdir(destination)
os.mkdir(destination_labels)

divided_dataset=os.listdir(path_main)
for i in divided_dataset:
    source=path_main+"/"+i+"/"+carpet
    files= os.listdir(source)
    for j in files:
        if j == "Label":
            files_labels=os.listdir(source+"/"+j)
            for k in files_labels:
                file_text=source+"/"+j+"/"+k
                shutil.move(file_text,destination_labels )
        else:
            file_img=source+"/"+j
            shutil.move(file_img,destination )


path_main=destination
path_labels=path_main+"/Label/"
arr = os.listdir(path_labels)
transform_data(arr)
shutil.rmtree(destination_labels)
shutil.rmtree(path_main_backup_to_delete)

######################### CREATING THE FILES FOR YOLO FORMAT #######################################

carpetaPrincipal=destination
carpetaImagenesGenerada="DB_YOLO_"+carpetaPrincipal

archivos=os.listdir(carpetaPrincipal)
os.makedirs(carpetaImagenesGenerada)

train=0.7
validation=0.2
test=0.1

countImageNombre=0
countSegundos=0

#carpetasDataset=["train","test"]
carpetasDataset=["images","labels"]
carpetasRaices=["train","val","test"]

for i in carpetasDataset:
    os.makedirs(carpetaImagenesGenerada+"/"+i)
    for k in carpetasRaices:
        os.makedirs(carpetaImagenesGenerada+"/"+i+"/"+k)
path = carpetaPrincipal

lstFiles = []
lstDir = os.walk(path)  

#Create a list of jpg files that exist in the directory and include them in the list.
for root, dirs, files in lstDir:
    for fichero in files:
        (nombreFichero, extension) = os.path.splitext(fichero)
        if(extension == ".jpg"):
            lstFiles.append(nombreFichero+extension)             

lstFiles=random.sample(lstFiles, len(lstFiles))                
print("only images: ",len(lstFiles) )
cantidadArchivos=len(archivos)/2 #total quantity of files


cantTrain=int(cantidadArchivos*train)
cantValidation=int(cantidadArchivos*validation)
cantTest=int(cantidadArchivos*test)

print("total images in train: ",cantTrain)
print("total images in validation: ",cantValidation)
print("total images in test: ",cantTest)

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

shutil.rmtree(destination)
print("finished!")
