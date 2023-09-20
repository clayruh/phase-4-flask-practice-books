from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Book(db.Model, SerializerMixin):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    page_count = db.Column(db.Integer, db.CheckConstraint('page_count > 0'), nullable=False, )
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'))

    publisher = db.relationship('Publisher', back_populates='books')
    author = db.relationship('Author', back_populates='books')
    
    serialize_rules = ('-publisher.books', '-author.books')

class Publisher(db.Model, SerializerMixin):
    __tablename__ = 'publishers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    founding_year = db.Column(db.Integer, nullable=False)

    books = db.relationship('Book', back_populates='publisher')
    author = association_proxy('books','author')
    serialize_rules = ('-books.publisher',)

    @validates('founding_year')
    def validate_founding_year(self, key, value):
        if value >= 1600 and value <= 2023:
            return value
        return ValueError('founding year is before 1600 or in the future')

class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    pen_name = db.Column(db.String)

    books = db.relationship('Book', back_populates='author')
    publisher = association_proxy('books','author')
    serialize_rules = ('-books.author',)