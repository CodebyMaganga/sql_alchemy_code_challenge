from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

review_association_table = Table(
    'reviews_user',
    Base.metadata,
    Column('customer_id', ForeignKey('customers.id')),
    Column('review_id', ForeignKey('reviews.id'))
)

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    price = Column(Integer())

    customers = relationship('Customer', secondary=review_association_table, backref='restaurants')
    reviews = relationship('Review', backref='restaurant')  

    def __repr__(self):
        return f'{self.name} Restaurant'

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())

    restaurants = relationship('Restaurant', secondary=review_association_table, backref='customers')
    reviews = relationship('Review', backref='customer')  

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)
    comment = Column(String())
    customer_id = Column(Integer(), ForeignKey('customers.id'))

    customer = relationship('Customer', back_populates='reviews')  
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))  

    restaurant = relationship('Restaurant', back_populates='reviews') 

