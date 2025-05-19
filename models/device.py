from urllib.parse import quote
from flask import request
from utils.helpers import getHtml
                                            
class Devices:
    def __init__(self, name, description, price, image , category):
        self.name = name
        self.description = description
        self.price = price
        self.image = image
        self.category = category

# used to: make each device dictionary to convert to JSON format if i want to deal with js so i will need it json
    def make_dictionary(self):
        dict={
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "image": self.image,
            "category": self.category,
        }
        return dict

# used to: parse the text files as lines to python devices objects of the class using constructor
# return: list to deal with html i use lists
    @staticmethod                               
    def parse_products_file():
        products =[]
        try:
            with open("data/products.txt", "r") as f:
                for line in f:
                    property = line.strip().split("|")
                    if len(property) == 5:
                        product = Devices(property[0], property[1], property[2], property[3], property[4])    
                        products.append(product)
        except(FileNotFoundError):
            products=[]
        return products
    
# i used the data- attribute so in javascript will get it by dataset.
    @staticmethod
    def display_devices_html(devices_list, show_cart_buttons=False, logged_in = False):
        html=""
        for device in devices_list: 
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