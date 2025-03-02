from ultralytics import YOLO
from IPython.display import Image
import cv2
import easyocr
import re
import pandas as pd 
model = YOLO("best.pt")

results = model.track(source = "fire1.mp4", save = True, conf = 0.01, iou = 0.3)
result_image_path = str(results[0].save_dir)

print(result_image_path)