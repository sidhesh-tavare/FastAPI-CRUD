# Python Context Managers: Class vs. Generator

In Python, there are two ways to create a context manager (something you can use with a `with` statement):

---

## 1. Class-Based Context Manager (`__enter__` and `__exit__`)

Best when your resource already has state or multiple methods (like a `Database` class with CRUD operations).

- **`__enter__(self)`**: Runs when entering the `with` block; returns the resource (`self`).
- **`__exit__(self, exc_type, exc_val, exc_tb)`**: Runs when exiting the `with` block (even if an error happens) to close/clean up resources. Returning `False` lets any exception propagate normally.

```python
import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("products.db", check_same_thread=False)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        return False

# Usage:
with Database() as db:
    ...
```
