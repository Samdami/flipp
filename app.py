from flask import Flask, render_template, url_for, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, LoginManager, UserMixin, current_user
import os

base_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
server = app.server

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, 'my_login.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payment.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'f8a68de9b6d130c88cff779a'


db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(db.Model, UserMixin):
    """This is the User database model"""
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.Text(), nullable=False)
   

    def __repr__(self):
        return f"User <{self.username}>"
        
@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))

class PaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    card_number = db.Column(db.String(16), nullable=False)
    exp_month = db.Column(db.String(2), nullable=False)
    exp_year = db.Column(db.String(4), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return '<PaymentMethod %r>' % self.name

@app.route('/api/payments', methods=['POST'])
def create_payment():
    amount = request.json.get('amount')
    card_number = request.json.get('card_number')
    # process payment here
    return jsonify({'message': 'Payment processed successfully'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/cashflip', methods=['GET', 'POST'])
def cashflip():
    return render_template('payment.html')    

@app.route('/add_payment_method', methods=['GET', 'POST'])
def add_payment_method():
    if request.method == 'POST':
        name = request.form['name']
        card_number = request.form['card_number']
        exp_month = request.form['exp_month']
        exp_year = request.form['exp_year']
        # expiration_date = request.form['expiration_date']
        cvv = request.form['cvv']

        if not name or not card_number or not exp_month or not exp_year or not cvv:
            return render_template('payment.html', error='All fields are required.')
        if not card_number.isdigit() or len(card_number) != 16:
            return render_template('payment.html', error='Invalid card number.')
        if not exp_month.isdigit() or len(exp_month) != 2 or int(exp_month) < 1 or int(exp_month) > 12:
            return render_template('payment.html', error='Invalid expiration month.')
        if not exp_year.isdigit() or len(exp_year) != 4:
            return render_template('payment.html', error='Invalid expiration year.')
        if not cvv.isdigit() or len(cvv) != 3:
            return render_template('payment.html', error='Invalid CVV.')

        payment_method = PaymentMethod(name=name, card_number=card_number, exp_month=exp_month, exp_year=exp_year, cvv=cvv)
        db.session.add(payment_method)
        db.session.commit()

        return 'Payment method added successfully!'
    else:    
        return render_template('payment.html')

@app.route('/pay')
def payment():
    return render_template('payment.html')    

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error_msg="Invalid username or password. Try again.")
    return render_template('login.html')


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Check if payment information is provided
        if 'paymentmethod' not in request.form:
            # Payment information not provided, show payment form
            return render_template('payment.html')
        
        # Payment information provided, process the payment
        paymentmethod = request.form['payment_info']
        # Process the payment here
        
        return "Payment successful"
    
    # Display checkout page
    return render_template('checkout.html')

@app.route('/logout')
def logout():
    logout_user() 
    return redirect(url_for('login'))


@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html')


@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        passwords_no_match = ""

        if confirm != password:
            passwords_no_match = "The two passwords must match"

        username_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()

        if username_exists or email_exists or passwords_no_match:
            username_msg = "This Username is already being used by another user."
            email_msg = "This Email is already being used by another user."
            return render_template('signup.html', username_error=username_msg, email_error=email_msg, password_error=passwords_no_match)
        password_hash = generate_password_hash(password)

        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run_server(debug=false)
