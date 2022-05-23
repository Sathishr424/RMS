import sys, os, datetime

class Product:
    def __init__(self, ID, name, price, stock):
        self.ID = ID
        self.name = name
        self.price = price
        self.stock = int(stock)
    
    def get_ID(self): return self.ID

    def get_name(self): return self.name
    
    def get_price(self): return self.price

    def set_price(self, price): self.price = price
    
    def get_stock(self): return self.stock

    def check_stock(self, qty):
        if self.get_stock() - qty < 0:
            return False
        return True

    def update_stock(self, stock): 
        self.stock = self.stock - stock

    def display_info(self):
        return (f"{self.ID}, {self.name}, {self.price}, {self.stock}")