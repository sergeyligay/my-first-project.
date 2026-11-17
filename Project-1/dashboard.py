import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

def get_engine():
    """Create and return a SQLAlchemy engine from DATABASE_URL."""

    url = os.getenv("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL is missing")
    engine = create_engine(url)
    return engine
    
def store_report(engine):
    """Print counts, the catalog, and the top 3 customers."""
    with engine.connect() as conn:
        users_count = conn.execute(
            text("SELECT COUNT(*) FROM users")
        ).scalar()
        products_count = conn.execute(
            text("SELECT COUNT(*) FROM products")
        ).scalar()
        orders_count = conn.execute(
            text("SELECT COUNT(*) FROM orders")
        ).scalar()
        print("Users:", users_count)
        print("Products:", products_count)
        print("Orders:", orders_count)

        print("\nProduct catalog:")
        products = conn.execute(
            text("SELECT name, price, stock FROM products ORDER BY name")
        )
        for product in products:
            print(product)
        print("\nTop 3 customers:")
        top_customers = conn.execute(
            text("""
                SELECT users.full_name, users.email, SUM(orders.quantity) AS total_quantity
                FROM orders
                JOIN users ON orders.user_id = users.id
                GROUP BY users.id, users.full_name, users.email
                ORDER BY total_quantity DESC
                LIMIT 3
            """)
        )

        for customer in top_customers:
            print(customer)

def add_product(engine, name, category, price, stock):
    """Add a new product to the database."""
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO products (name, category, price, stock)
                VALUES (:name, :category, :price, :stock)
                RETURNING id
            """),
            {
                "name": name,
                "category": category,
                "price": price,
                "stock": stock
            }
        )        
        product_id = result.scalar_one()
    return product_id

def place_order(engine, email, product_name, quantity):
    """Place an orderand update product stock."""
    with engine.begin() as conn:
        user = conn.execute(
            text("""
                SELECT id
                FROM users
                WHERE email = :email           
            """),
            {"email": email}
        ).scalar_one_or_none()
        if user is None:
            print("User not found.")
            return
        product = conn.execute(
            text("""
                SELECT id, stock
                FROM products
                WHERE name = :product_name
            """),
            {"product_name": product_name}
        ).fetchone()
        if product is None:
            print("Product not found.")
            return
        if product.stock < quantity:
            print("Not enough stock.")
            return
        conn.execute(
            text("""
                INSERT INTO orders (user_id, product_id, quantity)
                VALUES (:user_id, :product_id, :quantity)
            """),
            {
                "user_id": user,
                "product_id": product.id,
                "quantity": quantity
            }2
        )
        conn.execute(
            text("""
                UPDATE products
                SET stock = stock - :quantity
                WHERE id = :product_id
            """),
            {
                "quantity": quantity,
                "product_id": product.id 
            }
        )
    print("Order placed successfully.")


def main():
    engine = get_engine()
    store_report(engine)
    while True:
        print("\n1. Add product")
        print("2. Place order")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            name = input("Enter product name: ")
            category = input("Enter product category: ")
            price = float(input("Enter product price: "))
            stock = int(input("Enter product stock: "))
            product_id = add_product(engine, name, category, price, stock)
            print("Product added successfully!")
            print("Product ID:", product_id)
        elif choice == '2':
            email = input("Enter customer email: ")
            product_name = input("Enter product name: ")
            quantity = int(input("Enter quantity: "))
            place_order(engine, email, product_name, quantity)
        elif choice =="3":
            print("Goodbye!")
            break
        else:
            print("Inavalid option. Try again.")

if __name__ == "__main__":
    main()