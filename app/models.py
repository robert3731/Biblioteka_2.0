from app import db
from marshmallow import Schema, fields


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    books = db.relationship('Book', back_populates='author', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Author {self.first_name} {self.last_name}>"


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    isbn = db.Column(db.BigInteger, unique=True)
    description = db.Column(db.Text)
    availability = db.Column(db.Boolean, default=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    author = db.relationship('Author', back_populates='books')

    def __repr__(self):
        return f"<Book {self.title} - {self.author.first_name} {self.author.last_name}- {self.availability}>"


class AuthorSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    books = fields.List(fields.Nested(lambda: BookSchema(exclude=['author', 'availability'])))


class BookSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    isbn = fields.Integer()
    description = fields.String()
    availability = fields.Boolean()
    author_id = fields.Integer(load_only=True)
    author = fields.Nested(lambda: AuthorSchema(only=['id', 'first_name', 'last_name']))


author_schema = AuthorSchema()
book_schema = BookSchema()
