import tomli
from datetime import datetime
import pathlib
import random
import psycopg2
import pytz


data_path = pathlib.Path(__file__).parent /"database.toml"
data = tomli.loads(data_path.read_text())
products = data['products']['product']
customers = data['customers']['customer']
local_timezone = pytz.timezone("Africa/Nairobi")

def create_transactions_table(table_name, columns):
    with psycopg2.connect(host="localhost", port=5432, database="demo_db", user="user", password="user_password") as conn:
        with conn.cursor() as cur:
            cur.execute(f"create table if not exists {table_name}({','.join(columns)})")

def load_transactions_table(table_name, orders):
    with psycopg2.connect(host="localhost", port=5432, database="demo_db", user="user", password="user_password") as conn:
        with conn.cursor() as cur:
            cur.executemany(f"insert into {table_name} values({','.join(['%s'] * len(orders[0]))})", orders)
            conn.commit()

def get_last_invoice_number():
    with psycopg2.connect(host="localhost", port=5432, database="demo_db", user="user", password="user_password") as conn:
        with conn.cursor() as cur:
            cur.execute("select count(distinct invoice_number) from transactions")
            result = cur.fetchone()[0]
            return result if result else 0

def generate_new_invoice_number():
    last_invoice_number = get_last_invoice_number()
    last_invoice_number += 1
    invoice_number = f"INV{last_invoice_number:0005d}"
    return invoice_number

def generate_invoice_products():
    customer = random.choice(customers)
    num_products = random.randint(1, len(products))
    selected_products = random.sample(products, num_products)

    order_data = []
    invoice_number = generate_new_invoice_number()

    for product in selected_products:
        quantity = random.randint(1, 5)
        price = product["price"]
        weight = product["weight"]
        total_price = quantity * price
        total_weight = quantity * weight
        current_datetime = datetime.now(local_timezone)
        order_data.append((
            customer["c_name"],
            customer["crm"],
            customer["credit_limit"],
            customer["location"],
            invoice_number,
            current_datetime.date(),
            current_datetime.time(),
            product["p_name"],
            product["p_code"],
            quantity,
            weight,
            total_weight,
            price,
            total_price,
        ))
    return order_data

def load_to_database():
    num_orders = 1
    create_transactions_table("transactions", 
                        ["customer_name VARCHAR(255)",
                        "crm VARCHAR(255)",
                        "credit_limit FLOAT",
                        "location VARCHAR(255)",
                        "invoice_number VARCHAR(255)",
                        "order_date DATE",
                        "order_time TIME",
                        "product_name VARCHAR(255)",
                        "product_code VARCHAR(255)",
                        "quantity INTEGER",
                        "weight FLOAT",
                        "total_weight FLOAT",
                        "price FLOAT",
                        "total_price FLOAT"])
    invoice_data = []
    for _ in range(num_orders):
        order_data = generate_invoice_products()
        invoice_data.extend(order_data)
        load_transactions_table("transactions", invoice_data)
