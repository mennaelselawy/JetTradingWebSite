from flask import redirect, request,  url_for ,jsonify, Response , Flask
from models.user import User
from models.device import Devices
from utils.helpers import getHtml
from routes import handleLogin, handleProfile, handleProductsJson
app = Flask("app")

@app.route("/")
def homePage():
    return getHtml("index")

@app.route("/signup", methods=["GET"])
def signUpPage():
    html = getHtml("signup")
    return html.replace("$$ERROR$$" , "")

@app.route("/signup", methods=["POST"])
def signUp():
    user = User()  
    return user.saveData()

@app.route("/login" , methods=["GET"])
def logInPage():
    return getHtml("login")

@app.route("/login" , methods=["POST"])
def logIn():
    return handleLogin()

@app.route("/loggedInHome" , methods=["GET"])
def loggedInHomePage():
    return getHtml("loggedInHome")


@app.route("/profile", methods=["GET"])
def profilePage():
    return handleProfile()

@app.route("/profile" , methods=["POST"])
def updateUser():
    return User().updateUserInfo()

@app.route("/delete", methods=["POST"])
def deleteUserAccount():
    return User().deleteUser()

@app.route("/devices", methods=["GET"])
def devicesPage():
    return Devices.devicesPageHtml("devices", showCartButtons =False)

@app.route("/devicesLoggedIn", methods=["GET"])
def devicesLoggedInPage():
    return Devices.devicesPageHtml("devicesLoggedIn", showCartButtons =True)

@app.route("/products_json")
def productsJson():
    return handleProductsJson()

@app.route("/cart")
def cartPage():
    html = getHtml("cart")
    return html

@app.route("/product", methods=["GET"])
def productPage():
    return Devices.productDetails(logged_in=False)
    
@app.route("/productLoggedIn", methods=["GET"])
def productLoggedInPage():
    return Devices.productDetails(logged_in=True)

if __name__ == '__main__':
    app.run(debug=True)
