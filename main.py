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
        txt_files.append(fnames)
print(counter)

for fnames in tqdm(txt_files):
    data=[]
    with open(input_path+"/"+fnames, 'r') as fh:

        data=fh.readlines()

    # print(data[0].replace('\n', '').split(" "))

    for cc,lines in enumerate(data):
        lines=lines.replace('\n', '').split(" ")
        # print(lines[2])
        lines[0]=int(lines[0])

        lines[1]=float(lines[1])*image_width
        lines[2]=float(lines[2])*image_height
        lines[3]=float(lines[3])*image_width
        lines[4]=float(lines[4])*image_height
            # print(lines[1+dd])


        n_line= [0] * 16
        n_line[0]=lines[0]
        n_line[4]=int(lines[1]-lines[3]/2)
        n_line[5]=int(lines[2]-lines[4]/2)
        n_line[6]=int(lines[1]+lines[3]/2)
        n_line[7]=int(lines[2]+lines[4]/2)

        for c,n in enumerate(n_line):
            if n<0:
                n_line[c]=1


        str1 = ' '.join(str(n_line)).replace(' ', '').replace(',', ' ').replace('[', '').replace("]","")
        # print(str1)
        data[cc]=str1+"\n"

    strf = " ".join(str(x) for x in data)

    strf=strf.replace("\n ","\n")

    file = open("KITTI/"+fnames, "w")
    file.write(strf)
    file.close()
