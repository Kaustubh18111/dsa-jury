"""
models.py

Core data models for the e-commerce DSA project.

We use @dataclass for lightweight, readable model classes, and provide
(to_dict/from_dict) helpers to serialize/deserialize to JSON-friendly dicts.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class Product:
    """Represents a product in the catalog.

    Fields kept intentionally simple for DSA-focused project.
    """
    product_id: str
    name: str
    description: str
    price: float
    category: str

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a JSON-friendly dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Product":
        """Construct a Product from a dictionary, with basic type coercion."""
        return cls(
            product_id=str(data["product_id"]),
            name=str(data["name"]),
            description=str(data.get("description", "")),
            price=float(data["price"]),
            category=str(data.get("category", "uncategorized")),
        )


@dataclass
class Supplier:
    """Represents a supplier in the supply chain graph."""
    supplier_id: str
    name: str
    contact_info: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Supplier":
        return cls(
            supplier_id=str(data["supplier_id"]),
            name=str(data["name"]),
            contact_info=str(data.get("contact_info", "")),
        )
