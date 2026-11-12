import sqlite3
from typing import Any
from schemas.models import ProductCreate,ProductUpdate,BaseProduct

class Database:

    def __init__(self):
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
