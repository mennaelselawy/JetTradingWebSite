
# Jet Trading E-Commerce Website

This is a full-stack web application for electronics company, **Jet Trading**, that sells laptops, printers, and tablets. The website supports both guest and registered users, enabling a dynamic shopping experience.

## 🛍️ What Does It Do?

This website allows users to:

- 🖥️ **Browse available devices** by category (laptops, tablets, printers).

- ✅ **Sign up and log in** with validation for required fields and formats.

- 🛒 **Add devices to a cart**, which is available only to logged-in users.

- 🗑️ **Remove individual items from the cart** or **clear the entire cart**, using `sessionStorage`.

- 🔄 **Edit profile information** (username, password, address, phone) with validation for all fields:
  - Updated profile data is saved to the `users.json` file.
  - If the username is changed, the `localStorage` is automatically updated.

- 🔓 **Log out** at any time, which clears session and local storage safely.

- ❌ **Delete account permanently**, which removes the user from both the JSON file and browser `localStorage`.

- 🔍 **Filter/search products** by category or keyword dynamically.

- 💾 **Store cart data** per session using `sessionStorage`, so it clears on logout or tab close.

- 📦 **Load all product data** from a text file and display it dynamically using Python classes and HTML rendering.

- 🔐 **Secure password handling** via hashing.

- 🧪 **Input validation** is implemented in signup, login, and profile update forms to ensure clean, correct data.


### ✨ Unique Feature

- JavaScript-based cart using `sessionStorage`, giving each user a temporary session-based cart that clears on logout or tab close.
- Dynamic localStorage handling of logged-in users

---

## 🚀 Prerequisites

To run this project, make sure you have the following:

- Python 3 installed
- Flask installed:  
  ```bash 
  pip install Flask 

## 🧠 Project Checklist

- [x] It is available on GitHub.
- [x] It uses the **Flask** web framework.
- [x] It uses at least one module from the Python Standard Library other than `random`.  
  **Module name**: `urllib.parse.quote` (used to encode device names for URLs by replacing spaces with `%20`)

- [x] It contains at least one class written by you that has both properties and methods.  
  **First Class:**  
  - **File name**: `models/user.py`  
  - **Line number**: 7–139  
  - **Five properties**: `username`, `password` , `email`, `address`, `phone`
  - **Six instance methods**: `makeDictionary()`, `saveData()`, `getUserInfo()`, `fillProfileForm()`, `updateUserInfo()`, `deleteUser()`
  - **Two static methods**: `safeHash()`,`safeUnhash()`
  - **File and line numbers where used**: `app.py` and `routes.py`, multiple lines where users are read/written.
    
  **Second Class:**  
  - **File name**: `models/device.py`  
  - **Line number**: 4–130  
  - **Five properties**: `name`, `description`, `price`, `image`, `category` 
  - **One instance method**: `make_dictionary()`  
  - **Four static methods**: `parse_products_file()`,`display_devices_html()`, `devicesPageHtml()`, `productDetails()`
  - **File and line numbers where used**: `app.py` and `routes.py`, multiple lines where users are read/written.

- [x] It makes use of **JavaScript** in the front end and uses the **localStorage** and **sessionStorage** of the web browser.
- [x] It uses **modern JavaScript** (`let`, `const`, arrow functions).
- [x] It reads and writes to the **same file** (`users.json`) using Python, and also reads from a text file (`products.txt`).
- [x] It contains **conditional statements**.  
  **Example:**  
  - **File name**: `static/script.js`  
  - **Line number(s)**: 19-27-37-...  
    ```js
    if(cartItems){ displayCart(); }
    ```

- [x] It contains **loops**.  
  **Example:**  
  - **File name**: `static/script.js`  
  - **Line number(s)**: 111–152-234-282  
    ```js
    for (let i = 0; i < cartItems.length; i++) {
        // render cart item
    }
    ```

- [x] It lets the user enter a value in a text box (e.g., in the signup, login and profile forms).
- [x] This value is **processed by your back-end Python code**.
- [x] It **validates and handles wrong input gracefully** (all input fields are validated).
- [x] It is styled using custom **CSS** in `static/style.css`.
- [x] The code follows clean **style conventions**, uses proper comments, and avoids experimental or unused code.
- [x] All exercises are completed and pushed to **GitHub**.

## 📁 Project Structure

```text
project/
├── app.py                  # Main Flask app with routes
├── routes.py               # Additional helper functions
├── models/
│   ├── user.py             # User class
│   └── device.py           # Device class
├── utils/
│   └── helpers.py          # Utility function: getHtml()
├── templates/
│   ├── index.html
│   ├── loggedInHome.html
│   ├── devices.html
│   ├── devicesLoggedIn.html
│   ├── product.html
│   ├── productLoggedIn.html
│   ├── login.html
│   ├── signup.html
│   ├── profile.html
│   └── cart.html
├── static/
│   ├── style.css           # Custom CSS
│   └── script.js           # JavaScript for user/cart logic
├── data/
│   ├── users.json          # Stores registered users
│   └── products.txt        # Stores product details           
```

## 🧪 How to Run the App

1. Clone the repository:
   ```bash
   git clone https://github.com/mennaelselawy/JetTradingWebSite

2. Install Flask if you haven't already:
    ```bash
   pip install Flask
3. Run the Flask app:
   ```bash
   python app.py
4. Open your browser and go to:
   ```bash
   http://127.0.0.1:5000/

