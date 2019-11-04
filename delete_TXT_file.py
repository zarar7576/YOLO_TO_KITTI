#This is just a utility to delete all the text files in a folder
#Usage python3 delete_TXT_file.py coco/images

import argparse
import os
from tqdm import tqdm

image_height=256
image_width =256

parser = argparse.ArgumentParser()
# parser.add_argument("finput", help="echo the string you use here")
parser.add_argument("finput",help="Input files folder")
args = parser.parse_args()

input_path=args.finput

if not os.path.exists(input_path):
    # print("File Path :",args.finput," does not exist!!!!!")
    raise Exception(' File path: '+str(args.finput)+" dosent exis")
else:
    pass

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(input_path) if isfile(join(input_path, f))]

counter=0
txt_files=[]
for fnames in onlyfiles:
    if fnames[-4:]==".txt":
        counter=counter+1
        txt_files.append(input_path+"/"+fnames)
print(counter)

for dtf in tqdm(txt_files):
	os.remove(dtf)
