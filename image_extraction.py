import fitz  # PyMuPDF
import io
from PIL import Image
from pypdf import PdfReader
from PyPDF2 import PdfReader
import os
from pdf2image import convert_from_path


file = "/Users/balakrishnareddyragannagari/Desktop/Sat_questions/Question_generator/docs/SAT_math_problem_set_12_circles-quadrilaterals and volume.pdf"


pdf_path = file

# Convert all pages to images
images = convert_from_path(pdf_path)

os.makedirs('pdf_images',exist_ok=True)
# Save each page as a separate image
for i, page in enumerate(images):
    page.save(f'pdf_images/page_{i+1}.png', 'PNG')


                      






