import threading


# -----------------------------
# Product Class
# -----------------------------
class Product:
    def __init__(self, pid, name, stock):
        self.pid = pid
        self.name = name
        self.stock = stock
        self.lock = threading.Lock()   # for safe concurrent access


# -----------------------------
# Inventory Class
# -----------------------------
class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, pid, name, stock):
        if pid in self.products:
            print("Product already exists")
        else:
            self.products[pid] = Product(pid, name, stock)
            print("Product added successfully")

    def show_products(self):
        print("\nAvailable Products:")
        for product in self.products.values():
            print(f"{product.pid} | {product.name} | Stock: {product.stock}")


# -----------------------------
# Cart Class
# -----------------------------
class Cart:
    def __init__(self):
        self.items = {}

    def add_to_cart(self, inventory, pid, quantity):
        if pid not in inventory.products:
            print("Invalid product")
            return

        product = inventory.products[pid]

        # Lock ensures only one thread updates stock at a time
        with product.lock:
            if product.stock >= quantity:
                product.stock -= quantity
                self.items[pid] = self.items.get(pid, 0) + quantity
                print("Item added to cart")
            else:
                print("Not enough stock")

    def show_cart(self):
        print("Cart Items:", self.items)


# -----------------------------
# User Class
# -----------------------------
class User:
    def __init__(self, name):
        self.name = name
        self.cart = Cart()


# -----------------------------
# Thread Function
# -----------------------------
def buy_product(user, inventory, pid, quantity):
    user.cart.add_to_cart(inventory, pid, quantity)
    print(f"{user.name} finished operation")


# -----------------------------
# Main Program
# -----------------------------
inventory = Inventory()
users = {}

while True:
    print("\nMenu:")
    print("1. Add Product")
    print("2. Show Products")
    print("3. Create User")
    print("4. Add to Cart")
    print("5. Show Cart")
    print("6. Test Concurrency")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        pid = input("Enter Product ID: ")
        name = input("Enter Product Name: ")
        stock = int(input("Enter Stock: "))
        inventory.add_product(pid, name, stock)

    elif choice == "2":
        inventory.show_products()

    elif choice == "3":
        username = input("Enter username: ")
        users[username] = User(username)
        print("User created successfully")

    elif choice == "4":
        username = input("Enter username: ")
        pid = input("Enter Product ID: ")
        qty = int(input("Enter quantity: "))

        if username in users:
            users[username].cart.add_to_cart(inventory, pid, qty)
        else:
            print("User not found")

    elif choice == "5":
        username = input("Enter username: ")

        if username in users:
            users[username].cart.show_cart()
        else:
            print("User not found")

    elif choice == "6":
        pid = input("Enter Product ID: ")
        qty = int(input("Enter quantity: "))

        user1 = User("UserA")
        user2 = User("UserB")

        t1 = threading.Thread(target=buy_product, args=(user1, inventory, pid, qty))
        t2 = threading.Thread(target=buy_product, args=(user2, inventory, pid, qty))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        print("\nFinal Product Stock:")
        inventory.show_products()

    elif choice == "7":
        print("Exiting program...")
        break

    else:
        print("Invalid choice")
