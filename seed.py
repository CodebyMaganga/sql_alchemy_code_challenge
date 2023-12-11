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

    def all_reviews(self):
        reviews_list = []
        for review in self.reviews:
            review_string = f"Review for {self.name} by {review.customer.full_name()}: {review.star_rating} stars."
            reviews_list.append(review_string)
        return reviews_list

    @classmethod
    def fanciest(cls):
        restaurants = cls.query.all()

        fanciest_one = max(restaurants, key=lambda restaurant: restaurant.price)

        return fanciest_one

    def __repr__(self):
        return f'{self.name} Restaurant'

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())

    restaurants = relationship('Restaurant', secondary=review_association_table, backref='customers')
    reviews = relationship('Review', backref='customer')

    def full_name(self):
        return f'{self.first_name} {self.last_name}' 

    def favorite_restaurant(self):
        customer_reviews = sorted(self.reviews, key=lambda review: review.star_rating, reverse=True)

        if customer_reviews:
            return customer_reviews[0].restaurant

        return None 
    
    def add_review(self, restaurant, rating):
        new_review = Review(customer = self, restaurant = restaurant, rating = rating)
        self.reviews.append(new_review)
    
    def delete_review(self, restaurant):
        search_reviews = [review for review in self.reviews if review.restaurant == restaurant]

        for review in search_reviews:
            self.reviews.remove(review)



    def __repr__(self):
        return f'Customer:{self.first_name} {self.last_name}'

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)
    comment = Column(String())
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    star_rating = Column(Integer())

    customer = relationship('Customer', back_populates='reviews')  
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))  

    restaurant = relationship('Restaurant', back_populates='reviews') 

    def full_name(self):
        return f'Review for {self.restaurant} by {self.customer}: {self.star_rating}'

