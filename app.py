from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import json

app = Flask(__name__)

# Define paths for uploaded files
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def iou(bbox1, bbox2):
    x1_max = max(bbox1[0][0], bbox2[0][0])
    y1_max = max(bbox1[0][1], bbox2[0][1])
    x2_min = min(bbox1[2][0], bbox2[2][0])
    y2_min = min(bbox1[2][1], bbox2[2][1])
    
    inter_area = max(0, x2_min - x1_max) * max(0, y2_min - y1_max)
    
    bbox1_area = (bbox1[2][0] - bbox1[0][0]) * (bbox1[2][1] - bbox1[0][1])
    bbox2_area = (bbox2[2][0] - bbox2[0][0]) * (bbox2[2][1] - bbox2[0][1])
    
    union_area = bbox1_area + bbox2_area - inter_area
    
    if union_area == 0:
        return 0.0
    
    return inter_area / union_area

def match_bounding_boxes(gt_boxes, pred_boxes, iou_threshold=0.5):
    matches = []
    used_preds = set()
    
    for gt_key, gt_val in gt_boxes.items():
        best_iou = 0
        best_pred_key = None
        
        for pred_key, pred_val in pred_boxes.items():
            if pred_key in used_preds:
                continue
            current_iou = iou(gt_val['bbox'], pred_val['bbox'])
            if current_iou > best_iou:
                best_iou = current_iou
                best_pred_key = pred_key
        
        if best_iou >= iou_threshold:
            matches.append((gt_key, best_pred_key))
            used_preds.add(best_pred_key)
    
    return matches

def calculate_metrics(gt_json, pred_json):
    gt_boxes = {k: v for k, v in gt_json.items()}
    pred_boxes = {k: v for k, v in pred_json.items()}
    
    matches = match_bounding_boxes(gt_boxes, pred_boxes)
    
    tp = len(matches)
    fp = len(pred_boxes) - tp
    fn = len(gt_boxes) - tp
    
    precision = tp / (tp + fp) if tp + fp > 0 else 0
    recall = tp / (tp + fn) if tp + fn > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
    
    text_matches = sum(1 for gt_key, pred_key in matches if gt_boxes[gt_key]['text'] == pred_boxes[pred_key]['text'])
    text_accuracy = text_matches / tp if tp > 0 else 0
    
    metrics = {
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'text_accuracy': text_accuracy
    }
    
    return metrics

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files or 'gt_json' not in request.files or 'pred_json' not in request.files:
        return redirect(request.url)
    
    image = request.files['image']
    gt_json_file = request.files['gt_json']
    pred_json_file = request.files['pred_json']
    
    if image.filename == '' or gt_json_file.filename == '' or pred_json_file.filename == '':
        return redirect(request.url)
    
    if image and gt_json_file and pred_json_file:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        gt_json_path = os.path.join(app.config['UPLOAD_FOLDER'], gt_json_file.filename)
        pred_json_path = os.path.join(app.config['UPLOAD_FOLDER'], pred_json_file.filename)
        
        image.save(image_path)
        gt_json_file.save(gt_json_path)
        pred_json_file.save(pred_json_path)
        
        metrics = calculate_metrics(load_json(gt_json_path), load_json(pred_json_path))
        
        return render_template('result.html', metrics=metrics)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
