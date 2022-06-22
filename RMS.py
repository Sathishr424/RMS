import sys, os, datetime
from records_class import Records

# MAIN_PATH = os.path.join(os.getcwd(), "data_files", "files_HDlevel")
MAIN_PATH = os.getcwd()
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
        qty = self.ask("\nEnter the product quantity [enter a positive integer only, e.g. 1, 2, 3]:\n", True, "Please enter a number larger than 0.", 1)
        if not product.check_stock(qty):
            while not product.check_stock(qty):
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
        print("Please only pass the 'customers.txt', 'products.txt' and if have also pass 'orders.txt' as the argument to run this program")
    else:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        try:
            arg3 = sys.argv[3]
        except:
            arg3 = ""
        Operations(arg1, arg2, arg3)