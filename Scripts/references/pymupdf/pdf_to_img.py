import fitz 
import os
import pytesseract
from PIL import Image

file_name = "ET_Delhi_12_Nov_2023.pdf"
doc = fitz.open(file_name)

image_folder = 'image_folder/ET'
os.makedirs(image_folder, exist_ok=True)

def pdf_img(): 
    for page_num in range(doc.page_count):
        page = doc[page_num]
        zoom_x = 2.0  
        zoom_y = 2.0  
        mat = fitz.Matrix(zoom_x, zoom_y)
        pix = page.get_pixmap(matrix=mat)
        image_path = f"{image_folder}/page-{page_num + 1}.png"
        pix.save(image_path)

def ocr_images(image_folder):
    extracted_text = []
    
    for page_num in range(1, len(os.listdir(image_folder)) + 1):
        image_path = f"{image_folder}/page-{page_num}.png"
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        extracted_text.append(text)

    return extracted_text

text = ocr_images(image_folder)

print(text)
# pdf_img()