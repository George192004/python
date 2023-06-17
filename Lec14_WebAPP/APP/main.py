from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NewtonRaphson'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NewtonRaphson.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    # square = db.relationship('SquareRoot', backref='user')


# class SquareRoot(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     number = db.Column(db.Float, nullable=False)
    # square_root = db.Column(db.Float, nullable=False)
    # numGuesses = db.Column(db.Integer, nullable=False)

    # def __str__(self):
    #     return f'რიცხვი: {self.number}; ფესვი: {round(self.square_root, 3)}; მცდელობა: {self.numGuesses}'


db.create_all()


# def squareRoot(x):
#     square = x
#     epsilon = 0.01
#     guess = square/2
#     numGuesses = 0

#     while abs(guess*guess - square) >= epsilon:
#         numGuesses += 1
#         guess = guess - (((guess**2) - square) / (2*guess))

#     return guess, numGuesses


@app.route('/method')
def method():
    return render_template('method.html')


@app.route('/')
@app.route('/home')
def home():
    return render_template('method.html')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        username = request.form['user']
        email = request.form['email']
        password = request.form['password']

        obj = User(username=username, email=email, password=password)
        db.session.add(obj)
        db.session.commit()

    return render_template('registration.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        mail = request.form['email']
        password = request.form['password']
        obj = User.query.filter_by(email=mail).first()
        if obj.password == password:
            session['username'] = obj.email
            return redirect(url_for('user'))

    return render_template('login.html')


@app.route('/user', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        number = request.form['number']
        # sqrt = squareRoot(float(number))
        # guess, numGuesses = sqrt[0], sqrt[1]

        obj = User.query.filter_by(email=session['username']).first()
        # objSqrt = SquareRoot(user=obj, number=number)
        #  square_root=guess, numGuesses=numGuesses)
        # db.session.add(objSqrt)
        db.session.commit()

        return render_template('sqrt.html', number=number)

    return render_template('user.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('logout.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
