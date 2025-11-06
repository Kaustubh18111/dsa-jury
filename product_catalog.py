"""
product_catalog.py

ProductCatalog implemented with a Python dictionary (hash table) mapping
product_id -> Product. This provides O(1) average time complexity for lookups,
insertions, and deletions by ID.
"""
from __future__ import annotations
from typing import Dict, Optional, Any
from models import Product


class ProductCatalog:
    """Catalog backed by a hash table (dict) for O(1) average operations."""

    def __init__(self) -> None:
        # Using a hash table for O(1) product lookup by ID.
        self.products: Dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        """Add a new product to the catalog. Overwrites if ID already exists."""
        self.products[product.product_id] = product

    def get_product(self, product_id: str) -> Optional[Product]:
        """Get a product by ID in O(1) average time."""
        return self.products.get(product_id)

    def update_product(self, product_id: str, **details: Any) -> bool:
        """Update fields on an existing product. Returns True if updated.

        Accepts keyword args like name=..., price=..., etc.
        """
        prod = self.products.get(product_id)
        if not prod:
            return False
        # Update only provided fields
        for key, value in details.items():
            if hasattr(prod, key):
                setattr(prod, key, value)
        return True

    def remove_product(self, product_id: str) -> bool:
        """Remove a product by ID. Returns True if removed."""
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False

    def to_dict(self) -> Dict[str, Dict]:
        """Serialize the catalog to a dict of product_id -> product_dict."""
        return {pid: p.to_dict() for pid, p in self.products.items()}

    @classmethod
    def from_dict(cls, data: Dict[str, Dict]) -> "ProductCatalog":
        """Reconstruct a catalog from a dict created by to_dict()."""
        catalog = cls()
        for pid, pdict in data.items():
            catalog.products[pid] = Product.from_dict(pdict)
        return catalog
