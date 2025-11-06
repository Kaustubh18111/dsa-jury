# Project To-Do: Flask Web Frontend

## Milestone 1: Setup

- [ ] Install Flask: `pip install Flask`
- [x] Create a new file: `app.py`.
- [x] Create a folder named `templates/`.
- [x] Create a folder named `static/`.
- [x] (Optional) Create `static/style.css` for basic styling.

## Milestone 2: `app.py` (Flask Server)

- [x] Import Flask, `atexit`, and all project classes (`ProductCatalog`, `Inventory`, etc.) and data functions (`load_data`, `save_data`).
- [x] Initialize the Flask app: `app = Flask(__name__)`.
- [x] Load all data once at the top: `catalog, inventory, search, ... = load_data()`.
- [x] Register the save function to run on exit: `atexit.register(save_data, catalog, inventory, ...)`.
- [x] Implement the `@app.route('/')` to show all products (render `index.html`).
- [x] Implement the `@app.route('/product/<product_id>')` to show product details (render `product.html`).
- [x] Implement the `@app.route('/search')` to show search results (render `search_results.html`).
- [x] Implement the `@app.route('/add_product', methods=['POST'])` to handle the new product form).
- [x] Implement the `@app.route('/record_order', methods=['POST'])` to update the recommendation graph).
- [x] Implement the `@app.route('/supply_chain')` to show the supplier page (render `supply_chain.html`).
- [x] Implement the `@app.route('/add_supplier', methods=['POST'])` action.
- [x] Implement the `@app.route('/link_supplier', methods=['POST'])` action.
- [x] Add the `if __name__ == "__main__":` block to run the app.

## Milestone 3: HTML Templates (in `templates/` folder)

- [x] `base.html`: HTML5 layout, navbar, CSS, block content.
- [x] `index.html`: extends base; add product form and product list.
- [x] `product.html`: extends base; details, stock, suppliers, recommendations, simulate order form.
- [x] `search_results.html`: extends base; show query and results.
- [x] `supply_chain.html`: extends base; add supplier form, link form, and suppliers list.

## Milestone 4: Styling (Optional)

- [x] Add simple CSS to `static/style.css`.
