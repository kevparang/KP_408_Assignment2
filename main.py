###
# Kevan Parang
# 2368828
# kparang@chapman.edu
# Database Management FA23S CPSC-408-02
# Assignment 2 - MySQL
##

import mysql.connector
import re

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    port="3306",
    password="change-me",
    database="cpsc"
)

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Define the database schema creation queries
create_products_table_query = """
CREATE TABLE IF NOT EXISTS Products (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    ProductName VARCHAR(255),
    SupplierID INT,
    Category VARCHAR(255),
    UnitPrice DECIMAL(10, 2),
    UnitsInStock INT,
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
);
"""

create_customers_table_query = """
CREATE TABLE IF NOT EXISTS Customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerName VARCHAR(255),
    ContactName VARCHAR(255),
    Address VARCHAR(255),
    City VARCHAR(255),
    PostalCode VARCHAR(10),
    Country VARCHAR(255)
);
"""

create_orders_table_query = """
CREATE TABLE IF NOT EXISTS Orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    ShipDate DATE,
    ShipAddress VARCHAR(255),
    ShipCity VARCHAR(255),
    ShipPostalCode VARCHAR(10),
    ShipCountry VARCHAR(255),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);
"""

create_order_details_table_query = """
CREATE TABLE IF NOT EXISTS OrderDetails (
    OrderDetailID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    UnitPrice DECIMAL(10, 2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
"""

create_suppliers_table_query = """
CREATE TABLE IF NOT EXISTS Suppliers (
    SupplierID INT AUTO_INCREMENT PRIMARY KEY,
    SupplierName VARCHAR(255),
    ContactName VARCHAR(255),
    Address VARCHAR(255),
    City VARCHAR(255),
    PostalCode VARCHAR(10),
    Country VARCHAR(255),
    Phone VARCHAR(20)
);
"""

# Execute the schema creation queries
cursor.execute(create_products_table_query)
conn.commit()

cursor.execute(create_customers_table_query)
conn.commit()

cursor.execute(create_orders_table_query)
conn.commit()

cursor.execute(create_order_details_table_query)
conn.commit()

cursor.execute(create_suppliers_table_query)
conn.commit()

# Define the stored procedure for adding a new order
add_order_procedure = """
CREATE PROCEDURE IF NOT EXISTS AddNewOrder(
    IN p_CustomerID INT,
    IN p_OrderDate DATE,
    IN p_ShipDate DATE,
    IN p_ShipAddress VARCHAR(255),
    IN p_ShipCity VARCHAR(255),
    IN p_ShipPostalCode VARCHAR(10),
    IN p_ShipCountry VARCHAR(255),
    IN p_ProductID INT,
    IN p_Quantity INT,
    IN p_UnitPrice DECIMAL(10, 2)
)
BEGIN
    -- Insert into Orders table
    INSERT INTO Orders (CustomerID, OrderDate, ShipDate, ShipAddress, ShipCity, ShipPostalCode, ShipCountry)
    VALUES (p_CustomerID, p_OrderDate, p_ShipDate, p_ShipAddress, p_ShipCity, p_ShipPostalCode, p_ShipCountry);

    -- Get the last inserted OrderID
    SET @lastOrderID = LAST_INSERT_ID();

    -- Insert into OrderDetails table
    INSERT INTO OrderDetails (OrderID, ProductID, Quantity, UnitPrice)
    VALUES (@lastOrderID, p_ProductID, p_Quantity, p_UnitPrice);

    -- Update stock quantity in Products table
    UPDATE Products
    SET UnitsInStock = UnitsInStock - p_Quantity
    WHERE ProductID = p_ProductID;
END;
"""

# Define the stored procedure for updating stock quantity
update_stock_procedure = """
CREATE PROCEDURE IF NOT EXISTS UpdateStockQuantity(
    IN p_ProductID INT,
    IN p_Quantity INT
)
BEGIN
    -- Update stock quantity in Products table
    UPDATE Products
    SET UnitsInStock = UnitsInStock + p_Quantity
    WHERE ProductID = p_ProductID;
END;
"""

# Execute the stored procedure creation queries
cursor.execute(add_order_procedure, multi=True)
cursor.execute(update_stock_procedure, multi=True)
conn.commit()

# Main menu functions

# Function to list all products that are out of stock
def list_out_of_stock():
    try:
        query = """
        SELECT * FROM Products WHERE UnitsInStock = 0;
        """
        cursor.execute(query)
        result = cursor.fetchall()

        if not result:
            print("No out-of-stock products found.")
        else:
            print("List of out-of-stock products:")
            for row in result:
                print(row)
    except mysql.connector.Error as err:
        print(f"Error in list_out_of_stock: {err}")

# Function to find the total number of orders placed by each customer
def total_orders_by_customer():
    try:
        query = """
        SELECT c.CustomerID, c.CustomerName, c.ContactName, COUNT(o.OrderID) AS TotalOrders
        FROM Customers c
        LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
        GROUP BY c.CustomerID, c.CustomerName, c.ContactName;
        """
        cursor.execute(query)
        result = cursor.fetchall()

        if not result:
            print("No customer orders found.")
        else:
            print("Total number of orders placed by each customer:")
            print("{:<15} {:<30} {:<30} {:<15}".format("CustomerID", "CustomerName", "ContactName", "TotalOrders"))
            print("="*90)
            for row in result:
                print("{:<15} {:<30} {:<30} {:<15}".format(row[0], row[1], row[2], row[3]))
    except mysql.connector.Error as err:
        print(f"Error in total_orders_by_customer: {err}")


# Function to display details of the most expensive product ordered in each order
def most_expensive_product_details():
    try:
        query = """
        SELECT o.OrderID, p.ProductName, od.Quantity, od.UnitPrice
        FROM Orders o
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        JOIN Products p ON od.ProductID = p.ProductID
        ORDER BY o.OrderID, od.UnitPrice DESC
        LIMIT 1;
        """
        cursor.execute(query)
        result = cursor.fetchall()

        if not result:
            print("No orders found.")
        else:
            print("Details of the most expensive product ordered in each order:")
            print("{:<15} {:<30} {:<15} {:<15}".format("OrderID", "ProductName", "Quantity", "UnitPrice"))
            print("="*75)
            for row in result:
                print("{:<15} {:<30} {:<15} ${:<15.2f}".format(row[0], row[1], row[2], row[3]))
    except mysql.connector.Error as err:
        print(f"Error in most_expensive_product_details: {err}")

# Function to retrieve a list of products that have never been ordered
def products_never_ordered():
    try:
        query = """
        SELECT * FROM Products p
        LEFT JOIN OrderDetails od ON p.ProductID = od.ProductID
        WHERE od.ProductID IS NULL;
        """
        cursor.execute(query)
        result = cursor.fetchall()

        if not result:
            print("No products found that have never been ordered.")
        else:
            print("List of products that have never been ordered:")
            print("{:<10} {:<30} {:<20} {:<20} {:<15} {:<15}".format("ProductID", "ProductName", "SupplierID", "Category", "UnitPrice", "UnitsInStock"))
            print("="*110)
            for row in result:
                print("{:<10} {:<30} {:<20} {:<20} ${:<15.2f} {:<15}".format(row[0], row[1], row[2], row[3], row[4], row[5]))
    except mysql.connector.Error as err:
        print(f"Error in products_never_ordered: {err}")

# Function to show the total revenue generated by each supplier
def total_revenue_by_supplier():
    try:
        query = """
        SELECT s.SupplierID, s.SupplierName, SUM(od.Quantity * od.UnitPrice) AS TotalRevenue
        FROM Suppliers s
        JOIN Products p ON s.SupplierID = p.SupplierID
        JOIN OrderDetails od ON p.ProductID = od.ProductID
        GROUP BY s.SupplierID, s.SupplierName;
        """
        cursor.execute(query)
        result = cursor.fetchall()

        if not result:
            print("No revenue data available for suppliers.")
        else:
            print("{:<15} {:<30} {:<20}".format("SupplierID", "SupplierName", "TotalRevenue"))
            print("="*65)
            for row in result:
                print("{:<15} {:<30} ${:<20.2f}".format(row[0], row[1], row[2]))
    except mysql.connector.Error as err:
        print(f"Error in total_revenue_by_supplier: {err}")

# Functions to execute the stored procedure and validations for adding a new order
def get_int_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

# Function to get date input with validation
def get_date_input(prompt):
    while True:
        try:
            date_str = input(prompt)
            date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
            if date_pattern.match(date_str):
                return date_str
            else:
                print("Invalid date format. Please use YYYY-MM-DD.")
        except ValueError:
            print("Invalid date. Please enter a valid date.")

# Function to get valid input based on regex pattern
def get_valid_input(prompt, pattern):
    while True:
        try:
            value = input(prompt)
            if re.match(pattern, value):
                return value
            else:
                print("Invalid input. Please enter a valid value.")
        except ValueError:
            print("Invalid input. Please enter a valid value.")

# Function to get float input with validation
def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid floating-point number.")


# Rest of the code with add new order function

# Function to add a new order
def add_new_order():
    try:
        # User input for order details with input validation
        customer_id = get_existing_customer_id()
        order_date = get_date_input("Enter Order Date (YYYY-MM-DD): ")
        ship_date = get_date_input("Enter Ship Date (YYYY-MM-DD): ")
        ship_address = get_valid_input("Enter Shipping Address: ", r'^[A-Za-z0-9\s]+$')
        ship_city = get_valid_input("Enter Shipping City: ", r'^[A-Za-z\s]+$')
        ship_postal_code = get_valid_input("Enter Shipping Postal Code: ", r'^[A-Za-z0-9]+$')
        ship_country = get_valid_input("Enter Shipping Country: ", r'^[A-Za-z\s]+$')
        product_id = get_existing_product_id()
        quantity = get_int_input("Enter Quantity: ")
        unit_price = get_float_input("Enter Unit Price: ")

        # Execute the stored procedure using parameterized query
        add_order_query = """
        CALL AddNewOrder(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(add_order_query, (
            customer_id, order_date, ship_date, ship_address, ship_city,
            ship_postal_code, ship_country, product_id, quantity, unit_price
        ))
        conn.commit()
        print("New order added successfully.")
    except ValueError as ve:
        print(f"Invalid input. Please enter a valid number: {ve}")
    except mysql.connector.Error as err:
        print(f"Error in add_new_order: {err}")

# Function to get an existing customer ID
def get_existing_customer_id():
    while True:
        try:
            customer_id = get_int_input("Enter Customer ID: ")
            # Check if the customer ID exists in the database
            cursor.execute("SELECT CustomerID FROM Customers WHERE CustomerID = %s", (customer_id,))
            result = cursor.fetchone()
            if result:
                return customer_id
            else:
                print("Customer ID does not exist. Please enter a valid Customer ID.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Function to get an existing product ID
def get_existing_product_id():
    while True:
        try:
            product_id = get_int_input("Enter Product ID: ")
            # Check if the product ID exists in the database
            cursor.execute("SELECT ProductID FROM Products WHERE ProductID = %s", (product_id,))
            result = cursor.fetchone()
            if result:
                return product_id
            else:
                print("Product ID does not exist. Please enter a valid Product ID.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Function to add a new order
def add_new_order():
    try:
        # User input for order details with input validation
        customer_id = get_existing_customer_id()
        order_date = get_date_input("Enter Order Date (YYYY-MM-DD): ")
        ship_date = get_date_input("Enter Ship Date (YYYY-MM-DD): ")
        ship_address = get_valid_input("Enter Shipping Address: ", r'^[A-Za-z0-9\s]+$')
        ship_city = get_valid_input("Enter Shipping City: ", r'^[A-Za-z\s]+$')
        ship_postal_code = get_valid_input("Enter Shipping Postal Code: ", r'^[A-Za-z0-9]+$')
        ship_country = get_valid_input("Enter Shipping Country: ", r'^[A-Za-z\s]+$')
        product_id = get_existing_product_id()
        quantity = get_int_input("Enter Quantity: ")
        unit_price = get_float_input("Enter Unit Price: ")

        # Execute the stored procedure using parameterized query
        add_order_query = """
        CALL AddNewOrder(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(add_order_query, (
            customer_id, order_date, ship_date, ship_address, ship_city,
            ship_postal_code, ship_country, product_id, quantity, unit_price
        ))
        conn.commit()
        print("New order added successfully.")
    except ValueError as ve:
        print(f"Invalid input. Please enter a valid number: {ve}")
    except mysql.connector.Error as err:
        print(f"Error in add_new_order: {err}")


# Function to execute the stored procedure for updating stock quantity
def update_stock_quantity():
    try:
        # User input for stock update
        product_id = get_existing_product_id()
        quantity = get_int_input("Enter Quantity to Add: ")

        # Execute the stored procedure using parameterized query
        update_stock_query = """
        CALL UpdateStockQuantity(%s, %s);
        """
        cursor.execute(update_stock_query, (product_id, quantity))
        conn.commit()

        if cursor.rowcount == 0:
            print("Product ID not found. Please enter a valid Product ID.")
        else:
            print("Stock quantity updated successfully.")
    except ValueError as ve:
        print(f"Invalid input. Please enter a valid number: {ve}")
    except mysql.connector.Error as err:
        print(f"Error in update_stock_quantity: {err}")

# Menu to choose options
while True:
    print("\nMenu:")
    print("1. List all products that are out of stock.")
    print("2. Find the total number of orders placed by each customer.")
    print("3. Display details of the most expensive product ordered in each order.")
    print("4. Retrieve a list of products that have never been ordered.")
    print("5. Show the total revenue generated by each supplier.")
    print("6. Add a new order.")
    print("7. Update stock quantity.")
    print("8. Exit.")

    choice = input("Enter your choice (1-8): ")
    if choice == '1':
        list_out_of_stock()
    elif choice == '2':
        total_orders_by_customer()
    elif choice == '3':
        most_expensive_product_details()
    elif choice == '4':
        products_never_ordered()
    elif choice == '5':
        total_revenue_by_supplier()
    elif choice == '6':
        add_new_order()
    elif choice == '7':
        update_stock_quantity()
    elif choice == '8':
        break
    elif choice.isdigit() and 1 <= int(choice) <= 8:
        print("Invalid choice. Please use the functions above for tasks 1-8.")
    else:
        print("Invalid choice.")

# Close the cursor and connection
cursor.fetchall()
cursor.close()
conn.close()
