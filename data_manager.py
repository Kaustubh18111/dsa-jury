"""
data_manager.py

JSON-based persistence layer for the in-memory data structures. This simulates
simple file organization by saving/loading dictionaries and graphs to/from JSON
files between runs.

Files:
- data/products.json
- data/inventory.json
- data/recommendations.json
- data/supply_chain.json
"""
from __future__ import annotations
import json
import os
from typing import Tuple

from product_catalog import ProductCatalog
from inventory import Inventory
from search import ProductSearch
from recommendations import RecommendationEngine
from supply_chain import SupplyChain


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")
RECOMMENDATIONS_FILE = os.path.join(DATA_DIR, "recommendations.json")
SUPPLY_CHAIN_FILE = os.path.join(DATA_DIR, "supply_chain.json")


def _ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def save_data(
    catalog: ProductCatalog,
    inventory: Inventory,
    rec_engine: RecommendationEngine,
    supply_chain: SupplyChain,
) -> None:
    """Serialize all in-memory structures to JSON files.

    We keep the trie out of persistence and rebuild it on load from the catalog
    (product names), since the trie is a derived index over product names.
    """
    _ensure_data_dir()

    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog.to_dict(), f, indent=2, ensure_ascii=False)

    with open(INVENTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(inventory.to_dict(), f, indent=2, ensure_ascii=False)

    with open(RECOMMENDATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(rec_engine.to_dict(), f, indent=2, ensure_ascii=False)

    with open(SUPPLY_CHAIN_FILE, "w", encoding="utf-8") as f:
        json.dump(supply_chain.to_dict(), f, indent=2, ensure_ascii=False)


def _load_json(path: str, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def load_data() -> Tuple[ProductCatalog, Inventory, ProductSearch, RecommendationEngine, SupplyChain]:
    """Load JSON files (if present) and reconstruct in-memory structures.

    Returns instances of ProductCatalog, Inventory, ProductSearch, RecommendationEngine, SupplyChain.
    """
    # Load raw JSON data (or defaults)
    products_data = _load_json(PRODUCTS_FILE, {})
    inventory_data = _load_json(INVENTORY_FILE, {})
    rec_data = _load_json(RECOMMENDATIONS_FILE, {})
    supply_data = _load_json(SUPPLY_CHAIN_FILE, {"suppliers": {}, "product_to_suppliers": {}, "supplier_to_products": {}})

    # Rebuild in-memory objects
    catalog = ProductCatalog.from_dict(products_data)
    inventory = Inventory.from_dict(inventory_data)
    rec_engine = RecommendationEngine.from_dict(rec_data)
    supply_chain = SupplyChain.from_dict(supply_data)

    # Rebuild derived trie index from the catalog
    search = ProductSearch()
    for pid, product in catalog.products.items():
        search.add_product_to_trie(product.name, pid)

    return catalog, inventory, search, rec_engine, supply_chain
