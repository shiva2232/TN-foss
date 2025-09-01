import pytesseract
from PIL import Image

def readocr(url):
    img = Image.open(url)
    text = pytesseract.image_to_string(img)
    # print(text)
    return text
