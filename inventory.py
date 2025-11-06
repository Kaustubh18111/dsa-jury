"""
inventory.py

Inventory implemented with a Python dictionary (hash table) mapping
product_id -> stock_quantity. This gives O(1) average time for checking
and updating stock.
"""
from __future__ import annotations
from typing import Dict


class Inventory:
    """Inventory backed by a hash table (dict) for O(1) average ops."""

    def __init__(self) -> None:
        # Using a hash table for fast stock lookups by product_id.
        self.stock: Dict[str, int] = {}

    def get_stock(self, product_id: str) -> int:
        """Return current stock for a product (0 if unknown)."""
        return int(self.stock.get(product_id, 0))

    def add_stock(self, product_id: str, quantity: int) -> None:
        """Increase stock by quantity (must be non-negative)."""
        if quantity < 0:
            raise ValueError("quantity must be non-negative")
        self.stock[product_id] = self.get_stock(product_id) + int(quantity)

    def remove_stock(self, product_id: str, quantity: int) -> bool:
        """Decrease stock by quantity if available. Returns True if successful."""
        if quantity < 0:
            raise ValueError("quantity must be non-negative")
        current = self.get_stock(product_id)
        if quantity > current:
            return False
        self.stock[product_id] = current - int(quantity)
        return True

    def to_dict(self) -> Dict[str, int]:
        """Serialize inventory as product_id -> quantity mapping."""
        return {pid: int(qty) for pid, qty in self.stock.items()}

    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> "Inventory":
        inv = cls()
        for pid, qty in data.items():
            inv.stock[pid] = int(qty)
        return inv
