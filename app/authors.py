from flask import jsonify, request, make_response
from app import app, db
from app.models import Author, AuthorSchema, author_schema


@app.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    author_schema = AuthorSchema(many=True)

    return jsonify({
        'Authors': author_schema.dump(authors),
        'number_of_records': len(authors)
    })


@app.route('/authors', methods=['POST'])
def create_author():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    author = Author(first_name=first_name, last_name=last_name)
    db.session.add(author)
    db.session.commit()
    return jsonify({
        'information': 'Succesfully added new author'
    }), 201


@app.route("/authors/<int:author_id>/", methods=['GET'])
def get_author(author_id):
    author = Author.query.get_or_404(author_id, description=f"Author with ID {author_id} not found")
    return jsonify({
        'authors': author_schema.dump(author)
    })


@app.route("/authors/<int:author_id>", methods=['PUT'])
def update_author(author_id):
    author = Author.query.get_or_404(author_id, description=f"Author with ID {author_id} not found")
    print(type(author))
    data = request.get_json()
    author.first_name = data.get('first_name')
    author.last_name = data.get('last_name')
    db.session.commit()
    return jsonify({
        'information': 'Succesfully updated author'
    })


@app.route("/authors/<int:author_id>", methods=["DELETE"])
def delete_author(author_id):
    author = Author.query.get_or_404(author_id, description=f"Author with ID {author_id} not found")
    db.session.delete(author)
    db.session.commit()
    return jsonify({
        'information': f'Succesfully deleted author wit ID {author_id}'
    })


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Author not found', 'status_code': 404}), 404)


@app.errorhandler(409)
def conflict(error):
    return make_response(jsonify({'error': 'Author already exists', 'status_code': 409}), 409)