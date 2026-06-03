from flask import Flask, render_template, request
import pymysql
from flask_sqlalchemy import SQLAlchemy

conn = pymysql.connect(
        host = 'localhost',
	    user ='beni',
	    password = "ionescubeni",
	    db='beni_postman',
	    )
cur = conn.cursor()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://beni:ionescubeni@localhost/beni_postman'
db = SQLAlchemy(app)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    author = db.Column(db.String(50), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    language = db.Column(db.String(50), nullable = False)
    
    def __init__(self, id, title, author, price, language):
        self.id = id
        self.title = title
        self.author = author
        self.price = price
        self.language = language


@app.route('/', methods = ["GET"])
def get():
    data = Books.query.all()
    return render_template('index.html', data = data)

@app.route('/add', methods = ["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template('add_form.html')
    if request.method == "POST":
        book = Books(
        id = request.form['id'],
        title = request.form['title'],
        author = request.form['author'],
        price = request.form['price'],
        language = request.form['language'])
        db.session.add(book)
        db.session.commit()
        return render_template('return.html')

@app.route('/<id>/delete', methods = ["GET"])
def delete(id):
    if request.method == "GET":
        book = Books.query.get(id)
        print(book)
        db.session.delete(book)
        db.session.commit()
        return render_template('return.html')

@app.route('/<id>/update/', methods = ["GET", "POST"])
def update(id):
    if request.method == "GET":
        book = Books.query.get(id)
        return render_template('update_form.html', book = book)
    if request.method == "POST":
        book = Books.query.get(id)
        book.title = request.form['title']
        book.author = request.form['author']
        book.price = request.form['price']
        book.language = request.form['language']
        db.session.commit()
        conn.commit()
        return render_template('return.html')

if __name__ == "__main__":
    app.run(host = "localhost", port = 8000)
