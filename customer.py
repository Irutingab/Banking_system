import mysql.connector
import phonenumbers

def validate_phone_number(phone_number):

    if any(char.isalpha() for char in phone_number):
        return None
    if not all(c.isdigit() or c in '+ ()-' for c in phone_number):
        return None

    try:
        parsed_number = phonenumbers.parse(phone_number, "RW")
        
        if phonenumbers.is_valid_number(parsed_number):
            formatted_number = phonenumbers.format_number(
                parsed_number, 
                phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )
            return formatted_number
        else:
            return None
    except phonenumbers.NumberParseException:
        return None


def get_customer(cursor, customer_id):
    try:
        print(f"retrieving customer's details using their IDs: {customer_id}")  
        cursor.execute("SELECT customer_id, name, email, phone_number FROM Customers WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        if customer:
            print("Customer found")  
            return customer  
        else:
            print(f"Customer {customer_id} not found.")
            return None
    except mysql.connector.Error as e:
        print(f"An error occurred while retrieving customer: {e}")
        return None

def add_customer(cursor, conn):
    try:
        name = input("Enter customer name: ")
        email = input("Enter customer email: ")

        while True:
            phone_input = input("Enter customer's phone number: ")
            valid_phone = validate_phone_number(phone_input)
            
            if valid_phone:
                phone_number = valid_phone
                break
            else:
                print("Invalid phone number, please retry.")
        
        cursor.execute(
            "INSERT INTO Customers (name, email, phone_number) VALUES (%s, %s, %s)",
            (name, email, phone_number)
        )
        conn.commit()
        print("Customer added successfully.")
    except mysql.connector.Error as e:
        print(f"An error occurred while adding customer: {e}")

def update_customer(cursor, conn, customer_id):
    try:
        cursor.execute("SELECT name, email, phone_number FROM Customers WHERE customer_id = %s", (customer_id,))
        Existing_data = cursor.fetchone()

        if not Existing_data:
            print("Customer not found.")
            return

        current_name, current_email, current_phone = Existing_data

        print("Press enter to keep current value or edit them: \n")
        name = input(f"Enter new customer name (current: {current_name}): ").strip() or current_name
        email = input(f"Enter new customer email (current: {current_email}): ").strip() or current_email
        
        while True:
            phone_input = input(f"Enter new customer phone number (current: {current_phone}): ").strip()
            
            if not phone_input:
                phone_number = current_phone
                break
                
            valid_phone = validate_phone_number(phone_input)
            if valid_phone:
                phone_number = valid_phone
                
                break
            else:
                print("Invalid phone number, only rwandan phone numbers are accepted.")

        cursor.execute(
            "UPDATE Customers SET name = %s, email = %s, phone_number = %s WHERE customer_id = %s",
            (name, email, phone_number, customer_id)
        )
        conn.commit()
        print("Customer updated successfully.")
        
    except mysql.connector.Error as e:
        print(f"An error occurred while updating the database: {e}")

def delete_customer(cursor, conn, customer_id):
    try:
        cursor.execute("SELECT name FROM Customers WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        
        if not customer:
            print(f"Customer ID {customer_id} not found.")
            return False
            
        confirm = input(f"Are you sure you want to delete customer '{customer[0]}'? "
                        f"This will also delete all their accounts and transactions. (y/n): ")
        
        if confirm.lower() != 'y':
            print("Deletion cancelled.")
            return False
            
        cursor.execute("SELECT account_number FROM Accounts WHERE customer_id = %s", (customer_id,))
        accounts = cursor.fetchall()
        
        for account in accounts:
            account_number = account[0]
            print(f"Deleting transactions for account {account_number}...")
            cursor.execute("DELETE FROM Transactions WHERE account_number = %s", (account_number,))
            
        print(f"Deleting accounts for customer {customer_id}...")
        cursor.execute("DELETE FROM Accounts WHERE customer_id = %s", (customer_id,))
        
        print(f"Deleting customer {customer_id}...")
        cursor.execute("DELETE FROM Customers WHERE customer_id = %s", (customer_id,))
        
        conn.commit()
        print(f"Customer {customer_id} and all their accounts and transactions have been deleted.")
        return True
        
    except mysql.connector.Error as e:
        print(f"An error occurred while deleting customer: {e}")
        conn.rollback()  # back up any changes in case of error
        return False

def customer_menu(cursor, conn):
    while True:
        print("\nChoose an action:")
        print("1. Add New Customer")
        print("2. Update Customer Details")
        print("3. View Customer Details")  
        print("4. Delete Customer") 
        print("5. Exit")  

        choice = input("Enter your choice: ")
        if choice == '3':
            customer_id = input("Enter customer ID: ")
            customer = get_customer(cursor, customer_id)
            if customer:
                print(f"(Customer ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}, Phone: {customer[3]})")
        elif choice == '2':
            customer_id = input("Enter customer ID: ")
            customer = get_customer(cursor, customer_id)
            if customer:
                update_customer(cursor, conn, customer_id)  
        elif choice == '1':
            add_customer(cursor, conn)
        elif choice == '4': 
            customer_id = input("Enter customer ID to delete: ")
            delete_customer(cursor, conn, customer_id)
        elif choice == '5':  
            break
        else:
            print("Invalid choice")

