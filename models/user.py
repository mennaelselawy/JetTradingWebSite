import json
from flask import request, redirect, url_for
from urllib.parse import quote
from utils.helpers import getHtml

                                                        # USER
class User:
    def __init__(self, formData = None):
            if formData is None:
                formData = request.form
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
