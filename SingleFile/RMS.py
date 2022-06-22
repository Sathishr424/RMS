import sys, os, datetime

# MAIN_PATH = os.path.join(os.getcwd(), "data_files", "files_HDlevel")
MAIN_PATH = os.getcwd()

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
            return False, self.get_stock()
        return True, self.get_stock()

    def update_stock(self, stock): 
        self.stock = self.stock - stock

    def display_info(self):
        return (f"{self.ID}, {self.name}, {self.price}, {self.stock}")

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
        price = 0
        row_length = 20
        print("-" * row_length)
        for p in range(len(self.products)):
            # if self.products[p].get_ID()[0] == 'B':
            #     for b in self.products[p].get_products():
            #         price += b.get_price() * self.qtys[p]
            #         print(f"{self.customer_name} purchases {self.qtys[p]} x {b.get_name()}.")
            #         print("Unit price:" + " " * (row_length - len("Unit price")) + str(b.get_price()) + " (AUD)")
            # else:
            price += float(self.products[p].get_price()) * self.qtys[p]
            print(f"{self.customer_name} purchases {self.qtys[p]} x {self.products[p].get_name()}.")
            print("Unit price:" + (" " * (row_length - len("Unit price"))) + str(float(self.products[p].get_price())) + " (AUD)")
        if self.customer.get_ID()[0] == 'V' and self.new_member:
            print("Membership price:" + (" " * (row_length - len("Membership price"))) + "200.0 (AUD)")
        print(f"{self.customer_name} gets a discount of {self.customer.get_discount(price)[0] * 100} %.")
        print("Total price:" + (" " * (row_length - len("Total price"))) + str(self.customer.get_discount(price)[1] + (200 if self.new_member and self.customer.get_ID()[0] == 'V' else 0)) + " (AUD)")
        print("-" * row_length)
    
    def update_product_stock(self):
        for p in range(len(self.products)):
            self.products[p].update_stock(self.qtys[p])
    
    def update_customer_value(self):
        price = 0
        for p in range(len(self.products)):
            price += float(self.products[p].get_price()) * self.qtys[p]
        self.customer.update_value(price, 200 if self.new_member and self.customer.get_ID()[0] == 'V' else 0)
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
            if len(str(p.get_price())) <= 0 or float(p.get_price()) <= 0: return 0
            price += float(p.get_price())
        return round(price * 0.80, 2)
    
    def get_ID(self): return self.ID

    def get_name(self): return self.name

    def get_stock(self): 
        return self.stock

    def check_stock(self, qty):
        for p in self.products:
            if not p.check_stock(qty)[0]:
                return False, p.get_stock()
        if self.get_stock() - qty < 0:
            return False, self.get_stock()
        return True, self.get_stock()

    def get_products(self): return self.products

    def update_stock(self, stock):
        self.stock = self.stock - stock
        for p in self.products:
            p.update_stock(stock)

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
    
    def getThresholdLimit(self): return self.threshold_limit

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
                customer = Customer(self.getNextCustomerID(member), name, 0, 0.10 if member == 'V' else 0.05, self.threshold_limit)
                self.add_customer(customer)
            else:
                customer = Customer(self.getNextCustomerID('C'), name, 0, 0)
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
        if not os.path.exists(self.o_path) or len(self.o_path) <= 0:
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
                    if customer == None: 
                        print(str(o[0]) + " customer not found! Cannot load the order file. Run as if there is no order previously.")
                        self.o_path = ""
                        return []
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
            self.o_path = ""
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
        try:
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
                            products_bundle.append(product)
                        self.bundles.append(Bundle(p[0].strip(), p[1].strip(), int(p[-1].strip()), products_bundle))
                    else:
                        if len(p) < 4 or len(p) > 4 or p[0][0] not in ['P', 'B'] or not p[0][1:].isdigit() or any(i.isdigit() for i in p[1]) or not p[3].replace('.','').replace('-','').isdigit():
                            print("Something went wrong with the products.txt file. Exiting the program...")
                            sys.exit()
                        self.products.append(Product(p[0].strip(), p[1].strip(), (p[2].strip()), int(p[3].strip())))
        except Exception as e:
            # print(e)
            print("Something went wrong with the products.txt file. Exiting the program...")
            sys.exit() 
    
    def getMaxLenCustomers(self):
        ret = [0, 0, 0, 0, 0]
        for c in range(len(self.customers)):
            if len(self.customers[c].get_ID()) > ret[0]:
                ret[0] = len(self.customers[c].get_ID())
            if len(self.customers[c].get_name()) > ret[1]:
                ret[1] = len(self.customers[c].get_name())
            if len(str(self.customers[c].get_discount_rate())) > ret[2]:
                ret[2] = len(str(self.customers[c].get_discount_rate()))
            if len(str(self.customers[c].get_value())) > ret[3]:
                ret[3] = len(str(self.customers[c].get_value()))
            if len(str(self.customers[c].get_threshold())) > ret[4]:
                ret[4] = len(str(self.customers[c].get_threshold()))
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
        if len("Threshold") > maxLen[4]:
            maxLen[4] = len("Threshold")
        head = "| ID " + " " * (maxLen[0] - len("ID")) + "|" + " Name " + " " * (maxLen[1] - len("Name")) + "|" + " Discount Rate " + " " * (maxLen[2] - len("Discount Rate")) + "|" + " Value " + " " * (maxLen[3] - len("Value")) + "|" + " Threshold " + " " * (maxLen[4] - len("Threshold")) + "|"
        print("-" * len(head))
        print(head)
        print("-" * len(head))
        if customer == None:
            for c in self.customers:
                prints.append("| " + (str(c.get_ID()) + " " * (maxLen[0] - len(c.get_ID())) + " | " + str(c.get_name()) + " " * (maxLen[1] - len(c.get_name())) + " | " + str(c.get_discount_rate()) + " " * (maxLen[2] - len(str(c.get_discount_rate()))) + " | " + str(c.get_value()) + " " * (maxLen[3] - len(str(c.get_value()))) + " | " + str(c.get_threshold()) + " " * (maxLen[4] - len(str(c.get_threshold()))) + " | "))
        else:
            c = customer
            prints.append("| " + (str(c.get_ID()) + " " * (maxLen[0] - len(c.get_ID())) + " | " + str(c.get_name()) + " " * (maxLen[1] - len(c.get_name())) + " | " + str(c.get_discount_rate()) + " " * (maxLen[2] - len(str(c.get_discount_rate()))) + " | " + str(c.get_value()) + " " * (maxLen[3] - len(str(c.get_value()))) + " | " + str(c.get_threshold()) + " " * (maxLen[4] - len(str(c.get_threshold()))) + " | "))
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

# print(MAIN_PATH)
class Operations:
    def __init__(self, customers_path=os.path.join(MAIN_PATH, "customers.txt"), products_path=os.path.join(MAIN_PATH, "products.txt"), orders_path=os.path.join(MAIN_PATH, "orders.txt")):
        self.records = Records(customers_path, products_path, orders_path)
        # self.records.list_customers()
        # self.records.list_products()
        self.run()
    
    def init_screen(self):
        print("#######################################################################")
        print("1: Place an order")
        print("2: Display existing customers")
        print("3: Display existing products")
        print("4: Adjust the discount rates of a VIP member")
        print("5: Adjust the threshold limit of all VIP members")
        print("6: Display all orders")
        print("7: Display all orders of a customer")
        print("8: Summarize all orders")
        print("9: Reveal the most valuable customer")
        print("10: Reveal the most popular product")
        print("0: Exit the program")
        print("#######################################################################\n\n")
    
    def ask_options(self, ques, options, msg):
        inp = input(ques).upper()
        if inp not in options:
            print(msg)
            return self.ask_options(ques, options, msg)
        return inp

    def ask(self, ques, is_integer, msg, limit=0):
        inp = input(ques)
        if is_integer:
            if inp.isdigit():
                if int(inp) < limit:
                    print(msg)
                    return self.ask(ques, is_integer, msg)
                return int(inp)
            else:
                print(msg)
                return self.ask(ques, is_integer, msg)
        else:
            return inp
    
    def askFloat(self, ques, msg, limit=0):
        inp = input(ques)
        if inp.replace('.','').isdigit():
            inp = float(inp)
            if inp < limit:
                print(msg)
                return self.askFloat(ques, msg)
            else:
                return inp
        else:
            print(msg)
            return self.askFloat(ques, msg)
    
    def adjustDiscountVIP(self):
        customer = self.records.find_customer(self.ask("Please enter the name or ID of the VIP member:\n", False, ""))
        if customer == None or customer.get_ID()[0] != 'V':
            print("Invalid customer!")
        else:
            dr = self.askFloat("Please enter the new discount rate for this VIP customer:\n", "Please enter only Non-Negative number..\n")
            customer.set_rate(dr)
            print("Discount rate changed successfully for this VIP member..\n")
            input("Please enter to continue...")
        
    def adjustThresholdLimit(self):
        tl = self.askFloat("Please enter the new threshold limit for all the VIP Members:\n", "Please enter only Non-Negative number and larger than 0..\n", 1)
        self.records.changeDefaultThresholdLimit(tl)
        print("Threshold limit was changed successfully..\n")
        input("Please enter to continue...")
    
    def displayAllOrders(self):
        print("\n" + "-" * 70)
        for o in self.records.orders:
            print(o.display_info())
        print("-" * 70 + "\n")
    
    def displayAllOrdersOfACustomer(self):
        customer = self.records.find_customer(self.ask("Please enter the name or ID of the customer:\n", False, ""))
        if customer == None:
            print("Invalid customer!")
        else:
            print("\n" + "-" * 70)
            for o in customer.orders:
                if o.check_customer(customer.get_ID()):
                    print(o.display_info())
            print("-" * 70 + "\n")

    def run(self):
        while True:
            self.init_screen()
            inp = self.ask("Choose an option: ", True, "Please enter a correct option from above options.")
            if inp == 0:
                self.records.save_everything()
                sys.exit()
            elif inp == 1:
                self.order()
            elif inp == 2:
                self.records.list_customers()
                input("Please enter to continue...")
            elif inp == 3:
                self.records.list_products()
                input("Please enter to continue...")
            elif inp == 4:
                self.adjustDiscountVIP()
            elif inp == 5:
                self.adjustThresholdLimit()
            elif inp == 6:
                self.displayAllOrders()
                input("Please enter to continue...")
            elif inp == 7:
                self.displayAllOrdersOfACustomer()
                input("Please enter to continue...")
            elif inp == 8:
                # self.records.list_products()
                # self.displayAllOrders()
                self.records.summarizeAllOrders()
                input("Please enter to continue...")
            elif inp == 9:
                self.records.display_most_valuable_customer()
                input("Please enter to continue...")
            elif inp == 10:
                self.records.display_most_popular_product()
                input("Please enter to continue...")
            print("\n\n")
    
    def order_products(self, name, products, qtys):
        product = self.records.find_product(self.ask("\nEnter the product [enter a valid product only, e.g. shirt, towel, oven, kettle]:\n", False, ""))
        while product == None:
            print("\nProduct not found! Please enter the product that was in the stock.\n")
            product = self.records.find_product(self.ask("\nEnter the product [enter a valid product only, e.g. shirt, towel, oven, kettle]:\n", False, ""))
        if len(str(product.get_price())) <= 0 or float(product.get_price()) <= 0:
            print("Can't order this product. This product price is not valid..\n")
            ques = self.ask_options("\nDoes the customer wants to order more products? [e.g Y or N]:\n", ['Y', 'N'], '\nPlease enter only Y[yes] or N[no].')
            if ques == 'Y':
                return self.order_products(name, products, qtys)
            elif ques == 'N':
                return products, qtys
        if product.get_stock() <= 0 or product.check_stock(1)[1] <= 0:
            print("\nSorry this product was currently not in stock..\n")
            ques = self.ask_options("\nDoes the customer wants to order more products? [e.g Y or N]:\n", ['Y', 'N'], '\nPlease enter only Y[yes] or N[no].')
            if ques == 'Y':
                return self.order_products(name, products, qtys)
            elif ques == 'N':
                return products, qtys
        qty = self.ask("\nEnter the product quantity [enter a positive integer only, e.g. 1, 2, 3]:\n", True, "Please enter a number larger than 0.", 1)
        if not product.check_stock(qty)[0]:
            while not product.check_stock(qty)[0]:
                print("\nProduct was not in stock for the mentioned quantity! Please enter the quantity of the product that was in the stock.\n")
                qty = self.ask("\nEnter the product quantity [enter a positive integer only, e.g. 1, 2, 3]:\n", True, "\nPlease enter a positive integer only.")
        products.append(product)
        qtys.append(qty)
        ques = self.ask_options("\nDoes the customer wants to order more products? [e.g Y or N]:\n", ['Y', 'N'], '\nPlease enter only Y[yes] or N[no].')
        if ques == 'Y':
            return self.order_products(name, products, qtys)
        elif ques == 'N':
            return products, qtys
    
    def order(self):
        name = self.ask("Enter the name of the customer [e.g. Huong]:\n", False, "")
        while any(char.isdigit() for char in name):
            print("\nCustomer name must not contain numbers..")
            name = self.ask("\nEnter the name of the customer [e.g. Huong]:\n", False, "")
        products, qtys = self.order_products(name, [], [])
        if qtys == -1 or len(products) <= 0:
            return
        self.records.add_order(name, products, qtys)
        input("Please enter to continue...")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        Operations()
    elif len(sys.argv) > 4 or len(sys.argv) < 3:
        print("Please only pass the 'customers.txt', 'products.txt' and if have also pass 'orders.txt' as the arguments in this order to run this program")
    else:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        try:
            arg3 = sys.argv[3]
        except:
            arg3 = ""
        Operations(arg1, arg2, arg3)