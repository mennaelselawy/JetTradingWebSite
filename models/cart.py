from flask import request
from utils.helpers import getHtml
from models.device import Devices
                                               #CART
class Cart:
    def __init__(self):
        self.items=[]
    
    def add_product(self, product):
        self.items.append(product)
    def remove_product(self, product_name):
        new_items=[]
        for item in self.items:
            if item.name != product_name:
                new_items.append(item)
        self.items = new_items
    def make_dictionary(self):
        dictionaries = []
        for item in self.items:
            dictionaries.append(item.make_dictionary())
        return dictionaries
    def clear_cart(self):
        self.items = []
    def get_items(self):
        return self.items
    