# -Creating-a-metrics-module-that-will-take-the-predicted-JSON-and-ground-truth-JSON-as-input.
1. P&amp;ID Image: A diagram image. 2. Predicted JSON: A JSON file containing text extracted from the image using a data science module. 3. Ground Truth JSON: A JSON file containing manually curated text from the P&amp;ID.
Contents
Importing Libraries: Necessary libraries for handling JSON data, displaying images, and plotting.
Function Definitions:
load_json(file_path): Loads JSON data from the specified file.
draw_bounding_boxes(image_path, gt_json_path, output_image_path): Draws bounding boxes on images.
iou(bbox1, bbox2): Calculates the Intersection over Union for two bounding boxes.
match_bounding_boxes(gt_boxes, pred_boxes, iou_threshold): Matches ground truth and predicted bounding boxes based on IoU.
calculate_metrics(gt_json, pred_json): Calculates evaluation metrics such as precision and recall.
Visualization:
Visualizes both ground truth and predicted bounding boxes on images.
Loading Data: Example code for loading ground truth and predicted JSON files.
Analysis: Explanation of the need for IoU and how it is used in the context of object detection.
Prerequisites:
  Python 3.x
  Jupyter Notebook or Google Colab
  Required libraries: json, matplotlib, cv2, etc.
Functions
load_json(file_path)
Loads JSON data from the specified file path.

draw_bounding_boxes(image_path, gt_json_path, output_image_path)
Draws bounding boxes on the given image using ground truth data.

iou(bbox1, bbox2)
Calculates the Intersection over Union for two bounding boxes.

match_bounding_boxes(gt_boxes, pred_boxes, iou_threshold)
Matches ground truth and predicted bounding boxes based on the IoU threshold.

calculate_metrics(gt_json, pred_json)
Calculates evaluation metrics such as precision and recall based on the ground truth and predicted JSON data.

Visualization
Includes functions to visualize ground truth and predicted bounding boxes on images, helping to understand the performance of the object detection model.

Finally Creating a Flask App to visualise the Metric Report in the web.

![Screenshot (27)](https://github.com/kellasarath30/-Creating-a-metrics-module-that-will-take-the-predicted-JSON-and-ground-truth-JSON-as-input./assets/102147901/42ed8fd2-2b5b-46d4-a0ce-b324d441185e)

![Screenshot (28)](https://github.com/kellasarath30/-Creating-a-metrics-module-that-will-take-the-predicted-JSON-and-ground-truth-JSON-as-input./assets/102147901/220d33d0-e2aa-44bc-aa08-a25b9b2481c9)

![Screenshot (29)](https://github.com/kellasarath30/-Creating-a-metrics-module-that-will-take-the-predicted-JSON-and-ground-truth-JSON-as-input./assets/102147901/7d22fee2-498b-4956-aecb-b40b05a122c5)

