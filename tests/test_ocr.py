from extraction.ocr import extract_text_from_image

text = extract_text_from_image("assets/test_product.png")

print("===== OCR OUTPUT =====")
print(text)
print("======================")