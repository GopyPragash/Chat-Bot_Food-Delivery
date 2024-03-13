import db_support

if __name__ == "__main__":
    # Test get_next_order_id function
    next_order_id = db_support.get_next_order_id()
    print(f"Next Order ID: {next_order_id}")

    # Test insert_order_item function
    result = db_support.insert_order_item("Samosa", 5, next_order_id)
    if result == 1:
        print("Order item inserted successfully!")
    else:
        print("Failed to insert order item.")

    # Test insert_order_tracking function
    db_support.insert_order_tracking(next_order_id, "in progress")
    print("Order tracking record inserted.")

    # Test get_total_order_price function
    total_price = db_support.get_total_order_price(next_order_id)
    print(f"Total Order Price: {total_price}")

    # Test get_order_status function
    order_status = db_support.get_order_status(next_order_id)
    print(f"Order Status: {order_status}")
