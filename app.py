"""
app.py

Flask web frontend for the in-memory e-commerce DSA backend.
- Uses existing classes: ProductCatalog, Inventory, ProductSearch, RecommendationEngine, SupplyChain
- Persists via JSON using data_manager.load_data/save_data (no DB)
- Replaces the CLI in main.py with a simple web UI
"""
from __future__ import annotations
import atexit
from typing import List

from flask import Flask, render_template, request, redirect, url_for, abort

from models import Product, Supplier
from product_catalog import ProductCatalog
from inventory import Inventory
from search import ProductSearch
from recommendations import RecommendationEngine
from supply_chain import SupplyChain
from data_manager import load_data, save_data


app = Flask(__name__)

# Load all data once at startup
catalog: ProductCatalog
inventory: Inventory
search: ProductSearch
rec_engine: RecommendationEngine
supply_chain: SupplyChain
catalog, inventory, search, rec_engine, supply_chain = load_data()

# Ensure data is saved on server shutdown
atexit.register(save_data, catalog, inventory, rec_engine, supply_chain)


@app.route("/")
def index():
    # Show all products and provide add/search forms
    products = sorted(catalog.products.values(), key=lambda p: p.name.lower())
    return render_template("index.html", products=products)


@app.route("/product/<product_id>")
def product_detail(product_id: str):
    product = catalog.get_product(product_id)
    if not product:
        abort(404)
    stock = inventory.get_stock(product_id)
    rec_ids = rec_engine.get_recommendations(product_id, 5)
    rec_products = [catalog.get_product(pid) for pid in rec_ids if catalog.get_product(pid)]
    suppliers = supply_chain.get_suppliers_for_product(product_id)
    return render_template(
        "product.html",
        product=product,
        stock=stock,
        recommendations=rec_products,
        suppliers=suppliers,
    )


@app.route("/search")
def search_results():
    query = (request.args.get("query") or "").strip()
    results: List[Product] = []
    if query:
        ids = search.search_by_prefix(query)
        for pid in ids:
            p = catalog.get_product(pid)
            if p:
                results.append(p)
    return render_template("search_results.html", query=query, results=results)


@app.route("/add_product", methods=["POST"])
def add_product():
    product_id = (request.form.get("product_id") or "").strip()
    name = (request.form.get("name") or "").strip()
    description = (request.form.get("description") or "").strip()
    category = (request.form.get("category") or "uncategorized").strip()
    price_raw = (request.form.get("price") or "0").strip()
    stock_raw = (request.form.get("initial_stock") or "0").strip()

    if not product_id or not name:
        return redirect(url_for("index"))

    try:
        price = float(price_raw)
    except ValueError:
        price = 0.0
    try:
        initial_stock = max(0, int(stock_raw))
    except ValueError:
        initial_stock = 0

    product = Product(product_id=product_id, name=name, description=description, price=price, category=category)
    catalog.add_product(product)
    inventory.add_stock(product_id, initial_stock)
    search.add_product_to_trie(name, product_id)

    return redirect(url_for("index"))


@app.route("/record_order", methods=["POST"])
def record_order():
    order_raw = (request.form.get("order_ids") or "").strip()
    redirect_pid = (request.form.get("redirect_pid") or "").strip()
    ids = [x.strip() for x in order_raw.split(",") if x.strip()]
    if len(ids) >= 2:
        rec_engine.record_purchase(ids)
    if redirect_pid:
        return redirect(url_for("product_detail", product_id=redirect_pid))
    return redirect(url_for("index"))


@app.route("/supply_chain")
def supply_chain_page():
    suppliers = sorted(supply_chain.suppliers.values(), key=lambda s: s.name.lower())
    return render_template("supply_chain.html", suppliers=suppliers)


@app.route("/add_supplier", methods=["POST"])
def add_supplier():
    supplier_id = (request.form.get("supplier_id") or "").strip()
    name = (request.form.get("name") or "").strip()
    contact_info = (request.form.get("contact_info") or "").strip()
    if supplier_id and name:
        supply_chain.add_supplier(Supplier(supplier_id=supplier_id, name=name, contact_info=contact_info))
    return redirect(url_for("supply_chain_page"))


@app.route("/link_supplier", methods=["POST"])
def link_supplier():
    supplier_id = (request.form.get("supplier_id") or "").strip()
    product_id = (request.form.get("product_id") or "").strip()
    if supplier_id and product_id:
        supply_chain.link_supplier_to_product(supplier_id, product_id)
    return redirect(url_for("supply_chain_page"))


if __name__ == "__main__":
    # Run the Flask development server
    app.run(host="0.0.0.0", port=5000, debug=True)
