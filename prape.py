from select import select
from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
from flask_login import (current_user, LoginManager,
                         login_user, logout_user, login_required)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://julianopp:080818Tj@julianopp.mysql.pythonanywhere-services.com:3306/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_key'
)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class Usuario(db.Model):
    id = db.Column('idusuario', db.Integer, primary_key=True)
    nome = db.Column('usu_nome', db.String(256))
    email = db.Column('usu_email', db.String(256))
    senha = db.Column('usu_senha', db.String(256))
    cel = db.Column('usu_cel', db.String(256))

    def __init__(self, nome, email, senha, cel):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cel = cel

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Categoria(db.Model):
    id = db.Column('idcategoria', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(256))
    detalhe = db.Column('cat_det', db.String(256))

    def __init__(self, nome, detalhe):
        self.nome = nome
        self.detalhe = detalhe


class Produto(db.Model):
    id = db.Column('idproduct', db.Integer, primary_key=True)
    nome = db.Column('prod_nome', db.String(256))
    qtdd = db.Column('prod_qtdd', db.Integer)
    preco = db.Column('prod_preco', db.Integer)
    detalhe = db.Column('prod_det', db.String(256))
    idusuario = db.Column('usuario_idusuario', db.Integer,
                          db.ForeignKey(Usuario.id))
    idcategoria = db.Column('categoria_idcategoria',
                            db.Integer, db.ForeignKey(Categoria.id))

    def __init__(self, nome, qtdd, preco, detalhe, idcategoria):
        self.nome = nome
        self.qtdd = qtdd
        self.preco = preco
        self.detalhe = detalhe
        self.idcategoria = idcategoria


@app.route("/")
def index():
    return render_template('index.html')


@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(id)


@app.route("/login/caduser")
def caduser():
    return render_template('caduser.html')


@app.route("/login/caduser/registeruser", methods=['POST'])
def registerUser():
    usuario = Usuario(request.form.get('user'), request.form.get(
        'email'), request.form.get('psw'), request.form.get('cel'))
    db.session.add(usuario)
    db.session.commit()
    return 'ok'


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('email')
        password = request.form.get('pswd')

        user = Usuario.query.filter_by(email=user, senha=password).first()

        if user:
            login_user(user)
            return redirect('/')
        else:
            return redirect('/login')
    return render_template('login.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')


@app.route("/product")
def product():
    return render_template('product.html')


@app.route("/product/cadproduct")
@login_required
def cadproduct():
    return render_template('cadproduct.html', produtos=Produto.query.all(), categorias=Categoria.query.all())


@app.route("/product/cadproduct/registernewproduct", methods=['POST'])
def registerproduct():
    produto = Produto(request.form.get('nome'), request.form.get('qtdd'), request.form.get(
        'preco'), request.form.get('detalhe'), request.form.get('idcategoria'))
    db.session.add(produto)
    db.session.commit()
    return redirect('/product/cadproduct')


@app.route("/product/deleteproduct/<int:id>")
def deletarproduto(id):
    produto = Produto.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect('/product/cadproduct')


@app.route("/product/edit/product/<int:id>", methods=['GET', 'POST'])
def editarproduto(id):
    produto = Produto.query.get(id)
    if request.method == 'POST':
        produto.nome = request.form.get('nome')
        produto.qtdd = request.form.get('qtdd')
        produto.preco = request.form.get('preco')
        produto.detalhe = request.form.get('detalhe')
        produto.idcategoria = request.form.get('idcategoria')
        db.session.add(produto)
        db.session.commit()
        return redirect('/product/cadproduct')

    return render_template('eproduct.html', produto=produto, categorias=Categoria.query.all())


@app.route("/cad/notproduct")
def notProduct():
    return render_template('notproduct.html')


@app.route("/cadcategoria")
@login_required
def cadcategoria():
    return render_template('categoria.html', categorias=Categoria.query.all())


@app.route("/cadcategoria/registernewcategoria", methods=['POST'])
def registercategoria():
    categoria = Categoria(request.form.get(
        'nome'), request.form.get('detalhe'))
    db.session.add(categoria)
    db.session.commit()
    return redirect('/cadcategoria')


@app.route("/cadcategoria/deletecategoria/<int:id>")
def deletecategoria(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect('/cadcategoria')


@app.route("/product/purchase")
def purchase():
    print("produto comprado")
    return ""


@app.route("/rel/sale")
def relSale():
    return render_template('relSale.html')


@app.route("/rel/purchase")
def relPurchase():
    return render_template('relPurchase.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.errorhandler(404)
def paginanaoencontrada(error):
    return render_template('error404.html')


if __name__ == 'prape':
    db.create_all()
    app.run()
