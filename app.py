import flask 
from flask import redirect, request,  url_for ,jsonify, Response , Flask
import json
from urllib.parse import quote

#import os
app = flask.Flask("app")

def getHtml(pageName):
    with open(pageName + ".html") as htmlPage:
        return htmlPage.read()

                                                        # USER
class User:
    def __init__(self, formData = None):
            if formData is None:
                formData = flask.request.form
            self.username = formData.get("username")  #flask-> module , request-> object , form -> property, get-> method 
            self.password = formData.get("password", "").strip()
            self.email = formData.get("email", "" ).strip()
            self.address = formData.get("address", "").strip()
            self.phone = formData.get("phone", "").strip()

    @staticmethod
    def safeHash(text):
        result = ""
        for ch in text:
            code = ord(ch)
            if 32 <= code <= 126:
                shifted = 32 + ((code -32 +3) % 95)
                result += chr(shifted)
            else:
                result += ch
        return result
    
    @staticmethod
    def safeUnhash(text):
        result = ""
        for ch in text:
            code = ord(ch)
            if 32<= code <= 126:
                shifted = 32 +((code -32 -3)%95)
                result += chr(shifted)
            else:
                result += ch
        return result

    def makeDictionary(self):
        dict = {
            "username": self.username,
            "password": User.safeHash(self.password),
            "email": self.email,
            "address": self.address,
            "phone": self.phone
        }
        return dict 
    
    def saveData(self):
        # if the file not exist create one so
        try:
            with open("data/users.json", "r") as f:
                users = json.load(f)   #reads as json file gives python file
        except (FileNotFoundError , json.JSONDecodeError):
            users = [] #file does not exist or empty so i will start with empty list
        
        failedSignUp = getHtml("signup")
        #CHECK THAT THE USER NOT ALREADY EXIST BY EMAIL
        if any(user["email"].lower() == self.email.lower() for user in users) :
            return failedSignUp.replace("$$ERROR$$", "<p style='color:red;'>Sign Up Failed: User already exists</p>")
            
        if len(self.password) < 8:
            return failedSignUp.replace("$$ERROR$$", "<p style='color:red;'>Password must not be less than 8 characters</p>")
        if not (self.email.endswith("@gmail.com") or self.email.endswith("@org.com")):
            return failedSignUp.replace("$$ERROR$$", "<p style='color:red;'>Invalid email domain</p>")
        if len(self.address)< 10:
            return failedSignUp.replace("$$ERROR$$", "<p style='color:red;'>Invalid address: address must be more than 10</p>")
            #append the new user: to add in the python list in memory not in the file
        if not (self.phone.isdigit() and len(self.phone) == 11 and self.phone.startswith("01")):
            return failedSignUp.replace("$$ERROR$$", "<p style='color:red;'>Invalid Phone number</p>")
        
        users.append(self.makeDictionary())
        #to write the new user in the file
        with open("data/users.json", "w") as f:
                json.dump(users, f, indent=4)                #takes python object as user list and writes it as JSON formatted text into file SO reverse of json.load()
        return redirect(url_for("logInPage"))  # redirect after success

    def getUserInfo(self, email):
        try:
            with open("data/users.json", "r") as f:
                users = json.load(f)
        except(FileNotFoundError, json.JSONDecodeError):
            users = []
        for user in users:
            if user["email"].lower() == email.lower():
                return user 
    
    def fillProfileForm(self, userData, message =""):    
        html = getHtml("profile")
        html = html.replace("$$USERNAME$$", userData["username"])
        html = html.replace("$$PASSWORD$$", User.safeUnhash(userData["password"]))
        html = html.replace("$$EMAIL$$", userData["email"])
        html = html.replace("$$ADDRESS$$", userData["address"])
        html = html.replace("$$PHONE$$", userData["phone"])
        html = html.replace("$$ERROR$$", message)
        return html

    def updateUserInfo(self):
         # Server-side validation before updating data
        if len(self.password) < 8:
            return self.fillProfileForm(self.makeDictionary(), "<p style='color:red;'>Password must not be less than 8 characters</p>")
        if len(self.address) < 10:
            return self.fillProfileForm(self.makeDictionary(), "<p style='color:red;'>Address must be more than 10 characters</p>")
        if not (self.phone.isdigit() and self.phone.startswith("01") and len(self.phone) == 11):
            return self.fillProfileForm(self.makeDictionary(), "<p style='color:red;'>Invalid phone number</p>")
            # data = flask.request.form.to_dict()            #.get_json()parse JSON data from the body of an HTTP request (like an API) converts it into a Python dictionary
        try:
            with open("data/users.json", "r") as f:
                users =json.load(f)
        except(FileNotFoundError, json.JSONDecodeError):
            failedPage = getHtml("profile")
            return failedPage.replace("$$ERROR$$", "<p style='color:red;'>Update Failed </p>")
        
        for i in range(len(users)):
            # user = users[i]
            if users[i]["email"] == self.email:
                users[i] = self.makeDictionary()
                break

        with open("data/users.json" , "w") as f:
            json.dump(users, f, indent=4)
        updatedUser = self.makeDictionary()
        return self.fillProfileForm(updatedUser, "<p style='color:green;'>User updated successfully</p>")

    def deleteUser(self):
        try:
            with open("data/users.json", "r") as f:
                users = json.load(f)
        except(FileNotFoundError , json.JSONDecodeError):
            users=[]
        for user in users:
            if user["email"] == self.email:
                users.remove(user)
                break
        with open("data/users.json", "w") as f:
            json.dump(users, f, indent=4)
        return redirect(url_for("homePage"))


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
    html = getHtml("login")
    return html

@app.route("/login" , methods=["POST"])
def logIn():
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()


        if not email or not password:
            return jsonify(success=False, message="Email and password are required")

        with open("data/users.json", "r") as f:
            users = json.load(f)

        for user in users:
            if user["email"] == email and user["password"] == User.safeHash(password):
                return jsonify(success=True, user=user)

        return jsonify(success=False, message="Invalid credentials")

    except Exception as e:
        return jsonify(success=False, message=f"Server error: {str(e)}")

@app.route("/loggedInHome" , methods=["GET"])
def loggedInHomePage():
    return getHtml("loggedInHome")


@app.route("/profile", methods=["GET"])
def profilePage():
    email = flask.request.args.get("email")

    user = User().getUserInfo(email)
    if user:
        return User().fillProfileForm(user, "")
    else:
        return getHtml("login").replace("$$ERROR$$", "<p style='color:red;'>User not found</p>")

#HTML Forms do not suppory put or patch or delete for update or delete 
@app.route("/profile" , methods=["POST"])
def updateUser():
    user = User()
    return user.updateUserInfo()


@app.route("/delete", methods=["POST"])
def deleteUserAccount():
    user = User()
    return user.deleteUser()


                                                 #DEVICES
class Devices:
    def __init__(self, name, description, price, image , category):
        self.name = name
        self.description = description
        self.price = price
        self.image = image
        self.category = category

# make each device dictionary to convert to JSON format if i want to deal with js so i will need it json
    def make_dictionary(self):
        dict={
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "image": self.image,
            "category": self.category,
        }
        return dict

# here i parse the text files to python objects of the class to can deal with it as search/filter
#return list  to deal with html i use lists
    @staticmethod                               #only reads the lines from a file and convert them into Devices objects using constructor
    def parse_products_file():
        products =[]
        try:
            with open("data/products.txt", "r") as f:
                for line in f:
                    property = line.strip().split("|")
                    if len(property) == 5:
                        product = Devices(property[0], property[1], property[2], property[3], property[4])     #it creates objects from the class devices
                        products.append(product)
        except(FileNotFoundError):
            products=[]
        return products
    
    @staticmethod
    def display_devices_html(devices_list, show_cart_buttons=False, logged_in = False):
        html=""
        for device in devices_list: 
            # i used the data- attribute so in javascript will get it by dataset.
            # the quote library for the spaces in the name of the device to put it in teh url without spaces ht7ot mkan l space %
            if logged_in:
                product_page_path = "/productLoggedIn"
            else:
                product_page_path = "/product"
            html += f"""    
               <div class="device-card">
                    <a href="{product_page_path}?name={quote(device.name)}" class = "device-card-link">
                        <img src="static/images/{device.image}" alt="{device.name}" class="device-img">
                        </a>
                        <h3 class="device-name">{device.name}</h3>
                        <p class="device-description">{device.description}</p>
                        <p class="device-price">EGP {device.price}</p> """
            if show_cart_buttons:    
                html += f""" <button class="add-to-cart-button"
                        data-name = "{device.name}"
                        data-description = "{device.description}"
                        data-price = "{device.price}"
                        data-image = "{device.image}">
                        Add to Cart
                    </button>"""
            html += "</div>"
        return html
    
    @staticmethod
    def devicesPageHtml(pageName , showCartButtons):
        devices = Devices.parse_products_file()
        category = request.args.get('category')
        query = request.args.get('query')
        heading =""
        filtered = []
        if query:
            heading = f"Results of {query}"
            query = query.lower()
            for device in devices:
                if query in device.name.lower() or query in device.description.lower():
                    filtered.append(device)
        elif category:
            heading = category.capitalize()
            category = category.lower()
            for device in devices:
                if device.category.lower() == category:
                    filtered.append(device)  
        else:
            filtered = devices
            heading = "All Devices"
        logged_in = (pageName == "devicesLoggedIn")
        devices_html = Devices.display_devices_html(filtered, showCartButtons, logged_in)
        
        if not devices_html:
            devices_html = "<p class='no-results'>No devices found.</p>"
            
        html = getHtml(pageName)
        final_html = html.replace("$$CATEGORY$$", heading).replace("$$DEVICES$$", devices_html)
        return final_html

        
@app.route("/devices", methods=["GET"])
def devicesPage():
    return Devices.devicesPageHtml("devices", showCartButtons =False)

@app.route("/devicesLoggedIn", methods=["GET"])
def devicesLoggedInPage():
    return Devices.devicesPageHtml("devicesLoggedIn", showCartButtons =True)


                                               #CART
class Cart:
    def __init__(self):
        self.items=[]
    
    def add_product(self, product):
        self.items.append(product)
    def remove_product(self, product_name):
        for item in self.items:
            if item.name != product_name:
                self.items =item
    def make_dictionary(self):
        for item in self.item:
            return item.make_dictionary()
    def clear_cart(self):
        self.items = []
    def get_items(self):
        return self.items
    @staticmethod
    def productDetails(logged_in=False):
        product_name = request.args.get("name")
        devices = Devices.parse_products_file()
        for device in devices:
            if device.name.lower() == product_name.lower():
                if logged_in:
                    html = getHtml("productLoggedIn")
                else:
                    html = getHtml("product")
                html = html.replace("$$NAME$$", device.name)
                html = html.replace("$$DESCRIPTION$$", device.description)
                html = html.replace("$$PRICE$$", device.price)
                html = html.replace("$$IMAGE$$", f"static/images/{device.image}")
                html = html.replace("$$CATEGORY$$", device.category.capitalize())
                if logged_in:
                        # Add proper data attributes for JavaScript
                    add_to_cart_html = f"""
                    <button class="add-to-cart-button"
                        data-name="{device.name}"
                        data-description="{device.description}"
                        data-price="{device.price}"
                        data-image="{device.image}">
                        Add to Cart
                    </button>"""
                    html = html.replace("$$ADD_TO_CART$$", add_to_cart_html)
                else:
                    html = html.replace("$$ADD_TO_CART$$","")
                return html
        return "<p>Product not found</p>"

@app.route("/products_json")
def products_json():
    products_list = Devices.parse_products_file()
    devices_dicts = []
    for device in products_list:
        devices_dicts.append(device.make_dictionary())
    return jsonify(devices_dicts)

@app.route("/cart")
def cartPage():
    html = getHtml("cart")
    return html

@app.route("/product", methods=["GET"])
def productPage():
    return Cart.productDetails(logged_in=False)
    
@app.route("/productLoggedIn", methods=["GET"])
def productLoggedInPage():
    return Cart.productDetails(logged_in=True)