import sys, os, datetime

class Member:
    def __init__(self, name, discount_rate=0.05):
        self.discount_rate = discount_rate
        self.name = name
    
    def getDiscountRate(self):
        return self.get_discount(0)[0]

    def get_discount(self, price):
        return (self.discount_rate, round(price * (1 - self.discount_rate), 2))
    
    def set_rate(self, rate):
        self.discount_rate = rate
    
    def display_info(self):
        return f"Name: {self.name} | Member | Discount rate: {self.discount_rate}"

class VIPMember:
    def __init__(self, name, threshold=1000, discount_rate=0.10):
        self.discount_rate = discount_rate
        self.threshold = threshold
        self.name = name
    
    def getDiscountRate(self):
        return self.get_discount(0)[0]
    
    def set_threshold(self, threshold): self.threshold = threshold
    
    def get_threshold(self): return self.threshold

    def set_rate(self, rate): self.discount_rate = rate

    def get_discount(self, price):
        if price > self.threshold:
            return (round(self.discount_rate + 0.05, 2), round(price * (1 - (self.discount_rate+0.05)), 2))
        return (round(self.discount_rate, 2), round(price * (1 - self.discount_rate), 2))

    def display_info(self):
        return f"Name: {self.name} | VIP Member | Discount rate: {self.discount_rate}"

class Customer:
    def __init__(self, ID, name, value, discount_rate=0, threshold=1000):
        self.ID = ID
        self.name = name
        self.discount_rate = float(discount_rate)
        self.value = value
        self.type = self.ID[0]
        self.orders = []
        self.member = Member(name, self.discount_rate) if self.type == 'M' else (VIPMember(name, threshold, self.discount_rate) if self.type == 'V' else None)

    def add_order(self, order):
        self.orders.append(order)
    
    def get_ID(self): return self.ID

    def get_name(self): return self.name

    def set_threshold(self, threshold): 
        if self.member == None:
            pass
        else:
            self.member.set_threshold(threshold)
    
    def get_threshold(self):
        if self.get_ID()[0] == 'V': return self.member.get_threshold()
        return '-'

    def get_discount(self, price):
        if self.member == None:
            return (round(self.discount_rate, 2), round(price * (1 - self.discount_rate), 2))
        else:
            return self.member.get_discount(price)

    def get_discount_rate(self): 
        return self.get_discount(0)[0]

    def update_value(self, price, VIPMembershipCharge=0):
        self.set_value(self.get_value() + self.get_discount(price)[1] + VIPMembershipCharge)

    def get_value(self): return round(self.value, 3)

    def set_value(self, value): self.value = value

    def set_rate(self, dr):
        if self.member == None:
            self.discount_rate = dr
        else:
            self.member.set_rate(dr)

    def display_info(self):
        return f"Name: {self.name} | Customers | Discount rate: {self.get_discount_rate()}"