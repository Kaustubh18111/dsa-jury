from data_manager import load_data, save_data
from models import Product, Supplier

# Load fresh state
catalog, inventory, search, rec_engine, supply_chain = load_data()

# Add products and inventory
catalog.add_product(Product('p1', 'Apple iPhone', 'Smartphone', 999.99, 'phones'))
inventory.add_stock('p1', 10)
search.add_product_to_trie('Apple iPhone', 'p1')

catalog.add_product(Product('p2', 'Apple Watch', 'Wearable', 399.0, 'wearables'))
inventory.add_stock('p2', 5)
search.add_product_to_trie('Apple Watch', 'p2')

# Record co-purchase
rec_engine.record_purchase(['p1', 'p2'])

# Supply chain
s = Supplier('s1', 'BestSupplier', 'contact')
supply_chain.add_supplier(s)
supply_chain.link_supplier_to_product('s1', 'p1')

# Persist
save_data(catalog, inventory, rec_engine, supply_chain)

# Reload and assert
c2, i2, s2, r2, sc2 = load_data()
print('products', len(c2.products))
print('stock_p1', i2.get_stock('p1'))
print('recs_p1', r2.get_recommendations('p1'))
print('suppliers_p1', [sup.name for sup in sc2.get_suppliers_for_product('p1')])
print('search_Apple', s2.search_by_prefix('Apple'))
