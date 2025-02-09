import heapq
from collections import deque
from sortedcontainers import SortedDict

class Product:
    """Class to represent a product in the inventory"""
    def __init__(self, sku, price, category, stock):
        self.sku = sku
        self.price = price
        self.category = category
        self.stock = stock
    
    def __lt__(self, other):
        """Comparator function for heap sorting by stock levels"""
        return self.stock < other.stock
    
    def __repr__(self):
        return f"Product(SKU: {self.sku}, Price: {self.price}, Category: {self.category}, Stock: {self.stock})"

class Inventory:
    """Optimized inventory management system"""
    def __init__(self):
        self.products = {}  # Hash Table for quick lookup
        self.price_tree = SortedDict()  # BST-like sorted dictionary for fast price-based queries
        self.restock_queue = deque()  # Efficient FIFO Queue
        self.priority_heap = []  # Min-Heap for low-stock prioritization
    
    # Hash Table Operations
    def add_product(self, product):
        if product.sku in self.products:
            raise ValueError("SKU already exists.")
        
        self.products[product.sku] = product
        heapq.heappush(self.priority_heap, product)  # Add to heap
        self.price_tree.setdefault(product.price, []).append(product)  # Insert into BST-like structure
    
    def get_product(self, sku):
        return self.products.get(sku, "Product not found")
    
    def remove_product(self, sku):
        if sku in self.products:
            product = self.products.pop(sku)
            self.price_tree[product.price].remove(product)
            if not self.price_tree[product.price]:
                del self.price_tree[product.price]
        else:
            print("Product not found.")
    
    # Queue Operations
    def enqueue_restock(self, product):
        self.restock_queue.append(product)
    
    def process_restock(self):
        return self.restock_queue.popleft() if self.restock_queue else "No products to restock."
    
    # Heap Operations
    def get_low_stock_product(self):
        return heapq.heappop(self.priority_heap) if self.priority_heap else "No low-stock products."
    
    # Efficient Price-Based Query
    def get_products_by_price_range(self, min_price, max_price):
        return [prod for price in self.price_tree.irange(min_price, max_price) for prod in self.price_tree[price]]
    
    # Display all products
    def display_inventory(self):
        return list(self.products.values())

# ========== TESTING THE SYSTEM ==========

def test_inventory():
    inventory = Inventory()
    
    # Adding Products
    p1 = Product("A100", 20.5, "Electronics", 15)
    p2 = Product("B200", 10.0, "Groceries", 5)
    p3 = Product("C300", 50.0, "Clothing", 2)
    p4 = Product("D400", 15.0, "Books", 20)
    
    inventory.add_product(p1)
    inventory.add_product(p2)
    inventory.add_product(p3)
    inventory.add_product(p4)
    
    print("Inventory after adding products:")
    print(inventory.display_inventory())
    
    # Get Product
    print("\nFetching product B200:")
    print(inventory.get_product("B200"))
    
    # Remove Product
    inventory.remove_product("A100")
    print("\nInventory after removing product A100:")
    print(inventory.display_inventory())
    
    # Restocking Process
    inventory.enqueue_restock(p2)
    print("\nProcessing Restock:")
    print(inventory.process_restock())
    
    # Low-stock priority
    print("\nProduct with lowest stock:")
    print(inventory.get_low_stock_product())
    
    # Get products within a price range
    print("\nProducts in price range $10 - $25:")
    print(inventory.get_products_by_price_range(10, 25))

# Run test cases
test_inventory()
