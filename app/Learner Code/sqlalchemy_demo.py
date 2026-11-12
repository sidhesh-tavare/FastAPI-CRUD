import sqlite3
from typing import Any
from app.schemas.models import ProductCreate,ProductUpdate,BaseProduct
from collections.abc import Generator
from contextlib import contextmanager
class Database:

    def connect_to_db(self):
        self.conn = sqlite3.connect('products.db',check_same_thread=False)
        self.curr = self.conn.cursor()
        self.rowfactory = sqlite3.Row 
        self.create_table()

    def create_table(self):
        query = """
                    CREATE TABLE IF NOT EXISTS products(
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        price REAL NOT NULL,
                        stock INTEGER NOT NULL  
                    )
                """

        try:
            with self.conn:
                curr = self.conn.cursor()
                curr.execute(query)
        except sqlite3.Error as e:
            print(f"Error creating table {e}")

    def create_product(self, product: ProductCreate):
      data = product.model_dump()

      create_query = """
            INSERT INTO products (id, name, price, stock)
            VALUES (:id, :name, :price, :stock)
        """

      try:
        with self.conn:
          curr = self.conn.cursor()

          curr.execute("SELECT MAX(id) FROM products")
          max_id = curr.fetchone()[0]
          data["id"] = (max_id or 0) + 1

          curr.execute(create_query, data)
          return data["id"]

      except sqlite3.IntegrityError as ie:
        print(f"Integrity Error: {ie}")
        return None
      except sqlite3.Error as e:
        print(f"Database Error: {e}")
        return None

    def get_product(self, product_id: int) -> dict[str, Any] | None:
        query = "SELECT * FROM products WHERE id = :id"
        try:
            curr = self.conn.cursor()
            curr.row_factory = sqlite3.Row
            curr.execute(query, {"id": product_id})
            res = curr.fetchone()
            return res
        except sqlite3.Error as e:
            print(f"Error fetching product {product_id}: {e}")
            return None

    def update_product(self, product_id: int, new_product: ProductUpdate) -> dict[str, Any] | None:
        # Only include fields the user actually sent (ignores unset Optional fields)
        updates = new_product.model_dump(exclude_unset=True)

        if not updates:
            return self.get_product(product_id)

        # Dynamically build: "name = :name, price = :price"
        set_clause = ", ".join(f"{key} = :{key}" for key in updates)
        query = f"UPDATE products SET {set_clause} WHERE id = :id"
        updates["id"] = product_id

        try:
            with self.conn:  # <-- Automatically commits the UPDATE
                curr = self.conn.cursor()
                curr.execute(query, updates)
                if curr.rowcount == 0:
                    return None
                return self.get_product(product_id)  # Return the full, updated row
        except sqlite3.Error as e:
            print(f"Error updating product {product_id}: {e}")
            return None

    def delete_product(self,product_id : int)->dict[str,str] | None:
        query = 'DELETE FROM products WHERE id = :id'
        try:
            with self.conn:
                curr = self.conn.cursor()
                curr.execute(query,{'id':product_id})
                if curr.rowcount == 0:
                    return None
                return {"message" : "Product deleted Successfully"}
        except sqlite3.Error as e:
            print(f"Error Deleting Product : {e}")
            return None
    
    def close(self):
        if self.conn : self.conn.close()

    '''
    Context Manager using class using dunder methods of __enetr__ and __exit__ 
    '''

    def __enter__(self):
        self.connect_to_db()
        return self 

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False 


# with Database() as db:
#     res = db.get_product(1)
#     print(dict(res))

#     '''
#     here we did not are about open , commit , clsoe connection 
#     '''


# def gen_table():
#     table = [5,10,15,20,25]
#     for n in table:
#         yield n 

# gen = gen_table()
# print(next(gen)) # this is gen to use it save in variable
# print(next(gen))
# print(next(gen))
# print(next(gen))
# print(next(gen))
# # print(list(gen_table()))

'''
Context manager using generatro fucntion 
'''
@contextmanager
def managed_db():
    db = Database()
    db.connect_to_db()
    try:
        yield db 
    finally:
        db.close()

with managed_db() as db:
    print(dict(db.get_product(1)))