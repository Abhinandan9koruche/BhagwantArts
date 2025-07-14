from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Make sure to use a strong secret key
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'homepage'

# Define the database models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"Product('{self.name}', '{self.category}', '{self.price}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"
    
    # Set password after hashing
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    # Check if the password matches
    def check_password(self, password):
        return check_password_hash(self.password, password)

# Initialize the database (create tables)
with app.app_context():
    db.create_all()  # This creates the database tables if they don't exist

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Routes
@app.route('/')
def homepage():
    if current_user.is_authenticated:
        # Optionally, you can perform additional checks for logged-in users
        pass
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for('login'))

    products = Product.query.all()  # Get all products
    categories = set(product.category for product in products)  # Get unique categories
    return render_template('homepage.html', products=products, categories=categories)

@app.route('/search_results', methods=['GET'])
def search_results():
    query = request.args.get('q')  # Retrieve search query from the URL
    if query:
        # Perform the search query on name or description
        results = Product.query.filter(Product.name.contains(query) | Product.description.contains(query)).all()
    else:
        results = Product.query.all()  # If no query, return all products
    return render_template('search_results.html', results=results)



@app.route('/product_ganesh')
def product_ganesh():
    return render_template('product_ganesh.html')

@app.route('/product_ox')
def product_ox():
    return render_template('product_ox.html')

@app.route('/product_decorativeitems')
def product_decorativeitems():
    return render_template('product_decorativeitems.html')

@app.route('/product_diyas')
def product_diyas():
    return render_template('product_diyas.html')

@app.route('/product_pots')
def product_pots():
    return render_template('product_pots.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):  # Check hashed password
            login_user(user)
            flash('Login successful!')  # Flash success message
            return redirect(url_for('homepage'))  # Redirect to homepage after successful login
        else:
            flash('Login failed. Check your credentials and try again.')  # Flash error message

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.')
        else:
            new_user = User(username=username, password=password)
            new_user.set_password(password)  # Hash the password before saving
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_logged_in', None)  # Clear the session
    return redirect(url_for('homepage'))  # Redirect to homepage after logout


@app.route('/check_login_status')
def check_login_status():
    return jsonify({'logged_in': current_user.is_authenticated})

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # Get data from the form submission
        fullname = request.form['fullname']
        username = request.form['username']
        email = request.form['email']

        # Store data in session (or in a database if needed)
        session['fullname'] = fullname
        session['username'] = username
        session['email'] = email

        return redirect(url_for('profile'))  # Redirect to the profile page to display updated info

    # If GET request, display the form or user data
    user_data = {
        'fullname': session.get('fullname', 'N/A'),
        'username': session.get('username', 'N/A'),
        'email': session.get('email', 'N/A')
    }

    return render_template('profile.html', user=user_data)

@app.route('/confirmation_of_booking')
def confirmation_of_booking():
    return render_template('confirmation_of_booking.html')

@app.route('/confirmation_of_order')
def confirmation_of_order():
    return render_template('confirmation_of_order.html')

@app.route('/termsandconditions')
def termsandconditions():
    return render_template('termsandconditions.html')

@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    if request.method == 'POST':
        # Handle form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Process or save the data
        return redirect(url_for('thank_you'))  # Redirect to a thank you page or show success message
    return render_template('contactus.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/Clay1')
def Clay1():
    return render_template('Clay1.html')

@app.route('/Clay2')
def Clay2():
    return render_template('Clay2.html')

@app.route('/Clay3')
def Clay3():
    return render_template('Clay3.html')

@app.route('/Clay4')
def Clay4():
    return render_template('Clay4.html')

@app.route('/Clay5')
def Clay5():
    return render_template('Clay5.html')

@app.route('/Clay6')
def Clay6():
    return render_template('Clay6.html')

@app.route('/Clay7')
def Clay7():
    return render_template('Clay7.html')

@app.route('/Clay8')
def Clay8():
    return render_template('Clay8.html')

@app.route('/Decorate1')
def Decorate1():
    return render_template('Decorate1.html')

@app.route('/Decorate2')
def Decorate2():
    return render_template('Decorate2.html')

@app.route('/Decorate3')
def Decorate3():
    return render_template('Decorate3.html')

@app.route('/Decorate4')
def Decorate4():
    return render_template('Decorate4.html')

@app.route('/Decorate5')
def Decorate5():
    return render_template('Decorate5.html')

@app.route('/diya1')
def diya1():
    return render_template('diya1.html')

@app.route('/diya2')
def diya2():
    return render_template('diya2.html')

@app.route('/diya3')
def diya3():
    return render_template('diya3.html')

@app.route('/diya4')
def diya4():
    return render_template('diya4.html')

@app.route('/diya5')
def diya5():
    return render_template('diya5.html')

@app.route('/diya6')
def diya6():
    return render_template('diya6.html')

@app.route('/Ganesh2')
def Ganesh2():
    return render_template('Ganesh2.html')

@app.route('/Ganesh3')
def Ganesh3():
    return render_template('Ganesh3.html')

@app.route('/Ganesh4')
def Ganesh4():
    return render_template('Ganesh4.html')

@app.route('/Ganesh5')
def Ganesh5():
    return render_template('Ganesh5.html')

@app.route('/Ganesh6')
def Ganesh6():
    return render_template('Ganesh6.html')

@app.route('/Ganesh7')
def Ganesh7():
    return render_template('Ganesh7.html')

@app.route('/Ganesh8')
def Ganesh8():
    return render_template('Ganesh8.html')

@app.route('/Ganesh9')
def Ganesh9():
    return render_template('Ganesh9.html')

@app.route('/Ganesh10')
def Ganesh10():
    return render_template('Ganesh10.html')

@app.route('/ox1')
def ox1():
    return render_template('ox1.html')

@app.route('/ox2')
def ox2():
    return render_template('ox2.html')

@app.route('/ox3')
def ox3():
    return render_template('ox3.html')

if __name__ == "__main__":
    app.run(debug=True)
