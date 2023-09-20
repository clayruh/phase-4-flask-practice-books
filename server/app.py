#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Book, Publisher, Author

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/') 
def index():
    return "Hello world"

@app.get('/authors/<int:id>')
def get_authors_by_id(id):
    try:
        author = Author.query.filter(Author.id == id).first()
        # print(author)
        return jsonify(author.to_dict(rules=('-books.publisher',))), 200
    except:
        return jsonify({"error": "author could not be found"}), 404
    
@app.delete('/authors/<int:id>')
def delete_author(id):
    try: 
        author = Author.query.filter(Author.id == id).first()
        db.session.delete(author)
        db.session.commit()
        return {}, 204
    except:
        return jsonify({'error':'author could not be found by that id'}), 404

@app.get('/books')
def get_books():
    books = Book.query.all()
    book = [book.to_dict(rules=('-author.id','-author.pen_name', '-author_id','-publisher_id','-publisher.id', '-publisher.founding_year')) for book in books]
    return jsonify(book), 200

@app.post('/books')
def create_book():
    data = request.json
    author = Author.query.filter(Author.id == data['author_id']).first()
    publisher = Publisher.query.filter(Publisher.id == data['publisher_id']).first()

    book = Book(
        title = data['name'],
        page_count = data['page_count'],
        author = author,
        publisher = publisher
    )
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict()), 201

@app.get('/publishers/<int:id>')
def get_publishers(id):
    try:
        publisher = Publisher.query.filter(Publisher.id == id).first()
        # can you show only the books.author? how would you pull out the authors like in the test?
        return jsonify(publisher.to_dict(rules=('-books','books.author'))), 201
    except:
        return jsonify({'error':'publisher not found'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
