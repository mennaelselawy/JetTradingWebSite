import flask 
from flask import redirect, request,  url_for ,jsonify, Response , Flask
import json

#import os
app = flask.Flask("app")

def getHtml(pageName):
    with open(pageName + ".html") as htmlPage:
        return htmlPage.read()
    # htmlPage = open(pageName + ".html")
    # pageContent = htmlPage.read()
    # htmlPage.close()
    # return pageContent

                                                        # USER
class User:
    def __init__(self):
        self.username = flask.request.form.get("username")    #flask-> module , request-> object , form -> property, get-> method 
        self.password = flask.request.form.get("password")
        self.email = flask.request.form.get("email")
        self.address = flask.request.form.get("address")
        self.phone = flask.request.form.get("phone")
    
    def makeDictionary(self):
        dict = {
            "username": self.username,
            "password": self.password,
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
        
        #CHECK THAT THE USER NOT ALREADY EXIST BY EMAIL
        if any(user["email"] == self.email for user in users) :
            failedSignUp = getHtml("signup")
            return failedSignUp.replace("$$ERROR$$", "<p style='color:red;'>Sign Up Failed: User already exists</p>")

        else:
            #append the new user: to add in the python list in memory not in the file
            users.append(self.makeDictionary())
            #to write the new user in the file
            with open("data/users.json", "w") as f:
                json.dump(users, f, indent=4)                #takes python object as user list and writes it as JSON formatted text into file SO reverse of json.load()
            return redirect(url_for("logInPage"))  # redirect after success
                    
    def check_login(self):
        try:
            with open("data/users.json" , "r") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users =[]
        for user in users:
            if (user["email"] == self.email) and (user["password"] == self.password):
                return redirect(url_for('loggedInHomePage', email=self.email))
        
        # login failed — show error
        failedLogging = getHtml("login")
        return failedLogging.replace("$$ERROR$$", "<p style='color:red;'>Login failed: Wrong email or password</p>")
    
    def updateUserInfo(self):
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
        successPage = getHtml("profile")
        return successPage.replace("$$ERROR$$", "<p style='color:green;'>User updated successfully</p>")
    
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
        # updated_users=[]
        # for user in users:
        #     if user["email"] != self.email:
        #         updated_users.append(user)
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
    user.saveData()
    return redirect(url_for('logIn'))

@app.route("/login" , methods=["GET"])
def logInPage():
    html = getHtml("login")
    return html.replace("$$ERROR$$" , "")

@app.route("/login" , methods=["POST"])
def logIn():
    user = User()
    return user.check_login()

@app.route("/loggedInHome" , methods=["GET"])
def loggedInHomePage():
    return getHtml("loggedInHome")


@app.route("/profile", methods=["GET"])
def profilePage():
    html = getHtml("profile")
    return html.replace("$$ERROR$$", "")
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
    def display_devices_html(devices_list, show_cart_buttons=False):
        html=""
        for device in devices_list: 
            # f """" = formatted string literals embed expressions directly into string literals using {}
            # i used the data- attribute so in javascript will get it by dataset.
            html += f""" 
                <div class="device-card">  
                    <img src="static/images/{device.image}" alt="{device.name}" class="device-img">
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

        
@app.route("/devices", methods=["GET"])
def devicesPage():
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

    devices_html = Devices.display_devices_html(filtered, show_cart_buttons=False)
    
    if not devices_html:
        devices_html = "<p class='no-results'>No devices found.</p>"
    
    html = getHtml("devices")
    final_html = html.replace("$$CATEGORY$$", heading).replace("$$DEVICES$$", devices_html)
    return final_html
  
    # devices_dicts = [device.make_dictionary() for device in devices]
    # devices_dicts = []
    # for device in devices:
    #     device_dict = device.make_dictionary()
    #     devices_dicts.append(device_dict)
    # return jsonify(devices_dicts)       #jsonify to convert the dict's to json format 


# @app.route("/devices", methods=["GET"])
# def category_devices():
#     devices = Devices.parse_products_file()
#     category = request.args.get('category').lower()
#     filtered_category =[]
#     for device in devices:
#         if device.category.lower() == category:
#             filtered_category.append(device)
#     devices_html = Devices.display_devices_html(filtered_category)
#     html=getHtml("devices")
#     final_html = html.replace("$$DEVICES$$", devices_html)
#     return final_html

@app.route("/devicesLoggedIn", methods=["GET"])
def devicesLoggedInPage():
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

    devices_html = Devices.display_devices_html(filtered, show_cart_buttons=True)
    if not devices_html:
        devices_html = "<p class='no-results'>No devices found.</p>"
    
    html = getHtml("devicesLoggedIn")
    final_html = html.replace("$$CATEGORY$$", heading).replace("$$DEVICES$$", devices_html)
    return final_html




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