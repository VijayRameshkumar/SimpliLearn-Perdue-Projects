import uuid
import json

class Product:
    def __init__(self, id, name, category_id, price):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.category_id = category_id
        self.price = float(price)

class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.products = []

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cart = {}
        self.session_id = str(uuid.uuid4())

def initialize_catalog():
    categories = [Category("c1", "Boots"), Category("c2", "Coats"), Category("c3", "Jackets"), Category("c4", "Caps")]
    products = [
        Product(None, "Product1", "c1", 50),
        Product(None, "Product2", "c2", 100),
        Product(None, "Product3", "c3", 150),
        Product(None, "Product4", "c4", 20)
    ]

    for product in products:
        add_product(categories, product)

    return categories

def add_product(categories, product):
    category = next((cat for cat in categories if cat.id == product.category_id), None)
    if category:
        category.products.append(product)
        return True
    return False

def update_product(categories, updated_product, admin_session_id):
    if admin_session_id is not None:
        category = next((cat for cat in categories if cat.id == updated_product.category_id), None)
        if category:
            index = next((idx for idx, prod in enumerate(category.products) if prod.id == updated_product.id), None)
            if index is not None:
                category.products[index] = updated_product
                return True
    return False

def delete_product(categories, product_id, admin_session_id):
    if admin_session_id is not None:
        for category in categories:
            indexes = [idx for idx, prod in enumerate(category.products) if prod.id == product_id]
            for idx in reversed(indexes):
                del category.products[idx]
                return True
    return False

def add_category(categories, new_category, admin_session_id):
    if admin_session_id is not None:
        categories.append(new_category)
        return True
    return False

def delete_category(categories, category_id, admin_session_id):
    if admin_session_id is not None:
        index = next((idx for idx, cat in enumerate(categories) if cat.id == category_id), None)
        if index is not None:
            del categories[index]
            return True
    return False

def add_user(users, username, password):
    user = User(username, password)
    users[username] = user
    return user

def authenticate_user(users, username, password):
    user = users.get(username)
    if user and user.password == password:
        return user
    return None

def save_data(users, categories):
    with open('users.json', 'w') as user_file:
        json.dump(users, user_file, default=lambda o: o.__dict__, indent=2)
    with open('categories.json', 'w') as category_file:
        json.dump(categories, category_file, default=lambda o: o.__dict__, indent=2)

def load_data():
    try:
        with open('users.json', 'r') as user_file:
            users = json.load(user_file)
    except FileNotFoundError:
        users = {}
    try:
        with open('categories.json', 'r') as category_file:
            categories = json.load(category_file)
    except FileNotFoundError:
        categories = initialize_catalog()
    return users, categories

def show_all_products(categories):
    for category in categories:
        print(f"\nCategory: {category.name}")
        for product in category.products:
            print(f"Product ID: {product.id}, Name: {product.name}, Price: {product.price}")

def show_cart(user):
    print("\nShopping Cart:")
    for product_id, quantity in user.cart.items():
        print(f"Product ID: {product_id}, Quantity: {quantity}")

def pay(user):
    print("Redirecting you to payment gateway ...")
    temp = input("Enter (1) for COD\n(2) for UPI\n(3) for Internet banking\n(4) for PayPal\n")
    print("Your payemnt successfully received")
    print("Your order is successfully placed")
    print("Happy shopping, redirecting you to the HOMEPAGE")
    

def add_to_cart(user, product_id, quantity):
    user.cart[product_id] = user.cart.get(product_id, 0) + quantity
    print(f"Item added to cart: Product ID {product_id}, Quantity {quantity}")

if __name__ == "__main__":
    users, categories = load_data()
    admin_session_id = None
    
    # Use predefined credentials for the initial login
    predefined_users = {"admin": add_user(users, "admin", "secret"), "guest": add_user(users, "guest", "notasecret")}

    print("Welcome to the Demo Marketplace")

    while True:
        if admin_session_id is None:
            print("\nHome Menu Options:")
            print("1. Login")
            print("2. Show All Products")
            print("3. Show Cart")
            print("4. Pay")
            print("5. Add To Cart")
            print("6. Exit")
            
            cmd = input("Enter option: ")
            
            if cmd == "1":
                username = input("Enter username: ")
                password = input("Enter password: ")
                user = authenticate_user(predefined_users, username, password)
                if user:
                    if username == "admin":
                        admin_session_id = user.session_id
                        print("Admin logged in.")
                    else:
                        admin_session_id = None
                        print(f"User {username} logged in.")
                else:
                    print("Authentication failed.")
                    admin_session_id = None
            elif cmd == "2":
                show_all_products(categories)
            elif cmd == "3":
                if admin_session_id is None:
                    username = input("Enter username: ")
                    user = users.get(username)
                    if user:
                        show_cart(user)
                    else:
                        print("User not found")
                else:
                    print("Admin cannot view user's cart.")
            elif cmd == "4":
                if admin_session_id is None:
                    username = input("Enter username for payment: ")
                    user = users.get(username)
                    if user:
                        pay(user)
                    else:
                        print("User not found")
                else:
                    print("Admin cannot make payments.")
            elif cmd == "5":
                if admin_session_id is None:
                    username = input("Enter username: ")
                    user = users.get(username)
                    if user:
                        product_id = input("Enter product ID to add to cart: ")
                        quantity = int(input("Enter quantity: "))
                        add_to_cart(user, product_id, quantity)
                    else:
                        print("User not found")
                else:
                    print("Admin cannot add items to the cart.")
            elif cmd == "6":
                break
            else:
                print("Invalid option. Please try again.")
        else:
            print("\nAdmin Menu Options:")
            print("1. View Products")
            print("2. View Categories")
            print("3. Add Category")
            print("4. Delete Category")
            print("5. Add Product")
            print("6. Update Product")
            print("7. Delete Product")
            print("8. Logout")
            
            cmd = input("Enter option: ")
            
            if cmd == "1":
                show_all_products(categories)
            elif cmd == "2":
                for category in categories:
                    print(f"\nCategory: {category.name}")
                    for product in category.products:
                        print(f"Product ID: {product.id}, Name: {product.name}, Price: {product.price}")
                print()
            elif cmd == "3":
                new_category = Category(str(uuid.uuid4()), input("Enter new category name: "))
                if add_category(categories, new_category, admin_session_id):
                    print("Category added successfully.")
                    save_data(users, categories)
                else:
                    print("Failed to add category.")
            elif cmd == "4":
                category_id = input("Enter category ID to delete: ")
                if delete_category(categories, category_id, admin_session_id):
                    print("Category deleted successfully.")
                    save_data(users, categories)
                else:
                    print("Failed to delete category.")
            elif cmd == "5":
                category_id = input("Enter category ID: ")
                name = input("Enter product name: ")
                price = float(input("Enter product price: "))
                product = Product(None, name, category_id, price)
                if add_product(categories, product):
                    print("Product added successfully.")
                    save_data(users, categories)
                else:
                    print("Failed to add product.")
            elif cmd == "6":
                product_id = input("Enter product ID to update: ")
                category_id = input("Enter new category ID: ")
                name = input("Enter new product name: ")
                price = float(input("Enter new product price: "))
                updated_product = Product(product_id, name, category_id, price)
                if update_product(categories, updated_product, admin_session_id):
                    print("Product updated successfully.")
                    save_data(users, categories)
                else:
                    print("Failed to update product.")
            elif cmd == "7":
                product_id = input("Enter product ID to delete: ")
                if delete_product(categories, product_id, admin_session_id):
                    print("Product deleted successfully.")
                    save_data(users, categories)
                else:
                    print("Failed to delete product.")
            elif cmd == "8":
                admin_session_id = None
                print("Admin logged out.")
            else:
                print("Invalid option. Please try again.")
