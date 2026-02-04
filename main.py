import argparse
import os
from tqdm import tqdm

# Image dimensions used to de-normalize YOLO coordinates.
# Update these if your dataset images are not 256x256.
image_height = 256
image_width = 256

parser = argparse.ArgumentParser()
# parser.add_argument("finput", help="echo the string you use here")
parser.add_argument("finput",help="Input files folder")
args = parser.parse_args()

input_path = args.finput

# Output folder is created alongside the input folder name.
output_path = "KITTI_" + input_path
if not os.path.exists(output_path):
    os.mkdir(output_path)


if not os.path.exists(input_path):
    # Fail fast if the provided folder is missing.
    raise Exception("File path: " + str(args.finput) + " does not exist")



from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(input_path) if isfile(join(input_path, f))]

counter = 0
txt_files = []
for fnames in onlyfiles:
    # Only convert YOLO label files (one per image).
    if fnames[-4:] == ".txt":
        counter = counter + 1
        txt_files.append(fnames)
print(counter)

for fnames in tqdm(txt_files):
    data = []
    with open(input_path + "/" + fnames, "r") as fh:
        # Read all label rows for this image.
        data = fh.readlines()

    # print(data[0].replace('\n', '').split(" "))

    for cc, lines in enumerate(data):
        # YOLO fields: class_id x_center y_center width height (normalized 0..1)
        lines = lines.replace("\n", "").split(" ")
        lines[0] = int(lines[0])

        # Convert normalized values to pixel space.
        lines[1] = float(lines[1]) * image_width
        lines[2] = float(lines[2]) * image_height
        lines[3] = float(lines[3]) * image_width
        lines[4] = float(lines[4]) * image_height

        # Prepare KITTI-like output array (15 fields).
        n_line = [0] * 15
        # Map class ids to string labels (customize for your dataset).
        if lines[0] == 1:
            lines[0] = "other"
        else:
            lines[0] = "car"
        n_line[0] = lines[0]

        # Convert center/size to left, top, right, bottom corners.
        n_line[4] = int(lines[1] - lines[3] / 2)
        n_line[5] = int(lines[2] - lines[4] / 2)
        n_line[6] = int(lines[1] + lines[3] / 2)
        n_line[7] = int(lines[2] + lines[4] / 2)

        # Clamp numeric fields to image bounds (1..255 for 256x256 images).
        for c, n in enumerate(n_line):
            if not c == 0:
                if n < 0:
                    n_line[c] = 1
                if n > 256:
                    n_line[c] = 255

        # Populate remaining KITTI fields with defaults.
        for cc2, char in enumerate(n_line):
            if cc2 == 1:
                n_line[cc2] = float(0)
            if cc2 > 7:
                n_line[cc2] = 1

        # Format as a space-separated KITTI-like line.
        str1 = (
            " ".join(str(n_line))
            .replace(" ", "")
            .replace(",", " ")
            .replace("[", "")
            .replace("]", "")
            .replace("'", "")
            .replace('"', "")
        )
        data[cc] = str1 + "\n"

    strf = " ".join(str(x) for x in data)
    strf = strf.replace("\n ", "\n")

    # Write converted labels to the output directory.
    file = open(output_path + "/" + fnames, "w")
    file.write(strf)
    file.close()
