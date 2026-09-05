"""Domain representation of the information supplied to the rule engine."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Product:
    """A permissive internal product model.

    The public request contract remains :class:`schemas.product.ProductInput`.
    ``attributes`` keeps extraction-specific values without forcing the database
    product table to mirror every OCR field.
    """

    product_name: str | None = None
    brand: str | None = None
    product_category: str | None = None
    mrp: Any = None
    net_quantity: Any = None
    manufacturer: str | None = None
    manufacturer_address: str | None = None
    importer: str | None = None
    importer_address: str | None = None
    country_of_origin: str | None = None
    customer_care: str | None = None
    manufacturing_date: Any = None
    expiry_date: Any = None
    raw_text: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_input(cls, value: Any) -> "Product":
        """Adapt a Pydantic schema, mapping, or compatible object to a domain product."""
        if hasattr(value, "model_dump"):
            data = value.model_dump()
        elif isinstance(value, dict):
            data = dict(value)
        else:
            data = vars(value)
        known = {name: data.pop(name, None) for name in cls.__dataclass_fields__ if name != "attributes"}
        return cls(**known, attributes=data)

    def get(self, name: str, default: Any = None) -> Any:
        return getattr(self, name, self.attributes.get(name, default))
