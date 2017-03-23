from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, render_template, url_for
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres1@localhost:5433/Login'

db = SQLAlchemy(app)


# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500), unique=True)
    email = db.Column(db.String(500), unique=True)
    password = db.Column(db.String(500))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

# class Curso(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nombre = db.Column(db.String(140))
#     descripcion = db.Column(db.String(500))
#     recursos = relationship(Recurso)

class Recurso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(140))
    descripcion = db.Column(db.String(500))
    url = db.Column(db.String(500))
    preview_img = db.Column(db.String(500))
    curso_id = db.Column(Integer, ForeignKey('User.id'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logedin')
def logedin():
    return render_template('logedin.html')

@app.route('/register', methods=['POST'])
def register():
    user = User(request.form['username'], request.form['email'], request.form['password'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/login')
def log():
    return render_template('login.html')

@app.route('/login_user', methods=['GET'])
def login_user():
    mail = request.args.get('email')
    pas = request.args.get('password')
    user = User.query.filter_by(email=mail, password=pas).first()
    if user!=None:
        return redirect(url_for('index'))
    else:
        return "Usuario no valido"

if __name__ == "__main__":
    app.run(debug=True)
