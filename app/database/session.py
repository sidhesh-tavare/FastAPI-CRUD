from sqlmodel import SQLModel, create_engine, Session
from .models import ProductCategory, Product

engine = create_engine(
    "sqlite:///products.db",
    echo=True,
    connect_args={"check_same_thread": False},
)


def create_db_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session