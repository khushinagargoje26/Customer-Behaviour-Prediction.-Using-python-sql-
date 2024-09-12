import pandas as pd
import numpy as np
import mysql.connector
import logging

logging.basicConfig(format='%(asctime)s-%(levelname)s-%(message)s', level=logging.DEBUG)

con = mysql.connector.connect(host="localhost", user="root", password="root", database="customer_behaviour2")
mycursor = con.cursor()

# t='create table customer_details(cust_id int ,Name varchar(50),Address varchar(500),Price float)'
# mycursor.execute(t)
x= pd.read_csv("C:\\Users\\khush\\Downloads\\Customers123.csv")

for i,j in x.iterrows():
    sql="insert into customer_details(cust_id ,Name,Address,price)values(%s,%s,%s,%s)"
    values=(j['id'], j['Name'],j['Address'],j['price'])
    mycursor.execute(sql,values)
# con.commit()

print(" Data Inserted Successfully")

x = pd.DataFrame()





while True:
    choice = int(input("Enter your choice:\nPress 1 to Load CSV Data\nPress 2 for load segment values\nPress 3 to load segment\nPress 4 to Display report of Customer Segments\nPress 5 for segment customor \npress 6 to load segment customer to mysql..!\nPress 7 to exit:\n"))
    
    if choice == 1:
        x = pd.read_csv("C:\\Users\\khush\\Downloads\\Customers123.csv")
        print("Data Loaded successfully!")
        print(x)
    
    elif choice == 2:
        if len(x) > 0:
            conditions = [
                (x['price'] > 1000),
                (x['price'].between(500, 1000)),
                (x['price'] <= 500)
            ]
            x['segment'] = np.select(conditions, ['High_Spender', 'Medium_Spender', 'Low_Spender'], default=None)
            print("Customer segmentation values assigned.")
        else:
            print("No data loaded.")
    
    elif choice == 3:
        print("Loading segmented data into MySQL...")
        if 'segment' not in x.columns:
            print("Error: Customer segmentation not performed. Please segment the customers first (Option 2).")
        else:
            for i, j in x.iterrows():
                update_query = "UPDATE customer_details SET segment = %s WHERE cust_id = %s"
                values = (j['segment'], j['id'])
                mycursor.execute(update_query, values)
            con.commit()
            print("Segmented data loaded into MySQL successfully!")
    
    
    
    
    elif choice == 4:
        print("Displaying report of customer segments...")
        mycursor.execute("SELECT Name, price, High_Spender, Medium_Spender, Low_Spender FROM customer_details")
        result = mycursor.fetchall()
        for j in result:
            print(f"Name: {j[0]}, Price: {j[1]}, High Spender: {j[2]}, Medium Spender: {j[3]}, Low Spender: {j[4]}")
    
    
    elif choice == 5:
        if len(x) > 0:
            conditions = [
                (x['price'] > 1000),
                (x['price'].between(500, 1000)),
                (x['price'] <= 500)
            ]
            x['High_Spender'] = np.select(conditions, [True, False, False], default=False)
            x['Medium_Spender'] = np.select(conditions, [False, True, False], default=False)
            x['Low_Spender'] = np.select(conditions, [False, False, True], default=False)
            print("\nCustomer segmentation performed successfully.")
        else:
            print("No data loaded.")
    
    elif choice == 6:
        print("Loading segmented data into MySQL...")
        if 'High_Spender' not in x.columns:
            print("Error: Customer segmentation not performed. Please segment the customers first (Option 2).")
        else:
            for i, j in x.iterrows():
                update_query = "UPDATE customer_details SET High_Spender = %s, Medium_Spender = %s, Low_Spender = %s WHERE cust_id = %s"
                values = (j['High_Spender'], j['Medium_Spender'], j['Low_Spender'], j['id'])
                mycursor.execute(update_query, values)
            con.commit()
            print("Segmented data loaded into MySQL successfully!")


    elif choice == 7:
        print("Exiting the program.")
        break

    else:
        print("Invalid choice. Please try again.")


    
