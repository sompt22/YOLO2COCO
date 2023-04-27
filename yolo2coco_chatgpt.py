import json

#CHATGPT

def yolo_to_coco(yolo_annotations, image_width, image_height):
    coco_annotations = {
        "info": {
            "description": "YOLO to COCO conversion",
            "version": "1.0",
            "year": 2023,
            "date_created": "2023-04-27"
        },
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": []
    }

    # Add categories
    coco_annotations["categories"].append({
        "id": 1,
        "name": "object",
        "supercategory": "none"
    })

    # Loop through YOLO annotations and convert to COCO format
    for i, yolo_annotation in enumerate(yolo_annotations):
        x_center, y_center, width, height, class_id = yolo_annotation
        x_min = int((x_center - width / 2) * image_width)
        y_min = int((y_center - height / 2) * image_height)
        coco_width = int(width * image_width)
        coco_height = int(height * image_height)

        # Add image
        coco_annotations["images"].append({
            "id": i,
            "width": image_width,
            "height": image_height,
            "file_name": f"{i}.jpg"
        })

        # Add annotation
        coco_annotations["annotations"].append({
            "id": i,
            "image_id": i,
            "category_id": 1,
            "bbox": [x_min, y_min, coco_width, coco_height],
            "area": coco_width * coco_height,
            "iscrowd": 0
        })

    return coco_annotations


# Example usage
yolo_annotations = [
    [0.3, 0.5, 0.4, 0.6, 0],
    [0.6, 0.4, 0.2, 0.3, 1]
]
image_width = 640
image_height = 480
coco_annotations = yolo_to_coco(yolo_annotations, image_width, image_height)
with open("coco_annotations.json", "w") as f:
    json.dump(coco_annotations, f)






import json

def yolo_to_coco(yolo_annotations, image_width, image_height):
    coco_annotations = {
        "info": {
            "description": "YOLO to COCO conversion",
            "version": "1.0",
            "year": 2023,
            "date_created": "2023-04-27"
        },
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": []
    }

    # Add categories
    coco_annotations["categories"].append({
        "id": 1,
        "name": "object",
        "supercategory": "none"
    })

    # Group YOLO annotations by track ID
    yolo_tracks = {}
    for yolo_annotation in yolo_annotations:
        class_id = int(yolo_annotation[4])
        track_id = int(yolo_annotation[5])
        if track_id not in yolo_tracks:
            yolo_tracks[track_id] = []
        yolo_tracks[track_id].append([yolo_annotation[:4], class_id])

    # Loop through YOLO tracks and convert to COCO format
    for i, (track_id, yolo_track) in enumerate(yolo_tracks.items()):
        # Add images
        for j, yolo_annotation in enumerate(yolo_track):
            image_id = i * len(yolo_track) + j
            coco_annotations["images"].append({
                "id": image_id,
                "width": image_width,
                "height": image_height,
                "file_name": f"{track_id}_{j}.jpg"
            })

        # Add annotations
        for j, (yolo_annotation, class_id) in enumerate(yolo_track):
            x_center, y_center, width, height = yolo_annotation
            x_min = int((x_center - width / 2) * image_width)
            y_min = int((y_center - height / 2) * image_height)
            coco_width = int(width * image_width)
            coco_height = int(height * image_height)
            image_id = i * len(yolo_track) + j

            coco_annotations["annotations"].append({
                "id": image_id,
                "image_id": image_id,
                "category_id": 1,
                "bbox": [x_min, y_min, coco_width, coco_height],
                "area": coco_width * coco_height,
                "iscrowd": 0
            })

    return coco_annotations


# Example usage
yolo_annotations = [
    [0.3, 0.5, 0.4, 0.6, 0, 1],
    [0.6, 0.4, 0.2, 0.3, 1, 1],
    [0.4, 0.3, 0.5, 0.4, 0, 2]





import json

def yolo_to_coco_with_tracks(yolo_annotations, image_width, image_height):
    coco_annotations = {
        "info": {
            "description": "YOLO to COCO conversion with tracks",
            "version": "1.0",
            "year": 2023,
            "date_created": "2023-04-27"
        },
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": []
    }

    # Add categories
    coco_annotations["categories"].append({
        "id": 1,
        "name": "object",
        "supercategory": "none"
    })

    # Initialize track ID counter
    track_id_counter = 1

    # Loop through YOLO annotations and convert to COCO format
    for seq_idx, seq_annotations in enumerate(yolo_annotations):
        # Add image
        coco_annotations["images"].append({
            "id": seq_idx,
            "width": image_width,
            "height": image_height,
            "file_name": f"{seq_idx}.jpg"
        })

        # Loop through sequence annotations and convert to COCO format
        for i, yolo_annotation in enumerate(seq_annotations):
            x_center, y_center, width, height, class_id, track_id = yolo_annotation
            x_min = int((x_center - width / 2) * image_width)
            y_min = int((y_center - height / 2) * image_height)
            coco_width = int(width * image_width)
            coco_height = int(height * image_height)

            # Add annotation
            coco_annotations["annotations"].append({
                "id": track_id_counter,
                "image_id": seq_idx,
                "category_id": 1,
                "track_id": track_id,
                "bbox": [x_min, y_min, coco_width, coco_height],
                "area": coco_width * coco_height,
                "iscrowd": 0
            })

            # Increment track ID counter
            track_id_counter += 1

    return coco_annotations


# Example usage
yolo_annotations = [
    [
        [0.3, 0.5, 0.4, 0.6, 0, 1],
        [0.6, 0.4, 0.2, 0.3, 1, 2]
    ],
    [
        [0.2, 0.3, 0.3, 0.4, 0, 3],
        [0.5, 0.6, 0.4, 0.3, 1, 4],
        [0.8, 0.5, 0.1, 0.1, 0, 5]
    ]
]
image_width = 640
image_height = 480
coco_annotations = yolo_to_coco_with_tracks(yolo_annotations, image_width, image_height)
with open("coco_annotations.json", "w") as f:
    json.dump(coco_annotations, f)



import matplotlib.pyplot as plt

def generate_track_id_histogram(yolo_annotations):
    # Extract track IDs from YOLO annotations
    track_ids = []
    for seq_annotations in yolo_annotations:
        for yolo_annotation in seq_annotations:
            _, _, _, _, _, track_id = yolo_annotation
            track_ids.append(track_id)

    # Create histogram of track IDs
    num_bins = len(set(track_ids))
    plt.hist(track_ids, bins=num_bins)
    plt.xlabel("Track ID")
    plt.ylabel("Count")
    plt.title("Histogram of Track IDs")
    plt.show()


# Example usage
yolo_annotations = [
    [
        [0.3, 0.5, 0.4, 0.6, 0, 1],
        [0.6, 0.4, 0.2, 0.3, 1, 2]
    ],
    [
        [0.2, 0.3, 0.3, 0.4, 0, 3],
        [0.5, 0.6, 0.4, 0.3, 1, 4],
        [0.8, 0.5, 0.1, 0.1, 0, 5]
    ]
]
generate_track_id_histogram(yolo_annotations)




import matplotlib.pyplot as plt

def generate_bbox_histograms(yolo_annotations):
    aspect_ratios = []
    heights = []
    widths = []

    for seq_annotations in yolo_annotations:
        for yolo_annotation in seq_annotations:
            _, _, bbox_width, bbox_height, _, _ = yolo_annotation
            aspect_ratio = bbox_width / bbox_height
            aspect_ratios.append(aspect_ratio)
            heights.append(bbox_height)
            widths.append(bbox_width)

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    axs[0].hist(aspect_ratios, bins=20)
    axs[0].set_xlabel("Aspect Ratio")
    axs[0].set_ylabel("Count")
    axs[0].set_title("Aspect Ratio Histogram")

    axs[1].hist(heights, bins=20)
    axs[1].set_xlabel("Height")
    axs[1].set_ylabel("Count")
    axs[1].set_title("Height Histogram")

    axs[2].hist(widths, bins=20)
    axs[2].set_xlabel("Width")
    axs[2].set_ylabel("Count")
    axs[2].set_title("Width Histogram")

    plt.show()


# Example usage
yolo_annotations = [
    [
        [0.3, 0.5, 0.4, 0.6, 0, 1],
        [0.6, 0.4, 0.2, 0.3, 1, 2]
    ],
    [
        [0.2, 0.3, 0.3, 0.4, 0, 3],
        [0.5, 0.6, 0.4, 0.3, 1, 4],
        [0.8, 0.5, 0.1, 0.1, 0, 5]
    ]
]
generate_bbox_histograms(yolo_annotations)


import os

def read_yolo_annotations(directory):
    yolo_annotations = []
    for seq_folder in os.listdir(directory):
        seq_annotations = []
        for file_name in os.listdir(os.path.join(directory, seq_folder)):
            if file_name.endswith('.txt'):
                with open(os.path.join(directory, seq_folder, file_name), 'r') as f:
                    annotations = []
                    for line in f:
                        bbox = [float(x) for x in line.strip().split()]
                        annotations.append(bbox)
                    seq_annotations.append(annotations)
        yolo_annotations.append(seq_annotations)
    return yolo_annotations

yolo_annotations = read_yolo_annotations('/path/to/annotation/directory')


import cv2

def overlay_boxes_on_images(yolo_annotations, image_directory, output_directory):
    for i, seq_annotations in enumerate(yolo_annotations):
        for j, annotations in enumerate(seq_annotations):
            image_file = os.path.join(image_directory, f"seq{i}_frame{j}.jpg")
            image = cv2.imread(image_file)
            for bbox in annotations:
                x, y, w, h, _, _ = bbox
                x1 = int((x - w/2) * image.shape[1])
                y1 = int((y - h/2) * image.shape[0])
                x2 = int((x + w/2) * image.shape[1])
                y2 = int((y + h/2) * image.shape[0])
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            output_file = os.path.join(output_directory, f"seq{i}_frame{j}.jpg")
            cv2.imwrite(output_file, image)

yolo_annotations = read_yolo_annotations('/path/to/annotation/directory')
image_directory = '/path/to/image/directory'
output_directory = '/path/to/output/directory'
overlay_boxes_on_images(yolo_annotations, image_directory, output_directory)
