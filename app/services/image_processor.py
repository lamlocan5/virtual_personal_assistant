import pytesseract
import cv2
import json
import os
import re
import textwrap
from PIL import Image

def get_text_from_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3), 0) #giảm nhiễu bằng GaussianBlur
    #gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 10)
    
    text = pytesseract.image_to_string(gray, lang="vie+eng")
    # if "\n" in text:
    #     text = text.replace("\n", " ")
    return text

def save_to_json(image_path, json_dir):
    text = get_text_from_image(image_path)

    filename = os.path.splitext(os.path.basename(image_path))[0]
    json_path = os.path.join(json_dir, f"{filename}.json")

    data = {
        "image_path": image_path,
        "extracted_text": text
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Saved successfully: {json_path}")

image_path = r"E:\Project\2025_Project\virtual_personal_assistant\app\services\test2.jpg"
json_dir = r"E:\Project\2025_Project\virtual_personal_assistant\data\text_from_image"


save_to_json(image_path, json_dir)
