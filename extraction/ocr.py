import pytesseract
from PIL import Image


# Tell pytesseract where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_from_image(image_path: str) -> str:
    """
    Read text from a product package image using Tesseract OCR.
    """

    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    return text.strip()