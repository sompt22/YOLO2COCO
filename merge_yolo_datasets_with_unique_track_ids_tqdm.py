import os
import shutil
import cv2
from tqdm import tqdm

def merge_yolo_datasets_with_unique_track_ids(input_dirs, output_dir):
    # Create output directories
    os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'annotations'), exist_ok=True)

    # Initialize track ID offset
    track_id_offset = 0

    # Iterate over input directories
    for input_dir in input_dirs:
        # Iterate over annotation files in input directory
        for root, dirs, files in os.walk(input_dir):
            for file in tqdm(files, desc=f"Merging {input_dir}"):
                if file.endswith('.txt'):
                    annotation_path = os.path.join(root, file)

                    # Load annotations from file
                    with open(annotation_path, 'r') as f:
                        annotations = f.readlines()

                    # Modify track IDs to ensure uniqueness across input directories
                    for i in range(len(annotations)):
                        annotations[i] = annotations[i].split()
                        track_id = int(annotations[i][1])
                        annotations[i][1] = str(track_id + track_id_offset)
                        annotations[i] = ' '.join(annotations[i]) + '\n'

                    # Save modified annotations to output file
                    output_annotation_path = os.path.join(output_dir, 'annotations', file)
                    with open(output_annotation_path, 'a') as f:
                        f.writelines(annotations)

                    # Copy corresponding image file to output directory
                    image_path = os.path.splitext(annotation_path)[0] + '.jpg'
                    if os.path.exists(image_path):
                        output_image_path = os.path.join(output_dir, 'images', os.path.basename(image_path))
                        shutil.copyfile(image_path, output_image_path)
                    else:
                        # Convert .png to .jpg if .png file exists
                        image_path = os.path.splitext(annotation_path)[0] + '.png'
                        if os.path.exists(image_path):
                            img = cv2.imread(image_path)
                            output_image_path = os.path.join(output_dir, 'images', os.path.basename(image_path).replace('.png', '.jpg'))
                            cv2.imwrite(output_image_path, img)
                        else:
                            print(f"Warning: no corresponding image found for {annotation_path}")
                            continue

                    # Check if bounding box coordinates are within image
                    img = cv2.imread(output_image_path)
                    img_height, img_width = img.shape[:2]
                    for annotation in annotations:
                        x, y, w, h = map(float, annotation.split()[2:])
                        if x < 0:
                            x = 0
                        if y < 0:
                            y = 0
                        if x + w > img_width:
                            w = img_width - x
                        if y + h > img_height:
                            h = img_height - y
                        annotation = f"{annotation.split()[0]} {annotation.split()[1]} {int(x)} {int(y)} {int(w)} {int(h)}\n"

                    # Save modified annotations to output file
                    with open(output_annotation_path, 'w') as f:
                        f.writelines(annotations)

        # Update track ID offset
        track_id_offset += len(annotations)

    print(f"Merged {len(input_dirs)} YOLO datasets with unique track IDs into {output_dir}")




