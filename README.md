# E-Commerce DSA Project

A simple, in-memory e-commerce management system demonstrating core data structures:

- Hash Tables: Product Catalog and Inventory (Python dictionaries)
- Trie: Product name prefix search (autocomplete)
- Graph (Adjacency List): Product co-purchase recommendations
- Bipartite Graph: Supply chain relationships (suppliers ↔ products)
- File Organization: JSON persistence for all data between runs

## Why these data structures?

- Product Catalog (Hash Table): O(1) average lookup, insert, delete by product ID.
- Inventory (Hash Table): O(1) average check/update stock by product ID.
- Product Search (Trie): O(P) prefix traversal for queries of length P; efficient autocomplete over names.
- Recommendations (Graph): Sparse adjacency list keeps storage efficient and neighbor lookups fast; weighted edges count co-purchases.
- Supply Chain (Bipartite Graph): Two hash table adjacency lists model relationships in O(1) average time per link/lookup.

## Project Structure

- `models.py`: Dataclasses `Product` and `Supplier`.
- `product_catalog.py`: `ProductCatalog` (dict-backed) with CRUD.
- `inventory.py`: `Inventory` (dict-backed) stock checks and updates.
- `search.py`: `ProductSearch` with a Trie for prefix search.
- `recommendations.py`: `RecommendationEngine` with adjacency list.
- `supply_chain.py`: `SupplyChain` bipartite graph, plus supplier registry.
- `data_manager.py`: `save_data()` and `load_data()` using JSON files.
- `main.py`: CLI wiring everything together.
- `data/`: JSON persistence folder (created on first save).

## Run

```bash
python3 main.py
```

The CLI options:

1. Add a new product (updates Catalog, Inventory, and Search Trie)
2. Search for a product (by prefix) (uses the Trie)
3. Check stock (uses Inventory hash table)
4. Record a new order (updates Recommendation graph)
5. Get recommendations for a product (uses Recommendation graph)
6. Manage Supply Chain (add/link/query suppliers)
7. Save and Exit (writes JSON files and quits)

JSON files are created under `data/`:

- `products.json`
- `inventory.json`
- `recommendations.json`
- `supply_chain.json`

## Notes for Grading

- The trie is rebuilt on load from the product catalog (derived index), demonstrating file organization while minimizing duplicated state.
- All in-memory data structures are standard Python structures (dicts/sets/lists) emphasizing algorithmic complexity.
- Code is well-commented explaining data structure choices and complexity trade-offs.
