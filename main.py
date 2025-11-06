"""
main.py

Simple CLI application wiring together:
- ProductCatalog (hash table)
- Inventory (hash table)
- ProductSearch (Trie/prefix tree)
- RecommendationEngine (graph as adjacency list)
- SupplyChain (bipartite graph)

Data is persisted to JSON files via data_manager.save_data/load_data.
"""
from __future__ import annotations
from typing import List

from models import Product, Supplier
from product_catalog import ProductCatalog
from inventory import Inventory
from search import ProductSearch
from recommendations import RecommendationEngine
from supply_chain import SupplyChain
from data_manager import load_data, save_data


def input_nonempty(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("Value cannot be empty.")


def input_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Please enter a valid number.")


def input_int(prompt: str, min_value: int | None = None) -> int:
    while True:
        try:
            v = int(input(prompt).strip())
            if min_value is not None and v < min_value:
                print(f"Please enter a number >= {min_value}.")
                continue
            return v
        except ValueError:
            print("Please enter a valid integer.")


def add_product_flow(catalog: ProductCatalog, inventory: Inventory, search: ProductSearch) -> None:
    print("\n-- Add New Product --")
    product_id = input_nonempty("Product ID: ")
    name = input_nonempty("Name: ")
    description = input("Description: ")
    price = input_float("Price: ")
    category = input("Category (optional): ") or "uncategorized"
    initial_stock = input_int("Initial stock quantity (>=0): ", min_value=0)

    product = Product(product_id=product_id, name=name, description=description, price=price, category=category)
    catalog.add_product(product)
    inventory.add_stock(product_id, initial_stock)
    search.add_product_to_trie(name, product_id)

    print(f"Product '{name}' added with ID {product_id} and stock {initial_stock}.")


def search_product_flow(catalog: ProductCatalog, search: ProductSearch) -> None:
    print("\n-- Search Products (Prefix) --")
    prefix = input_nonempty("Enter prefix: ")
    matches = search.search_by_prefix(prefix)
    if not matches:
        print("No products found for that prefix.")
        return
    print(f"Found {len(matches)} product(s):")
    for pid in matches:
        p = catalog.get_product(pid)
        if p:
            print(f"- {p.product_id} | {p.name} | ${p.price:.2f} | {p.category}")
        else:
            print(f"- {pid} (details not found)")


def check_stock_flow(inventory: Inventory) -> None:
    print("\n-- Check Stock --")
    product_id = input_nonempty("Product ID: ")
    print(f"Stock for {product_id}: {inventory.get_stock(product_id)}")


def record_order_flow(rec_engine: RecommendationEngine) -> None:
    print("\n-- Record Order --")
    raw = input_nonempty("Enter product IDs in order, comma-separated: ")
    product_ids = [x.strip() for x in raw.split(",") if x.strip()]
    if len(product_ids) < 2:
        print("Need at least 2 products to record a co-purchase.")
        return
    rec_engine.record_purchase(product_ids)
    print("Order recorded.")


def recommendations_flow(catalog: ProductCatalog, rec_engine: RecommendationEngine) -> None:
    print("\n-- Get Recommendations --")
    product_id = input_nonempty("Product ID: ")
    k = input_int("How many recommendations? (default 5, enter 0 to cancel): ")
    if k == 0:
        return
    recs = rec_engine.get_recommendations(product_id, k)
    if not recs:
        print("No recommendations yet for this product.")
        return
    print("Top recommendations:")
    for pid in recs:
        p = catalog.get_product(pid)
        if p:
            print(f"- {p.product_id} | {p.name} | ${p.price:.2f}")
        else:
            print(f"- {pid}")


def supply_chain_menu(catalog: ProductCatalog, supply_chain: SupplyChain) -> None:
    while True:
        print("\n-- Supply Chain --")
        print("1. Add Supplier")
        print("2. Link Supplier to Product")
        print("3. Get Suppliers for Product")
        print("4. Get Products from Supplier")
        print("5. Back")
        choice = input_nonempty("Choose an option: ")
        if choice == "1":
            sid = input_nonempty("Supplier ID: ")
            name = input_nonempty("Supplier Name: ")
            contact = input("Contact Info: ")
            supply_chain.add_supplier(Supplier(supplier_id=sid, name=name, contact_info=contact))
            print("Supplier added.")
        elif choice == "2":
            sid = input_nonempty("Supplier ID: ")
            pid = input_nonempty("Product ID: ")
            if not catalog.get_product(pid):
                print("Warning: Product ID not found in catalog. You can still link it, but consider adding the product first.")
            supply_chain.link_supplier_to_product(sid, pid)
            print("Link created.")
        elif choice == "3":
            pid = input_nonempty("Product ID: ")
            sups = supply_chain.get_suppliers_for_product(pid)
            if not sups:
                print("No suppliers found.")
            else:
                print(f"Suppliers for {pid}:")
                for s in sups:
                    print(f"- {s.supplier_id} | {s.name} | {s.contact_info}")
        elif choice == "4":
            sid = input_nonempty("Supplier ID: ")
            products = supply_chain.get_products_from_supplier(sid)
            if not products:
                print("No products found.")
            else:
                print(f"Products from {sid}: {', '.join(products)}")
        elif choice == "5":
            return
        else:
            print("Invalid choice.")


def main() -> None:
    print("Loading data...")
    catalog, inventory, search, rec_engine, supply_chain = load_data()

    while True:
        print("\n==== E-Commerce DSA CLI ====")
        print("1. Add a new product")
        print("2. Search for a product (by prefix)")
        print("3. Check stock")
        print("4. Record a new order")
        print("5. Get recommendations for a product")
        print("6. Manage Supply Chain")
        print("7. Save and Exit")
        choice = input_nonempty("Choose an option: ")

        if choice == "1":
            add_product_flow(catalog, inventory, search)
        elif choice == "2":
            search_product_flow(catalog, search)
        elif choice == "3":
            check_stock_flow(inventory)
        elif choice == "4":
            record_order_flow(rec_engine)
        elif choice == "5":
            recommendations_flow(catalog, rec_engine)
        elif choice == "6":
            supply_chain_menu(catalog, supply_chain)
        elif choice == "7":
            print("Saving data...")
            save_data(catalog, inventory, rec_engine, supply_chain)
            print("Saved. Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-7.")


if __name__ == "__main__":
    main()
