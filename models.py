from sqlalchemy import create_engine, Column, Date, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'
    
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    date_updated = Column(Date)
    

    def __repr__(self):
        return f'Product Name: {self.product_name}, Product Price: {self.product_price}, Product Quantity: {self.product_quantity}, Date Updated: {self.date_updated}'