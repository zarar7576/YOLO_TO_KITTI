# YOLO_TO_KITTI
Convert YOLO-format label files to KITTI-format labels for use with NVIDIA Transfer Learning Toolkit (TLT) or other KITTI-based pipelines.

## Features
- Converts YOLO `.txt` labels into KITTI-like annotation text files.
- Preserves one output file per input label file.
- Writes results to a `KITTI_<input_folder>` directory.

## Input/Output formats
### YOLO input (per line)
```
<class_id> <x_center> <y_center> <width> <height>
```
All coordinate values are normalized in the range `[0, 1]`.

### KITTI-like output (per line)
```
<type> <truncated> <occluded> <alpha> <bbox_left> <bbox_top> <bbox_right> <bbox_bottom> <h> <w> <l> <x> <y> <z> <rotation_y>
```
Example:
```
car 0.0 0 0 7 0 39 32 1 1 1 1 1 1 1
```

> Note: The current script uses a fixed image size of 256x256 when converting normalized coordinates to pixels.

## Usage
```
python3 main.py "<folder_path>"
```

- `<folder_path>` must contain YOLO label `.txt` files.
- Output will be written to `KITTI_<folder_path>/`.

## Example
```
python3 main.py labels
```
This creates a `KITTI_labels/` folder with converted annotation files.

## Tips
- Ensure your images are 256x256 (or update `image_width` / `image_height` in `main.py`).
- The script currently maps class `1` to `other` and all other classes to `car`.

