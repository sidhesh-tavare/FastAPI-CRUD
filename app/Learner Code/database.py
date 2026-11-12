import sqlite3

create_table_query = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'available'
    )
"""

insert_query = """
    INSERT INTO products (id, name, price, stock, status)
    VALUES (?, ?, ?, ?, ?)
"""

update_query = """
    UPDATE products SET stock = ? WHERE id = ?
"""

delete_query = """DELETE FROM products WHERE id = ?"""
delete_data : tuple[int] = (1000,)
update_data : tuple[int,int] = (0,10100)
product_data = (1008, "LaraDutta", 399, 900, "active")

conn = None

# try:
#   with sqlite3.connect("products.db") as conn:
#     curr = conn.cursor()

#     # 1. Ensure table exists
#     curr.execute(create_table_query)

#     # 2. Insert new product
#     curr.execute(insert_query, product_data)
#     print("Inserted")

#     # 3. Read all products
#     curr.execute("SELECT * FROM products")
#     print(f"Read: {curr.fetchall()}")

# except sqlite3.IntegrityError as ie:
#   print(f"Integrity Error: {ie}")
# except sqlite3.Error as e:
#   print(f"Database Error: {e}")
# finally:
#   if conn:
#     conn.close()

# try:
#   with sqlite3.connect('products.db') as conn:
#     curr = conn.cursor()
#     curr.execute(update_query,update_data)

#     if curr.rowcount == 0: print("Such id does not exist")
#     else: print("Updated Successfully")
# except sqlite3.Error as e:
#   print(f"Error : {e}")
# finally:
#   if conn: conn.close()

try:
  with sqlite3.connect('products.db') as conn:
    curr=conn.cursor()
    curr.execute(delete_query,delete_data)

    if curr.rowcount == 0: print("Such id does not exist")
    else: print("DELETED Successfully")
except sqlite3.Error as e:
    print(f"Error : {e}")
finally:
    if conn: conn.close()


