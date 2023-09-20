#!/usr/bin/env python3

from app import app
from models import db, Author, Publisher, Book
from faker import Faker
import random

faker = Faker()

if __name__ == '__main__':
    with app.app_context():
        print('Deleting database...')
        Author.query.delete()
        Publisher.query.delete()
        Book.query.delete()

        print("Seeding database...")
        print("Seeding authors...")
        authors = []
        for _ in range(10):
            author = Author(
                name = faker.name(),
                pen_name = faker.user_name()
            )
            authors.append(author)
            db.session.add_all(authors)
            db.session.commit()

        print("Seeding publishers...")
        publishers = []
        for _ in range(15):
            publisher = Publisher(
                name = faker.word(),
                founding_year = random.randint(1600, 2023)
            )
            publishers.append(publisher)
            db.session.add_all(publishers)
            db.session.commit()

        print("Seeding books...")
        books = []
        for _ in range(15):
            book = Book(
                title = faker.word(),
                page_count = faker.random_number(),
                author_id = random.randint(1,10),
                publisher_id = random.randint(1,15)
            )
            books.append(book)
            db.session.add_all(books)
            db.session.commit()

        print("Seeding complete!")
