from backend.inspection.validator import (
    check_product_name,
    check_mrp,
    check_net_quantity,
    check_manufacturer_address,
    check_customer_care,
    check_date,
)

VALIDATOR_REGISTRY = {
    "TEXT_EXISTS": check_product_name,
    "CURRENCY": check_mrp,
    "QUANTITY": check_net_quantity,
    "ADDRESS": check_manufacturer_address,
    "PHONE": check_customer_care,
    "DATE": check_date,
}


from backend.inspection.validator import (
    check_product_name,
    check_mrp,
    check_net_quantity,
    check_manufacturer_address,
    check_customer_care,
)

VALIDATOR_REGISTRY = {
    "TEXT_EXISTS": check_product_name,
    "CURRENCY": check_mrp,
    "QUANTITY": check_net_quantity,
    "ADDRESS": check_manufacturer_address,
    "PHONE": check_customer_care,
}

from backend.inspection.validator import (
    check_mrp,
    check_net_quantity,
    check_manufacturer_address,
    check_customer_care,
)

VALIDATOR_REGISTRY = {
    "CURRENCY": check_mrp,
    "QUANTITY": check_net_quantity,
    "ADDRESS": check_manufacturer_address,
    "PHONE": check_customer_care,
}