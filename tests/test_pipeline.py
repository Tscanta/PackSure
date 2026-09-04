import json

from extraction.ocr import extract_text_from_image
from extraction.normalizer import normalize_text
from extraction.parser import extract_product_data
from extraction.nutrition import extract_nutrition_data


# ============================================================
# IMAGE
# ============================================================

image_path = "assets/test_product.png"


# ============================================================
# OCR
# ============================================================

raw_ocr = extract_text_from_image(image_path)

print("===== RAW OCR OUTPUT =====")
print(raw_ocr)


# ============================================================
# NORMALIZATION
# ============================================================

normalized_text = normalize_text(raw_ocr)

print("\n===== NORMALIZED OCR OUTPUT =====")
print(normalized_text)


# ============================================================
# PRODUCT PARSER
# ============================================================

product = extract_product_data(normalized_text)


# ============================================================
# NUTRITION PARSER
# ============================================================

nutrition = extract_nutrition_data(normalized_text)

product.nutrition = nutrition


# ============================================================
# PRODUCT DATA
# ============================================================

print("\n===== PRODUCT DATA =====")

print("Product Name       :", product.product_name)
print("Product Category   :", product.product_category)
print("MRP                :", product.mrp)
print("Net Quantity       :", product.net_quantity)
print("Manufacturer       :", product.manufacturer)
print("Manufacturer Addr. :", product.manufacturer_address)
print("Importer/Marketer  :", product.importer)
print("Importer Address   :", product.importer_address)
print("Country of Origin  :", product.country_of_origin)
print("Ingredients        :", product.ingredients)
print("Allergens          :", product.allergens)
print("Manufacturing Date :", product.manufacturing_date)
print("Best Before        :", product.best_before)
print("FSSAI License      :", product.fssai_license)
print("Customer Care      :", product.customer_care)


# ============================================================
# NUTRITION DATA
# ============================================================

print("\n===== NUTRITION DATA =====")

print("Serving Size       :", nutrition.serving_size)
print("Calories           :", nutrition.calories)
print("Total Fat          :", nutrition.total_fat)
print("Saturated Fat      :", nutrition.saturated_fat)
print("Trans Fat          :", nutrition.trans_fat)
print("Cholesterol        :", nutrition.cholesterol)
print("Sodium             :", nutrition.sodium)
print("Potassium          :", nutrition.potassium)
print("Total Carbohydrate :", nutrition.total_carbohydrate)
print("Dietary Fiber      :", nutrition.dietary_fiber)
print("Sugars             :", nutrition.sugars)
print("Protein            :", nutrition.protein)
print("Vitamin A          :", nutrition.vitamin_a)
print("Vitamin C          :", nutrition.vitamin_c)
print("Vitamin D          :", nutrition.vitamin_d)
print("Calcium            :", nutrition.calcium)
print("Iron               :", nutrition.iron)
print("Magnesium          :", nutrition.magnesium)
print("Phosphorus         :", nutrition.phosphorus)
print("Niacin             :", nutrition.niacin)
print("Vitamin B6         :", nutrition.vitamin_b6)


# ============================================================
# CONVERT PRODUCT TO DICTIONARY
# ============================================================

product_data = product.model_dump()


# ============================================================
# REMOVE INTERNAL FIELD
# ============================================================

# raw_text is already stored separately as raw_ocr
product_data.pop("raw_text", None)


# ============================================================
# FINAL JSON
# ============================================================

output = {
    "raw_ocr": raw_ocr,
    "product": product_data
}


# ============================================================
# PRINT FINAL JSON
# ============================================================

print("\n===== FINAL JSON =====")

print(
    json.dumps(
        output,
        indent=2,
        ensure_ascii=False
    )
)