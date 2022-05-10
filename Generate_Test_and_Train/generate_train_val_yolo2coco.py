import argparse
import os
import random
from shutil import copyfile
from sklearn.model_selection import train_test_split
from glob import glob
import shutil


parser = argparse.ArgumentParser()
parser.add_argument(
    '--data', help='Path to dataset', type=str, default=0)
args = parser.parse_args()

input_data_path = os.path.join(args.data)


train_ratio = 0.75
validation_ratio = 0.15
test_ratio = 0.10

clase = glob(input_data_path+'/images'+'/*.jpg')
print(clase)
trainClase, testClase = train_test_split(clase, test_size=1 - train_ratio)
        
print()
print()
print(trainClase)

file = open("train.txt", "w")
for  i in trainClase:
    file.write(i+"\n")
file.close()

file = open("val.txt", "w")
for  i in testClase:
    file.write(i+"\n")
#file.write(testClase)
file.close()


"""



# create target training directories
sets = ["train", "test", "val"]

# iter over dataset and fill
print("Copying dataset to new split dataset: ", data_path)
#print(len(os.listdir(input_data_path)))
print(clf_classes) #class
print(sets) # train,test,val
###############################################

train_ratio = 0.75
validation_ratio = 0.15
test_ratio = 0.10

#files creations
for  i in sets:# train,test,val
    os.mkdir(data_path+"/"+i)
    for j in clf_classes:#class
        os.mkdir(data_path+"/"+i+"/"+j)

for  i in sets:# train,test,val
    for j in clf_classes:#class
        # train is now 75% of the entire data set
        # the _junk suffix means that we drop that variable completely
        clase = glob(input_data_path+'/'+j+'/*.png')
        print(clase)
        trainClase, testClase = train_test_split(clase, test_size=1 - train_ratio)
        # test is now 10% of the initial data set
        # validation is now 15% of the initial data set
        valClase, testClase= train_test_split(testClase, test_size=test_ratio/(test_ratio + validation_ratio)) 
        #print ("para "+i+" :"+ str(len(trainClase))+'  '+ str(len(testClase)) +'  '+str (len(valClase)))
        if(i=="train"):
            for k in trainClase:
                shutil.copy(k,data_path+"/"+i+"/"+j)
        if(i=="test"):
            for k in testClase:
                shutil.copy(k,data_path+"/"+i+"/"+j)
        if(i=="val"):
            for k in valClase:
                shutil.copy(k,data_path+"/"+i+"/"+j)

# write labels file for main dir
labels_file_path = os.path.join(data_path, "labels.txt")
with open(labels_file_path, "w") as f:
    for cat in clf_classes:
        f.write(cat)
        f.write("\n")

print("Wrote labels file to {}".format(labels_file_path))
print(" ")
print("Processed finished!!!")
"""