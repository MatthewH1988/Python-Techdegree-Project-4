import sys
import csv
import datetime
from models import engine, session, Base, Product


def menu():
    while True:
        print('''
        INVENTORY DATABASE
        \rv) View the details of a product
        \ra) Add a new product
        \rb) Make a backup of the database
        \re) Exit''')
        choice = input("What would you like to do? ").lower()
        if choice in ["v", "a", "b", "e"]:
            return choice
        else:
            input("This input is invalid. Press enter to try again.")


def clean_price(price_str):
    try:
        cleaned_price = int(float(price_str.replace("$", ""))*100)
    except ValueError:
        print("This input is invalid. Press try again. ")
    else:
        return cleaned_price


def clean_date(date_str):
    try:
        datetime_obj = datetime.datetime.strptime(date_str, "%m/%d/%Y")
    except ValueError:
        input("This input is invalid. Press enter to try again. ")
    else:
         return datetime_obj


def clean_quantity(quantity_str):
    try:
        quantity_clean = int(quantity_str)
    except ValueError:
        input("This input is invalid. Press enter to try again. ")
        return
    else:
        return quantity_clean


def clean_id(id_str):
    id_options = []
    for product in session.query(Product):
        id_options.append(product.product_id)
    try:
        id_choice = int(id_str)
    except ValueError:
        input("This input is invalid. Press enter to try again. ")
        return
    else:
        if id_choice in id_options:
            return id_choice
        else:
            input(f'''
                  \rOptions: {id_options}
                  \rPress enter to try again.''')
            return


def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            if product_in_db == None:
                name = row[0]
                price = clean_price(row[1])
                quantity = clean_quantity(row[2])
                date = clean_date(row[3])
                the_product = Product(product_name=name,product_price=price,product_quantity=quantity,date_updated=date)
                session.add(the_product)
            session.commit()


def app():
    while True:
        choice = menu()
        if choice == "v":
            id_error = True
            while id_error:
                id_choice = input("Please enter the Product ID: ")
                id_choice = clean_id(id_choice)
                if type(id_choice) == int:
                    id_error = False
                    the_product = session.query(Product).filter(Product.product_id==id_choice).one_or_none()
                    print(f'''
                         \rName: {the_product.product_name}
                         \rPrice: {the_product.product_price}
                         \rQuantity: {the_product.product_quantity}
                         \rDate: {the_product.date_updated}
                        ''')
        elif choice == "a":
            name  = input("What is the name of the product you'd like to add? ")
            price_error = True
            while price_error:
                price = input('What is the price of the product? Example: $4.27 ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            quantity_error = True
            while quantity_error:
                quantity = input("How many of the product are there? ")
                quantity = clean_quantity(quantity)
                if type(quantity) == int:
                    quantity_error = False
            date_error = True
            while date_error:
                date = input("What is the date updated?(Example: 11/1/2018) ")
                date = clean_date(date)
                if isinstance(date, datetime.date):
                    date_error = False
            new_product = Product(product_name=name, product_price=price, product_quantity=quantity, date_updated=date)
            session.add(new_product)
            session.commit()
            print("Product added successfully!")
        elif choice == "b":
            with open('backup.csv', 'w', newline='') as csvfile: 
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(["Name", "Price", "Quantity", "Date"])
                for product in session.query(Product):
                    csvwriter.writerow([
                        product.product_name,
                        product.product_price,
                        product.product_quantity,
                        product.date_updated,
                        ])
                print("Backup was successful")
        elif choice == "e":
            print("Thank you! Goodbye!")
            sys.exit()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv()
    app()
