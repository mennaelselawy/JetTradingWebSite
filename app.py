import flask 
from flask import redirect, request,  url_for  
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
                return redirect(url_for('loggedInHomePage'))
        
        # login failed — show error
        failedLogging = getHtml("login")
        return failedLogging.replace("$$ERROR$$", "<p style='color:red;'>Login failed: Wrong email or password</p>")
    
    def updateUserInfo():
        

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
    return getHtml("profile")