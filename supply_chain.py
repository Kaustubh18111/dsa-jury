"""
supply_chain.py

SupplyChain modeled as a bipartite graph using adjacency lists:
- product_to_suppliers: product_id -> set of supplier_ids
- supplier_to_products: supplier_id -> set of product_ids

We also keep a hash table of suppliers (supplier_id -> Supplier) for O(1)
lookup of supplier details.
"""
from __future__ import annotations
from typing import Dict, Set, List
from models import Supplier


class SupplyChain:
    def __init__(self) -> None:
        # Hash tables to represent a bipartite graph between products and suppliers
        self.product_to_suppliers: Dict[str, Set[str]] = {}
        self.supplier_to_products: Dict[str, Set[str]] = {}
        self.suppliers: Dict[str, Supplier] = {}

    def add_supplier(self, supplier: Supplier) -> None:
        """Add/update supplier details in O(1) average time."""
        self.suppliers[supplier.supplier_id] = supplier
        # Ensure adjacency lists exist
        self.supplier_to_products.setdefault(supplier.supplier_id, set())

    def link_supplier_to_product(self, supplier_id: str, product_id: str) -> None:
        """Create a relationship edge between supplier and product."""
        # Using sets for O(1) average-time membership checks and to avoid duplicates
        self.product_to_suppliers.setdefault(product_id, set()).add(supplier_id)
        self.supplier_to_products.setdefault(supplier_id, set()).add(product_id)

    def get_suppliers_for_product(self, product_id: str) -> List[Supplier]:
        """Return Supplier objects providing a given product."""
        ids = self.product_to_suppliers.get(product_id, set())
        # Only return suppliers that exist in the supplier table
        return [self.suppliers[sid] for sid in ids if sid in self.suppliers]

    def get_products_from_supplier(self, supplier_id: str) -> List[str]:
        """Return product_ids that a supplier provides."""
        return sorted(self.supplier_to_products.get(supplier_id, set()))

    def to_dict(self) -> Dict:
        """Serialize supply chain to a JSON-friendly dict."""
        return {
            "suppliers": {sid: s.to_dict() for sid, s in self.suppliers.items()},
            "product_to_suppliers": {pid: sorted(list(sids)) for pid, sids in self.product_to_suppliers.items()},
            "supplier_to_products": {sid: sorted(list(pids)) for sid, pids in self.supplier_to_products.items()},
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "SupplyChain":
        sc = cls()
        for sid, sdict in data.get("suppliers", {}).items():
            sc.suppliers[sid] = Supplier.from_dict(sdict)
        for pid, sids in data.get("product_to_suppliers", {}).items():
            sc.product_to_suppliers[pid] = set(sids)
        for sid, pids in data.get("supplier_to_products", {}).items():
            sc.supplier_to_products[sid] = set(pids)
        return sc
