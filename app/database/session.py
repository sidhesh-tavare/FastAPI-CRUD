from sqlmodel import SQLModel, create_engine, Session
from .models import ProductCategory, Product

engine = create_engine(
    "sqlite:///products.db",
    echo=True,
    connect_args={"check_same_thread": False},
)


def create_db_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_tables()

    with Session(engine) as session:
        # Create product
        product1 = Product(
            name="Wireless Mouse",
            price=23.99,
            stock=25,
            category=ProductCategory.ELECTRONICS,
        )
        session.add(product1)
        session.commit()
        session.refresh(product1)
        print("Created:", product1)

        # Read product
        fetched = session.get(Product, product1.id)
        print("Fetched:", fetched)
