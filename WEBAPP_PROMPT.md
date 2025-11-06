# Flask Web Frontend Prompt

You are an expert Python web developer specializing in the Flask framework. My goal is to create a simple "webpage" (a web application) that acts as a frontend for my existing Python data structures project.

I already have the following Python files created and working:
- `models.py` (with `Product` and `Supplier` dataclasses)
- `product_catalog.py` (with `ProductCatalog` class using a hash table)
- `inventory.py` (with `Inventory` class using a hash table)
- `search.py` (with `ProductSearch` class using a Trie)
- `recommendations.py` (with `RecommendationEngine` class using a graph)
- `supply_chain.py` (with `SupplyChain` class using a graph)
- `data_manager.py` (with `load_data` and `save_data` functions)

Your task is to **create a new Flask application in a file named `app.py`**. This app will *replace* the CLI in `main.py`.

## Core Requirements

1. Framework: Use Flask.
2. No DB: Keep it database-less.
3. Use Existing Code: Import and use the existing classes.
   - At the start of `app.py`, call `load_data()` once and store results in globals.
   - Use `atexit.register()` to call `save_data()` when the Flask server shuts down.
4. Templates: Create HTML files in a `templates/` folder (clean HTML5).
5. Routes:
   - `/` — Homepage: list all products, search bar, and "Add Product" form (template: `index.html`).
   - `/product/<product_id>` — Product detail page; show details, stock, recommendations, and suppliers (template: `product.html`).
   - `/search` — Use `search.search_by_prefix(query)` and list matching products (template: `search_results.html`).
   - `/add_product` (POST) — Read from `request.form`; update catalog, inventory, and trie; redirect to `/`.
   - `/record_order` (POST) — Read comma-separated product IDs; call `rec_engine.record_purchase`; redirect to product page.
   - `/supply_chain` — Show all suppliers, with forms to add supplier and link supplier to product (template: `supply_chain.html`).
   - Action routes: `/add_supplier` (POST) and `/link_supplier` (POST) to handle those forms.

## Deliverables

- `app.py`
- `templates/base.html`, `templates/index.html`, `templates/product.html`, `templates/search_results.html`, `templates/supply_chain.html`
- Optional: `static/style.css`
