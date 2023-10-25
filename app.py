from werkzeug.utils import secure_filename
from flask import Flask, Response, flash, make_response, render_template, request, session, url_for, redirect
from flask_login import login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
from flask_migrate import Migrate


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite"
app.config["SECRET_KEY"] = "mamoud"
db = SQLAlchemy()
migrate = Migrate(app, db)


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))
    confirmPassword = db.Column(db.String(80))
    
       
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    #products = db.relationship('Product', backref='category', lazy=True)
    
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
 # Champ pour le prix du produit
    
class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #name_product = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    image = db.Column(db.String(255))
    #img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    #mimetype = db.Column(db.Text, nullable=False)

    
        
    
db.init_app(app)
 
 
with app.app_context():
    db.create_all()
@app.route('/')
def home():
    return render_template('index.html')

# enregistrement de l'utilisateur
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user = User(
            name = request.form.get('name'),
            username = request.form.get('username'),
            email = request.form.get('email'),
            password = request.form.get('password'),
            confirmPassword = request.form.get('confirmPassword')
        )
        flash("c'est bon")

        # Ajout de l'utilisateur à la base de données
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user  = User.query.filter_by(email = email, password = password).first()
        if user:
            session['username'] = user.name
            return redirect (url_for('user_connecte'))
        flash('email ou mot de passe incorrect')
    return render_template("login.html")
@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html")


@app.route("/user_connecte")
def user_connecte():
    return render_template("user_connect.html")

@app.route('/ajouter', methods=['GET','POST'])
def ajouter():
    if request.method == 'POST':
        user = User(
            name = request.form.get('name'),
            username = request.form.get('username'),
            email = request.form.get('email'),
            password = request.form.get('password'),
            confirmPassword = request.form.get('confirmPassword')
    )
        flash("c'est bon")

        # Ajout de l'utilisateur à la base de données
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('data'))
    return render_template('ajouteruser.html')
    
# connexion de l'utilisateur


# apres la connexion de l'utilisateur

@app.route("/delete<int:id>", methods=['GET', 'POST'])
def delete(id):
    data = User.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return  redirect("/data")

@app.route("/update<int:id>",methods=['GET','POST'])
def update(id):
    user = User.query.get(id)  # Récupérez l'utilisateur que vous souhaitez mettre à jour
    if user:
        if request.method == 'POST':
            user.name = request.form.get('name')  # Mettez à jour les attributs de l'utilisateur
            user.username = request.form.get('username')
            user.email = request.form.get('email')
            user.password = request.form.get('password')
            user.confirmPassword = request.form.get('confirmPassword')
            db.session.commit()  # Enregistrez les modifications dans la base de données
            #return redirect('/data')  # Redirigez où vous le souhaitez après la mise à jour
            return redirect (url_for('user_connecte'))
    return render_template('miseajour.html', user=user)

# recuperer tous les utlisateurs pour afficher dans table.html
@app.route('/data')
def data():
    liste_data =  User.query.all()
    return render_template ('table.html',liste_data= liste_data )



# @app.route('/admin', methods=['GET','POST'])
# def admin():
#     if request.method == 'POST':
#         produit = Product(
#             name = request.form.get('name'),
#             image = request.form.get('image'),
#             category = request.form.get('Categories'),
#             price = request.form.get('price')
#         )
#         db.session.add(produit)
#         db.session.commit()
#         flash("c'est bon")
#         return redirect(url_for('afficherimage'))
#     return render_template("picture.html")

# # enregistrement d'un produit dans la base de données a partir du formulaire
# @app.route('/add_product', methods=['GET', 'POST'])
# def add_product():
#     if request.method == 'POST':
#         name = request.form['name']
#         price = request.form['price']
#         image = request.files['image']
#         category_name = request.form['category']

#         # Recherchez la catégorie correspondant au nom sélectionné dans le formulaire
#         category = Category.query.filter_by(name=category_name).first()

#         if category is None:
#             # Gérer le cas où la catégorie n'existe pas
#             return "La catégorie n'existe pas"

#         if image:
#             image_path = PhotoImage.save(image)
#         else:
#             image_path = None

#         product = Product(name=name, price=price, image=image_path, category=category)
#         db.session.add(product)
#         db.session.commit()

#         return redirect(url_for('product_list'))
#     return render_template('add_product.html')

# @app.route('/products')
# def product_list():
#     products = Product.query.all()
#     return render_template('product_list.html', products=products)


@app.route('/picture', methods=['GET','POST'])
def picture():
     return render_template("picture.html")

@app.route('/add_product', methods = ['POST'])
def add_product():
    if request == 'POST':
        product = Product(
            name = request.form.get('name'),
            price = request.form.get('price'),
            categorie  =request.form.get('category')     
        )
        
        flash('produit ajouter')
        db.session.add(product())
        db.session.commit()
        return redirect(url_for('afficherimage'))
    return render_template('picture.html')

class imm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    prix= db.Column(db.Integer, nullable=False)
    def __init__(self, name, prix):
        self.name = name
        self.prix = prix
# @app.route("/images")
# def images():
#     ajout = imm.query.all()
#     return render_template('picture.html', ajout=ajout)

@app.route('/addstore', methods=['GET', 'POST'])
def addstore():
    if request.method == 'POST':
        name = request.form.get('name')
        prix = request.form.get('prix')       
        db.session.add(imm(name=name, prix=prix))
        db.session.commit()
        
        return redirect(url_for('afficherimage'))
    #return render_template('picture.html')
@app.route('/images', methods=['GET'])
# recuper tous les produits pour afficher dans table.html
def afficherimage():
    list_produit = imm.query.all()
    return render_template('afficherimage.html', list_produit=list_produit)


if __name__ == '__main__':
    app.run(debug=True)


#cree une fonction nombre premier
