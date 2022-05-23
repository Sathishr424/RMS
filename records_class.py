from math import prod
import sys, os, datetime

from customer_class import Customer
from product_class import Product

class Order:
    def __init__(self, customer, products, qtys, date, new_member=False):
        self.customer = customer
        self.products = products
        self.qtys = qtys
        self.date = date.replace('-', '/')
        self.date = self.date[:self.date.find('.')] if self.date.find('.') != -1 else self.date
        self.customer_name = self.customer.get_name()
        self.new_member = new_member
    
    def check_customer(self, ID_name):
        if self.customer.get_name() == ID_name or self.customer.get_ID() == ID_name:
            return True
        return False
    
    def get_orders(self):
        ret = []
        for p in range(len(self.products)):
            ret.append([self.customer.get_name(), self.products[p].get_ID(), self.qtys[p]])
        return ret
    
    def order_placed(self):
        self.update_customer_value()
        self.update_product_stock()
        price = 200 if self.new_member and self.customer.get_ID()[0] == 'V' else 0
        row_length = 20
        print("-" * row_length)
        for p in range(len(self.products)):
            # if self.products[p].get_ID()[0] == 'B':
            #     for b in self.products[p].get_products():
            #         price += b.get_price() * self.qtys[p]
            #         print(f"{self.customer_name} purchases {self.qtys[p]} x {b.get_name()}.")
            #         print("Unit price:" + " " * (row_length - len("Unit price")) + str(b.get_price()) + " (AUD)")
            # else:
            price += self.products[p].get_price() * self.qtys[p]
            print(f"{self.customer_name} purchases {self.qtys[p]} x {self.products[p].get_name()}.")
            print("Unit price:" + (" " * (row_length - len("Unit price"))) + str(self.products[p].get_price()) + " (AUD)")
        if self.customer.get_ID()[0] == 'V' and self.new_member:
            print("Membership price:" + (" " * (row_length - len("Membership price"))) + "200.0 (AUD)")
        
        print(f"{self.customer_name} gets a discount of {self.customer.get_discount(price)[0] * 100} %.")
        print("Total price:" + (" " * (row_length - len("Total price"))) + str(self.customer.get_discount(price)[1]) + " (AUD)")
        print("-" * row_length)
    
    def update_product_stock(self):
        for p in range(len(self.products)):
            self.products[p].update_stock(self.qtys[p])
    
    def update_customer_value(self):
        price = 200 if self.new_member and self.customer.get_ID()[0] == 'V' else 0
        for p in range(len(self.products)):
            price += self.products[p].get_price() * self.qtys[p]
        self.customer.update_value(price)
        # if price > 1000 and self.customer.get_name()[0] == 'V':
        #     price = price - (price * (self.customer.get_discount_rate() + 0.05))
        # else: price = price - (price * self.customer.get_discount_rate())
        # self.customer.set_value(self.customer.get_value() + price)
    
    def display_info(self):
        # print([str(str(self.products[p].get_name()) + ", " + str(self.qtys[p])) for p in range(len(self.products))])
        return (f"{self.customer_name}, " + (", ".join([str(str(self.products[p].get_name()) + ", " + str(self.qtys[p])) for p in range(len(self.products))])) + ", " + str(self.date))

class Bundle:
    def __init__(self, ID, name, stock, products):
        self.ID = ID
        self.name = name
        self.stock = int(stock)
        self.products = products
    
    def get_price(self):
        price = 0
        for p in self.products:
            price += p.get_price()
        return price
    
    def get_ID(self): return self.ID

    def get_name(self): return self.name

    def get_stock(self): return self.stock

    def check_stock(self, qty):
        # for p in self.products:
        #     if not p.check_stock(qty):
        #         return False
        # return True
        if self.get_stock() - qty < 0:
            return False
        return True

    def get_products(self): return self.products

    def update_stock(self, stock):
        # for p in self.products:
        #     p.update_stock(stock)
        self.stock = self.stock - stock

    def display_info(self):
        return (f"{self.ID}, {self.name}, " + (', '.join([p.get_ID() for p in self.products])) + ", " + str(self.stock))

class Records:
    def __init__(self, c_path, p_path, o_path):
        self.c_path = c_path
        self.p_path = p_path
        self.o_path = o_path
        self.products = []
        self.customers = []
        self.bundles = []
        self.orders = []
        self.threshold_limit = 1000
        self.read_customers()
        self.read_products()
        self.read_orders()
    
    def changeDefaultThresholdLimit(self, tl):
        self.threshold_limit = tl
        for c in self.customers:
            if c.get_ID()[0] == 'V':
                c.set_threshold(tl)

    def ask_options(self, ques, options, msg):
        inp = input(ques).upper()
        if inp not in options:
            print(msg)
            return self.ask_options(ques, options, msg)
        return inp

    def add_customer(self, customer):
        self.customers.append(customer)

    def add_product(self, product):
        self.products.append(product)
    
    def add_order(self, name, products, qtys):
        customer = self.find_customer(name)
        new_member = False
        if customer == None:
            ques = self.ask_options("\nThis is a new customer, Does this customer want to have a membership [enter y or b]:\n", ['Y', 'N'], '\nPlease enter only Y[Yes] or N[No]..')
            new_member = True
            if ques.lower() == 'y':
                member = self.ask_options("\nWhat kind of membership the customer wants?[enter M or V]:\n", ['M', 'V'], "\nPlease enter only M[Member] or V[VIP Member].").upper()
                customer = Customer(self.getNextCustomerID(member), name, 0 if member == 'V' else 0, 0.10, self.threshold_limit)
                self.add_customer(customer)
            else:
                customer = Customer(self.getNextCustomerID('C'), name, 0, 0.05)
                self.add_customer(customer)
        order = Order(customer, products, qtys, str(datetime.datetime.now()), new_member)
        order.order_placed()
        self.orders.append(order)
        customer.add_order(order)
    
    def change_product_stock(self, ID_name, qty):
        p = self.find_product(ID_name)
        p.update_stock(qty)

    def update_customer_value(self, ID_name, value):
        self.find_customer(ID_name).set_value(value)
    
    def find_customer(self, ID_name):
        for c in self.customers:
            if c.get_ID() == ID_name or c.get_name() == ID_name:
                return c
        return None

    def find_product(self, ID_name):
        for p in self.products:
            if p.get_ID() == ID_name or p.get_name() == ID_name:
                return p
        return self.find_bundle(ID_name)

    def find_bundle(self, ID_name):
        for b in self.bundles:
            if b.get_ID() == ID_name or b.get_name() == ID_name:
                return b
        return None
    
    def save_everything(self):
        with open(self.c_path, 'w') as file:
            data = ""
            for c in self.customers:
                data += f"{c.get_ID()}, {c.get_name()}, {c.get_discount_rate()}, {c.get_value()}\n"
            data = data[:-1]
            file.write(data)
        with open(self.p_path, 'w') as file:
            data = ""
            for p in self.products:
                data += str(p.display_info()) + "\n"
            for b in self.bundles:
                data += str(b.display_info()) + "\n"
            data = data[:-1]
            file.write(data)
        if not os.path.exists(self.o_path):
            self.o_path = os.path.join(os.getcwd(), "orders.txt")
        with open(self.o_path, 'w') as file:
            data = ""
            for o in self.orders:
                data += str(o.display_info()) + "\n"
            data = data[:-1]
            file.write(data)
        print("Saved successfully!")
    
    def read_orders(self):
        try:
            with open(self.o_path, 'r') as file:
                data = file.readlines()
                orders = []
                for o in data:
                    o = o.replace('\n', '').split(',')
                    o = [i.strip() for i in o]
                    customer = self.find_customer(o[0])
                    if customer == None: return []
                    products = []
                    qtys = []
                    for p in range(1, len(o[:-1]), 2):
                        product = self.find_product(o[p])
                        products.append(product)
                        qtys.append(int(o[p+1]))
                    order = Order(customer, products, qtys, str(o[-1]))
                    orders.append(order)
                    customer.add_order(order)
                self.orders = orders
        except Exception as e:
            print("Cannot load the order file. Run as if there is no order previously.")
            return []

    def read_customers(self):
        try:
            with open(self.c_path, 'r') as file:
                data = file.readlines()
                for c in data:
                    c = c.replace('\n', '').split(',')
                    c = [i.strip() for i in c]
                    c[2] = c[2].replace(' ', '')
                    c[3] = c[3].replace(' ', '')
                    if len(c) < 4 or len(c) > 4 or c[0][0] not in ['C', 'M', 'V'] or not c[0][1:].isdigit() or any(i.isdigit() for i in c[1]) or not c[2].replace('.','').isdigit() or not c[3].replace('.','').isdigit():
                        print("Something wrong with the customer.txt file.. Exiting the program.")
                        sys.exit()
                    self.customers.append(Customer(c[0].strip(), c[1].strip(), float(c[3].strip()), float(c[2].strip())))
        except:
            print("Something wrong with the customer.txt file.. Exiting the program.")
            sys.exit()

    def read_products(self):
        # try:
        with open(self.p_path, 'r') as file:
            data = file.readlines()
            for p in data:
                p = p.strip().replace('\n', '').split(',')
                p = [i.strip() for i in p]
                p[2] = p[2].replace(' ', '')
                p[3] = p[3].replace(' ', '')
                if p[0][0] == 'B':
                    products_bundle = []
                    for b in p[2:-1]:
                        product = self.find_product(b)
                        products_bundle.append(Product(b, product.get_name(), product.get_price(), p[-1]))
                    self.bundles.append(Bundle(p[0].strip(), p[1].strip(), int(p[-1].strip()), products_bundle))
                else:
                    if len(p) < 4 or len(p) > 4 or p[0][0] not in ['P', 'B'] or not p[0][1:].isdigit() or any(i.isdigit() for i in p[1]) or not p[2].replace('.','').isdigit() or not p[3].replace('.','').isdigit():
                        print("Something went wrong with the products.txt file. Exiting the program...")
                        sys.exit()
                    self.products.append(Product(p[0].strip(), p[1].strip(), float(p[2].strip()), int(p[3].strip())))
        # except Exception as e:
        #     print(e)
        #     print("Something went wrong with the products.txt file. Exiting the program...")
        #     sys.exit() 
    
    def getMaxLenCustomers(self):
        ret = [0, 0, 0, 0]
        for c in range(len(self.customers)):
            if len(self.customers[c].get_ID()) > ret[0]:
                ret[0] = len(self.customers[c].get_ID())
            if len(self.customers[c].get_name()) > ret[1]:
                ret[1] = len(self.customers[c].get_name())
            if len(str(self.customers[c].get_discount_rate())) > ret[2]:
                ret[2] = len(str(self.customers[c].get_discount_rate()))
            if len(str(self.customers[c].get_value())) > ret[3]:
                ret[3] = len(str(self.customers[c].get_value()))
        return ret
    
    def getNextCustomerID(self, member):
        last = 0
        for c in self.customers:
            id = c.get_ID()
            if id[0] == member and int(id[1:]) > last:
                last = int(id[1:])
        return member + str(last + 1)
    
    def display_most_valuable_customer(self):
        max_spend = 0
        customer = None
        for c in self.customers:
            if c.get_value() > max_spend:
                max_spend = c.get_value()
                customer = c
        if customer:
            self.list_customers(customer)
        else:
            print("No customer found!")
    
    def display_most_popular_product(self):
        data = ""
        for c in self.orders:
            for o in c.get_orders():
                data += " " + str(o[1])
        max_num = 0
        product = None
        for p in self.products:
            if data.count(p.get_ID()) > max_num:
                max_num = data.count(p.get_ID())
                product = p
        if product != None:
            print("\n")
            print(str(max_num) + " times this product has been ordered!")
            print("-" * 35)
            print(product.display_info())
            print("-" * 35)
        else:
            print("No data was found!")

    def list_customers(self, customer=None):
        maxLen = self.getMaxLenCustomers()
        prints = []
        if len("name") > maxLen[1]:
            maxLen[1] = len("name") 
        if len("Discount Rate") > maxLen[2]:
            maxLen[2] = len("Discount Rate")
        if len("Value") > maxLen[3]:
            maxLen[3] = len("Value")
        head = "| ID " + " " * (maxLen[0] - len("ID")) + "|" + " Name " + " " * (maxLen[1] - len("Name")) + "|" + " Discount Rate " + " " * (maxLen[2] - len("Discount Rate")) + "|" + " Value " + " " * (maxLen[3] - len("Value")) + "|"
        print("-" * len(head))
        print(head)
        print("-" * len(head))
        if customer == None:
            for c in self.customers:
                prints.append("| " + (str(c.get_ID()) + " " * (maxLen[0] - len(c.get_ID())) + " | " + str(c.get_name()) + " " * (maxLen[1] - len(c.get_name())) + " | " + str(c.get_discount_rate()) + " " * (maxLen[2] - len(str(c.get_discount_rate()))) + " | " + str(c.get_value()) + " " * (maxLen[3] - len(str(c.get_value()))) + " | "))
        else:
            c = customer
            prints.append("| " + (str(c.get_ID()) + " " * (maxLen[0] - len(c.get_ID())) + " | " + str(c.get_name()) + " " * (maxLen[1] - len(c.get_name())) + " | " + str(c.get_discount_rate()) + " " * (maxLen[2] - len(str(c.get_discount_rate()))) + " | " + str(c.get_value()) + " " * (maxLen[3] - len(str(c.get_value()))) + " | "))
        [print(p) for p in prints]
        print("-" * len(head))

    def list_products(self):
        print("-" * 35)
        for c in self.products:
            print(c.display_info())
        for b in self.bundles:
            print(b.display_info())
        print("-" * 35)
    
    def summarizeAllOrders(self):
        data = []
        for c in self.orders:
            data += (c.get_orders())
        # print(data)
        p_ids = []
        max_rows = [0] * (len(self.products) + len(self.bundles) + 1)
        tot_qty = [[0,0]] * (len(self.products) + len(self.bundles))
        for p in range(len(self.products)):
            p_ids.append(self.products[p].get_ID())
            if len(p_ids[-1]) > max_rows[p+1]: max_rows[p+1] = len(p_ids[-1])
        for b in range(len(self.bundles)):
            p_ids.append(self.bundles[b].get_ID())
            if len(p_ids[-1]) > max_rows[len(self.products)+b+1]: max_rows[len(self.products)+b+1] = len(p_ids[-1])
        # print(p_ids)
        customer_data = []
        for c in self.customers:
            name = c.get_name()
            if len(name) > max_rows[0]: max_rows[0] = len(name)
            p_data = []
            for p in range(len(p_ids)):
                qty = 0
                order_num = 0
                for d in data:
                    if d[0] == name and d[1] == p_ids[p]:
                        qty += d[2]
                        order_num += 1
                if len(str(qty)) > max_rows[p+1]: max_rows[p+1] = len(str(qty))
                tot_qty[p] = [tot_qty[p][0]+qty, tot_qty[p][1]+order_num]
                p_data.append([qty, order_num])
            customer_data.append([name, p_data])
        # print(customer_data)
        # print(tot_qty)
        if len("OrderNum") > max_rows[0]:
            max_rows[0] = len("OrderNum")
        max_rows[0] += 2
        head = (" " * max_rows[0]) + " ".join([str(p_ids[p]) + (" " * (max_rows[p+1] - len(str(p_ids[p])))) for p in range(len(p_ids))])
        print("-" * len(head))
        print(head)
        print("-" * len(head))
        for d in customer_data:
            print((d[0] + (" " * (max_rows[0] - len(d[0])))) + " ".join([str(d[1][p][0]) + (" " * (max_rows[p+1] - len(str(d[1][p][0])))) for p in range(len(d[1]))]))
        
        print("-" * len(head))
        print("OrderNum" + (" " * (max_rows[0] - len("OrderNum"))) + " ".join(str(tot_qty[o][1]) + " " * (max_rows[o+1] - len(str(tot_qty[o][1]))) for o in range(len(tot_qty))))
        print("OrderQty" + (" " * (max_rows[0] - len("OrderQty"))) + " ".join(str(tot_qty[o][0]) + " " * (max_rows[o+1] - len(str(tot_qty[o][0]))) for o in range(len(tot_qty))))
        print("-" * len(head))

                
        
