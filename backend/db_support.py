import mysql.connector
global cnx

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="pandeyji_eatery"
)
# Function to call the MySQL stored procedure and insert an order item
def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()

        # Get the item_id for the food_item
        cursor.execute("SELECT item_id FROM food_items WHERE name = %s", (food_item,))
        result = cursor.fetchone()
        if result is None:
            raise ValueError(f"Item '{food_item}' not found in food_items table")

        item_id = result[0]

        # Insert the order item into the orders table
        insert_query = "INSERT INTO orders (order_id, item_id, quantity, total_price) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (order_id, item_id, quantity, get_total_order_price(order_id)))

        # Committing the changes
        cnx.commit()

        # Closing the cursor
        cursor.close()

        print("Order item inserted successfully!")

        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        cnx.rollback()

        return -1


# Function to get the next available order_id

def get_next_order_id():
    cursor = cnx.cursor()

    # Executing the SQL query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    # Returning the next available order_id
    if result is None:
        return 1
    else:
        return result + 1

# Function to fetch the order status from the order_tracking table
def get_order_status(order_id: int):
    #creating a cursor object
    cursor = cnx.cursor()

    # Executing the SQL query to fetch the order status
    query = ("SELECT status FROM order_tracking WHERE order_id = %s")
    cursor.execute(query, (order_id,))

    # Fetching the result
    result = cursor.fetchone()
    # Closing the cursor
    cursor.close()
    # Returning the order status
    if result:
        return result[0]
    else:
        return None


def get_total_order_price(order_id):
    cursor = cnx.cursor()

    # Executing the SQL query to get the total order price
    query = """
        SELECT SUM(fi.price * o.quantity) 
        FROM orders o 
        JOIN food_items fi ON o.item_id = fi.item_id 
        WHERE o.order_id = %s
    """
    cursor.execute(query, (order_id,))

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    return result if result is not None else 0

# Function to insert a record into the order_tracking table
def insert_order_tracking(order_id, status):
    cursor = cnx.cursor()

    # Inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    # Committing the changes
    cnx.commit()

    # Closing the cursor
    cursor.close()

    if __name__ == "__main__":
        # print(get_total_order_price(56))
        # insert_order_item('Samosa', 3, 99)
        # insert_order_item('Pav Bhaji', 1, 99)
        # insert_order_tracking(99, "in progress")
        print(get_next_order_id())