"""
Script to create a test SQLite database with sample data.
Run this to set up a test environment for the NL2SQL package.
"""

import sqlite3
import random
from datetime import datetime, timedelta

def create_test_database():
    """Create a test SQLite database with sample tables and data."""
    
    # Connect to SQLite database (creates file if doesn't exist)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    # Drop tables if they exist (for clean setup)
    cursor.execute('DROP TABLE IF EXISTS order_items')
    cursor.execute('DROP TABLE IF EXISTS orders')
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('DROP TABLE IF EXISTS customers')
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            city TEXT,
            state TEXT,
            signup_date DATE
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            price DECIMAL(10,2),
            stock_quantity INTEGER
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date DATE,
            status TEXT,
            total_amount DECIMAL(10,2),
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
    ''')
    
    # Create order_items table
    cursor.execute('''
        CREATE TABLE order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            unit_price DECIMAL(10,2),
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    ''')
    
    # Insert sample customers
    customers_data = [
        ('John', 'Doe', 'john.doe@email.com', 'New York', 'NY', '2023-01-15'),
        ('Jane', 'Smith', 'jane.smith@email.com', 'Los Angeles', 'CA', '2023-02-20'),
        ('Bob', 'Johnson', 'bob.johnson@email.com', 'Chicago', 'IL', '2023-03-10'),
        ('Alice', 'Williams', 'alice.williams@email.com', 'Houston', 'TX', '2023-01-25'),
        ('Charlie', 'Brown', 'charlie.brown@email.com', 'Phoenix', 'AZ', '2023-04-05'),
        ('Diana', 'Davis', 'diana.davis@email.com', 'Philadelphia', 'PA', '2023-02-14'),
        ('Eve', 'Miller', 'eve.miller@email.com', 'San Antonio', 'TX', '2023-03-20'),
        ('Frank', 'Wilson', 'frank.wilson@email.com', 'San Diego', 'CA', '2023-01-30'),
        ('Grace', 'Moore', 'grace.moore@email.com', 'Dallas', 'TX', '2023-04-12'),
        ('Henry', 'Taylor', 'henry.taylor@email.com', 'San Jose', 'CA', '2023-02-28')
    ]
    
    cursor.executemany('''
        INSERT INTO customers (first_name, last_name, email, city, state, signup_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', customers_data)
    
    # Insert sample products
    products_data = [
        ('Laptop Pro', 'Electronics', 1299.99, 50),
        ('Wireless Mouse', 'Electronics', 29.99, 200),
        ('Coffee Maker', 'Appliances', 89.99, 75),
        ('Running Shoes', 'Footwear', 129.99, 100),
        ('Bluetooth Headphones', 'Electronics', 199.99, 80),
        ('Office Chair', 'Furniture', 299.99, 30),
        ('Water Bottle', 'Sports', 24.99, 150),
        ('Smartphone', 'Electronics', 799.99, 60),
        ('Desk Lamp', 'Furniture', 49.99, 90),
        ('Fitness Tracker', 'Electronics', 149.99, 120)
    ]
    
    cursor.executemany('''
        INSERT INTO products (product_name, category, price, stock_quantity)
        VALUES (?, ?, ?, ?)
    ''', products_data)
    
    # Insert sample orders
    base_date = datetime(2024, 1, 1)
    orders_data = []
    order_items_data = []
    
    for i in range(1, 51):  # 50 orders
        customer_id = random.randint(1, 10)
        order_date = base_date + timedelta(days=random.randint(0, 120))
        status = random.choice(['completed', 'pending', 'shipped', 'cancelled'])
        
        # Generate 1-4 items per order
        num_items = random.randint(1, 4)
        total_amount = 0
        
        for j in range(num_items):
            product_id = random.randint(1, 10)
            quantity = random.randint(1, 3)
            
            # Get product price (we'll calculate this)
            cursor.execute('SELECT price FROM products WHERE product_id = ?', (product_id,))
            unit_price = cursor.fetchone()[0]
            
            total_amount += unit_price * quantity
            
            order_items_data.append((i, product_id, quantity, unit_price))
        
        orders_data.append((customer_id, order_date.strftime('%Y-%m-%d'), status, total_amount))
    
    cursor.executemany('''
        INSERT INTO orders (customer_id, order_date, status, total_amount)
        VALUES (?, ?, ?, ?)
    ''', orders_data)
    
    cursor.executemany('''
        INSERT INTO order_items (order_id, product_id, quantity, unit_price)
        VALUES (?, ?, ?, ?)
    ''', order_items_data)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("✅ Test database 'test.db' created successfully!")
    print("\nTables created:")
    print("- customers (10 records)")
    print("- products (10 records)")  
    print("- orders (50 records)")
    print("- order_items (multiple records)")
    
    print("\nYou can now test the NL2SQL package with questions like:")
    print("- 'Show me all customers from Texas'")
    print("- 'What are the top 5 products by price?'")
    print("- 'How many orders were completed?'")
    print("- 'What's the total revenue by month?'")

if __name__ == "__main__":
    create_test_database()
