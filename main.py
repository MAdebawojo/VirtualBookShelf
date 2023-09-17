import json
from flask import Flask, session, flash, jsonify, url_for, render_template, request, redirect
from flask_bcrypt import Bcrypt
from pymongo import MongoClient, errors
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_URI = os.getenv('DATABASE_URI')
SECRET_KEY = os.getenv('SECRET_KEY')


app = Flask(__name__)
app.secret_key = SECRET_KEY

# Initialize the MongoDB client
try:
    client = MongoClient(DATABASE_URI)
    # Get the database
    db = client.get_database(DATABASE_NAME)
    # Get the 'user_accounts' collection
    users = db.user_accounts
    # Get the 'user_books' collection
    user_books = db.user_accounts
    # Access the MongoDB collections (books)
    books_collection = db.books
except Exception as e:
    print(f"MongoDB connection error: {e}")
    raise e

bcrypt = Bcrypt(app)

update_book_id = None

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form.get('password')

        try:
            user = users.find_one({'email': email})
            print(user['username'])
        except Exception as e:
            print(f"MongoDB query error: {e}")
            flash(f"Connection error: {e}")
        else:
            if user and bcrypt.check_password_hash(user.get('password', ''), password):
                session['email'] = email
                session['username'] = user['username']
                print(f"Session: {session['username']}")
                return redirect(url_for("library", email=email))
            else:
                flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template("login.html")

@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form.get('password')

        existing_user = users.find_one({'email': email})
        if existing_user:
            flash('Registration failed. Email is already in use.', category='danger')
        elif not password:
            flash('Password cannot be empty', category='danger')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = {
                'username': username,
                'email': email,
                'password': hashed_password
            }

            try:
                users.insert_one(new_user)
                flash('Your account has been created! You are now able to log in.', category='success')
                return redirect(url_for('login'))
            except Exception as e:
                print(f"MongoDB insertion error: {e}")
                flash(f"Connection error: {e}")
    return render_template("register.html")

@app.route('/library/')
def library():
    logged_in_user = session['username'].title()
    # Fetch the book data from the database (you'll need to modify this part)
    book_data = books_collection.find({'email': session['email']})

    # Pass the book data to the template
    return render_template("library.html", username= logged_in_user, book_data=book_data)

@app.route('/add_book/', methods=['POST'])
def add_book():
    if request.method == 'POST' and 'email' in session:
        book_title = request.form.get('book_title')
        description = request.form.get('description')
        authors = request.form.get('authors')
        status = request.form.get('status')
        user_email = session['email']
        book_id = str(ObjectId())

        book_data = {
            'book_id': book_id,
            'book_title': book_title,
            'description': description,
            'authors': authors,
            'status': status,
            'email': user_email
        }

        try:
            books_collection.insert_one(book_data)
            flash('Book added successfully!', 'success')
            return redirect(url_for('library'))
        except errors.DocumentTooLarge as e:
            print(f"MongoDB document size error: {e}")
            flash(f"Document size error: {e}")
        except Exception as e:
            print(f"MongoDB insertion error: {e}")
            flash(f"Connection error: {e}")

@app.route('/update_book/', methods=['POST'])
def update_book():
    if request.method == 'POST' and 'email' in session and update_book_id:
        book_id = ObjectId(update_book_id)
        user_email = session['email']
        book_title = request.form.get('edit_book_title')
        description = request.form.get('edit_book_description')
        authors = request.form.get('edit_book_authors')
        status = request.form.get('edit_book_status')
        updated_book_data = {
            'book_title': book_title,
            'description': description,
            'authors': authors,
            'status': status,
            'email': user_email
        }
        try:
            result = books_collection.update_one({'_id': book_id}, {'$set': updated_book_data})
            if result.modified_count > 0:
                flash('Book updated successfully')
                return redirect(url_for('library'))
            else:
                return redirect(url_for('add_book'))
        except Exception as e:
            print(f"MongoDB update error: {e}")
            return jsonify({'error': str(e)}, 500)

@app.route('/get_book_id/', methods=['POST'])
def get_book_id_route():
    data = request.get_json()
    book_title_to_find = data.get('bookTitle')

    if book_title_to_find:
        email_to_find = session.get('email')
        if email_to_find:
            query = {
                'email': email_to_find,
                'book_title': book_title_to_find
            }

            result = books_collection.find_one(query)
            if result:
                book_id = str(result.get("_id"))
                global update_book_id
                update_book_id = book_id
            return jsonify({'book_id': 'Book Found'})
    return jsonify({'error': 'Book not found'})

@app.route('/delete_book/', methods=['DELETE'])
def delete_book():
    try:
        if update_book_id:
            book_id = ObjectId(update_book_id)
            result = books_collection.delete_one({"_id": book_id})

            if result.deleted_count == 1:
                flash('Book deleted successfully', 'success')
                return jsonify({'message': 'Book deleted successfully'}), 200
    except Exception as e:
        print(f"MongoDB delete error: {e}")
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Book not found'}), 404

@app.route('/logout/')
def logout():
    if 'email' in session:
        session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    print("The server is listening...")
    app.run(debug=True, port=5002)












































