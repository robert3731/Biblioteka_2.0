from flask import jsonify, request, make_response, abort
from app import app, db
from app.models import Book, BookSchema, book_schema, Author


@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    items = BookSchema(many=True).dump(books)

    return jsonify({
        'books': items,
        'number_of_records': len(items)
    })


@app.route('/authors/books/<int:author_id>', methods=['GET'])
def get_authors_books(author_id):
    Author.query.get_or_404(author_id, description=f'Author with id {author_id} not found')
    books = Book.query.filter(Book.author_id == author_id).all()
    items = BookSchema(many=True, exclude=['author']).dump(books)
    return jsonify({
        'books': items,
        'number_of_records': len(items)
    })


@app.route('/authors/books/<int:author_id>', methods=['POST'])
def create_book(author_id):
    Author.query.get_or_404(author_id, description=f'Author with id {author_id} not found')
    data = request.get_json()
    if Book.query.filter(Book.isbn == data.get('isbn')).first():
        abort(409)
    else:
        title = data.get('title')
        isbn = data.get('isbn')
        description = data.get('description')
        availability = data.get('availability')
        book = Book(title=title, isbn=isbn, description=description, author_id=author_id)
        db.session.add(book)
        db.session.commit()

    return jsonify({
        'information': 'Successfully added new book'
    }), 201


@app.route("/books/<int:book_id>/", methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id, description=f"Book with ID {book_id} not found")
    item = book_schema.dump(book)
    return jsonify({
        'authors': item
    })


@app.route("/books/<int:book_id>", methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id, description=f"Book with ID {book_id} not found")
    print(book)
    data = request.get_json()
    book.title = data.get('title')
    book.isbn = data.get('isbn')
    book.description = data.get('description')
    book.availability = data.get('availability')
    book.author_id = data.get('author_id')
    db.session.commit()
    return jsonify({
        'information': 'Successfully updated book'
    })


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id, description=f"Book with ID {book_id} not found")
    db.session.delete(book)
    db.session.commit()
    return jsonify({
        'information': f'Successfully deleted book'
    })


@app.route('/books/available', methods=['GET'])
def get_available_books():
    books = Book.query.filter_by(availability=True)
    items = BookSchema(many=True).dump(books)

    return jsonify({
        'available_books': items,
        'number_of_records': len(items)
    })


@app.route('/books/unavailable', methods=['GET'])
def get_unavailable_books():
    books = Book.query.filter_by(availability=False)
    items = BookSchema(many=True).dump(books)
    return jsonify({
        'unavailable_books': items,
        'number_of_records': len(items)
    })


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.errorhandler(409)
def conflict(error):
    return make_response(jsonify({'error': 'Already exists', 'status_code': 409}), 409)
