from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import User, db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import flask_monitoringdashboard as dashboard
import secrets

from indeed_scrapping import run_scrapping



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# génération de la clé sécrète
app.secret_key = secrets.token_hex(16)

db.init_app(app)
dashboard.bind(app)

# Initialise le gestionnaire de connexion
login_manager = LoginManager()
login_manager.init_app(app)


app.app_context().push()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('Email déjà utilisé', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256') # nouvelle annottation de 'sha256'
        # Créer un nouvel utilisateur avec les données du formulaire
        new_user = User(username=username, email=email, password_hash=hashed_password)
        # Ajouter le nouvel utilisateur à la base de données
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html')


@login_manager.user_loader
def load_user(user_id):
    # Charge l'utilisateur à partir de la base de données
    return User.query.get(int(user_id))

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Vérifie si l'utilisateur est déjà connecté
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        # Récupère les informations de connexion depuis le formulaire
        email = request.form['email']
        password = request.form['password']

        # Recherche l'utilisateur dans la base de données
        user = User.query.filter_by(email=email).first()

        # Vérifie si le mot de passe est correct
        if not  user or not check_password_hash(user.password_hash, password):
            flash("Email ou mot de passe incorrect")
            return redirect(url_for('login'))
        else:
            # Connecte l'utilisateur
            login_user(user)
            # Redirige l'utilisateur vers la page d'accueil
            return redirect(url_for('home'))
    # Affiche le formulaire de connexion
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Déconnecte l'utilisateur
    logout_user()
    # Redirige l'utilisateur vers la page d'accueil
    return redirect(url_for('home'))



@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')



# route pour la visualisation des résultats

@app.route('/dashboard')
@login_required
def dashboard():

    results = run_scrapping()
    return render_template('dashboard.html',infos = results)



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)