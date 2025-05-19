from flask import request, jsonify
import json
from models.user import User
from models.device import Devices
from utils.helpers import getHtml


def handleLogin():
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

def handleProfile():
    email = request.args.get("email")
    user = User().getUserInfo(email)
    if user:
        return User().fillProfileForm(user, "")
    else:
        return getHtml("login").replace("$$ERROR$$", "<p style='color:red;'>User not found</p>")
    
def handleProductsJson():
    products_list = Devices.parse_products_file()
    devices_dicts = []
    for device in products_list:
        devices_dicts.append(device.make_dictionary())
    return jsonify(devices_dicts)