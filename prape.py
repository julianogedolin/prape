from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cad/user")
def user():
    return render_template('user.html')

@app.route("/cad/caduser")
def caduser():
    return render_template('caduser.html')

@app.route("/cad/cadnewuser", methods=['POST'])
def cadNewuser():
    return request.form

@app.route("/cad/product")
def product():
    return render_template('product.html')

@app.route("/cad/notproduct")
def notProduct():
    return render_template('notproduct.html')

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