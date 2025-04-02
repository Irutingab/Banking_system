import mysql.connector

def get_customer(cursor, customer_id):
    try:
        print(f"Fetching customer with ID: {customer_id}")  
        cursor.execute("SELECT customer_id, name, email, phone_number FROM Customers WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        if customer:
            print(f"Customer found: {customer}")  
            return customer
        print(f"Customer {customer_id} not found.")
        return None
    except mysql.connector.Error as e:
        print(f"Error fetching customer: {e}")
        return None

def add_customer(cursor, conn):
    try:
        name = input("Enter customer name: ")
        email = input("Enter customer email: ")
        phone_number = input("Enter customer phone number: ")
        cursor.execute(
            "INSERT INTO Customers (name, email, phone_number) VALUES (%s, %s, %s)",
            (name, email, phone_number)
        )
        conn.commit()
        print("Customer added successfully.")
    except mysql.connector.Error as e:
        print(f"Error adding customer: {e}")

def update_customer(cursor, conn, customer_id):
    try:
        name = input("Enter new customer name: ")
        email = input("Enter new customer email: ")
        phone_number = input("Enter new customer phone number: ")
        cursor.execute(
            "UPDATE Customers SET name = %s, email = %s, phone_number = %s WHERE customer_id = %s",
            (name, email, phone_number, customer_id)
        )
        conn.commit()
        print("Customer updated successfully.")
    except mysql.connector.Error as e:
        print(f"Error updating customer: {e}")

def customer_menu(cursor, conn):
    while True:
        print("\nChoose an action:")
        print("1. Add New Customer")
        print("2. Update Customer Details")
        print("3. View Customer Details")  
        print("4. Exit")  

        choice = input("Enter your choice: ")
        if choice == '3':
            customer_id = input("Enter customer ID: ")
            customer = get_customer(cursor, customer_id)
            if customer:
                print(f"Customer ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}, Phone: {customer[3]}")
        elif choice == '2':
            customer_id = input("Enter customer ID: ")
            customer = get_customer(cursor, customer_id)
            if customer:
                update_customer(cursor, conn, customer_id)
        elif choice == '1':
            add_customer(cursor, conn)
        elif choice == '4':  
            break
        else:
            print("Invalid choice. Please try again.")

