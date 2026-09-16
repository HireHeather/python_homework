import sqlite3
import os

# TASK 1: Complex JOINs with Aggregation

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "db", "lesson.db")

try:
    conn = sqlite3.connect(db_path)

    cursor = conn.execute("""
        SELECT orders.order_id, SUM(products.price * line_items.quantity) AS total_price
        FROM orders
        JOIN line_items ON orders.order_id = line_items.order_id
        JOIN products ON line_items.product_id = products.product_id
        GROUP BY orders.order_id
        ORDER BY orders.order_id
        LIMIT 5;
    """)

    results = cursor.fetchall()
    for row in results:
        print(row)

    # TASK 2: Understanding Subqueries

    cursor = conn.execute("""
        SELECT customers.customer_name, AVG(sub.total_price) AS average_total_price
        FROM customers
        LEFT JOIN (
            SELECT orders.customer_id AS customer_id_b, orders.order_id,
                   SUM(products.price * line_items.quantity) AS total_price
            FROM orders
            JOIN line_items ON orders.order_id = line_items.order_id
            JOIN products ON line_items.product_id = products.product_id
            GROUP BY orders.order_id
        ) AS sub ON customers.customer_id = sub.customer_id_b
        GROUP BY customers.customer_id;
    """)

    results = cursor.fetchall()
    for row in results:
        print(row)

    # TASK 3: An Insert Transaction Based on Data

    conn.execute("PRAGMA foreign_keys = 1")

    cursor = conn.execute(
        "SELECT customer_id FROM customers WHERE customer_name = ?;",
        ("Perez and Sons",)
    )
    customer_id = cursor.fetchone()[0]

    cursor = conn.execute(
        "SELECT employee_id FROM employees WHERE first_name = ? AND last_name = ?;",
        ("Miranda", "Harris")
    )
    employee_id = cursor.fetchone()[0]

    cursor = conn.execute(
        "SELECT product_id FROM products ORDER BY price ASC LIMIT 5;"
    )
    cheapest_product_ids = [row[0] for row in cursor.fetchall()]

    cursor = conn.execute(
        "INSERT INTO orders (customer_id, employee_id, date) VALUES (?, ?, ?) RETURNING order_id;",
        (customer_id, employee_id, "2026-09-16")
    )
    new_order_id = cursor.fetchone()[0]

    for product_id in cheapest_product_ids:
        conn.execute(
            "INSERT INTO line_items (order_id, product_id, quantity) VALUES (?, ?, ?);",
            (new_order_id, product_id, 10)
        )

    conn.commit()

    cursor = conn.execute("""
        SELECT line_items.line_item_id, line_items.quantity, products.product_name
        FROM line_items
        JOIN products ON line_items.product_id = products.product_id
        WHERE line_items.order_id = ?;
    """, (new_order_id,))

    results = cursor.fetchall()
    for row in results:
        print(row)

    # TASK 4: Aggregation with HAVING

    cursor = conn.execute("""
        SELECT employees.employee_id, employees.first_name, employees.last_name,
               COUNT(orders.order_id) AS order_count
        FROM employees
        JOIN orders ON employees.employee_id = orders.employee_id
        GROUP BY employees.employee_id
        HAVING COUNT(orders.order_id) > 5;
    """)

    results = cursor.fetchall()
    for row in results:
        print(row)




except sqlite3.Error as error:
    print(f"Database error: {error}")

finally:
    conn.close()