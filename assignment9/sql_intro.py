import sqlite3
import os


DB_PATH = os.path.join("..", "db", "magazines.db")


def connect_to_db():
    
    print(f"Connecting to database at: {DB_PATH}")

    connection = sqlite3.connect(DB_PATH)

    # TASK 3:

    connection.execute("PRAGMA foreign_keys = 1")

    return connection


def create_tables(conn):
   
    try:

       
        cursor = conn.cursor()

        print("Creating database tables if they do not exist...")

        # 1. PUBLISHERS TABLE
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS publishers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
        """)

        # 2. MAGAZINES TABLE
       
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                publisher_id INTEGER NOT NULL,
                FOREIGN KEY(publisher_id) REFERENCES publishers(id)
            );
        """)

        # 3. SUBSCRIBERS TABLE
       
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL
            );
        """)

        # 4. SUBSCRIPTIONS (JOIN TABLE)
       
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscriber_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                expiration_date TEXT NOT NULL,
                FOREIGN KEY(subscriber_id) REFERENCES subscribers(id),
                FOREIGN KEY(magazine_id) REFERENCES magazines(id)
            );
        """)

        
        conn.commit()
        print("Successfully validated/created all 4 structural tables.")

    except sqlite3.Error as error:
        print(f"An error occurred while building the tables: {error}")



# TASK 3: DATA POPULATION FUNCTIONS (WITH DUP CHECKS)



def add_publisher(conn, name):
   
    try:
        cursor = conn.cursor()

        # Step A: Check if this publisher name already exists in our master table
        # We use a tuple (name,) with a trailing comma because SQLite expects a sequence
        cursor.execute(
            "SELECT id FROM publishers WHERE name = ?;", (name,)
        )
        existing = cursor.fetchone()

        if existing:
            print(
                f"Skipping Publisher: '{name}' already exists with ID {existing[0]}."
            )
            return existing[0]  # Return the ID that already exists

        # Step B: If it doesn't exist, execute an INSERT statement
        # The '?' is a placeholder. This protects us from dangerous SQL Injection hacks.
        cursor.execute(
            "INSERT INTO publishers (name) VALUES (?);", (name,)
        )
        conn.commit()
        print(f"Successfully added Publisher: {name}")
        return cursor.lastrowid  # Returns the brand new ID row number

    except sqlite3.Error as error:
        print(f"Database error while adding publisher: {error}")
        return None


def add_magazine(conn, name, publisher_id):

    try:
        cursor = conn.cursor()

        # Step A: Check for structural duplicate name
        cursor.execute(
            "SELECT id FROM magazines WHERE name = ?;", (name,)
        )
        existing = cursor.fetchone()

        if existing:
            print(
                f"Skipping Magazine: '{name}' already exists with ID {existing[0]}."
            )
            return existing[0]

        # Step B: Insert the new record along with its matching foreign key ID
        cursor.execute(
            "INSERT INTO magazines (name, publisher_id) VALUES (?, ?);",
            (name, publisher_id),
        )
        conn.commit()
        print(f"Successfully added Magazine: {name}")
        return cursor.lastrowid

    except sqlite3.Error as error:
        print(f"Database error while adding magazine: {error}")
        return None


def add_subscriber(conn, name, address):
    
    try:
        cursor = conn.cursor()

        # Step A: Check if a person with this EXACT name living at this EXACT address exists
        cursor.execute(
            "SELECT id FROM subscribers WHERE name = ? AND address = ?;",
            (name, address),
        )
        existing = cursor.fetchone()

        if existing:
            print(
                f"Skipping Subscriber: '{name}' at '{address}' already exists with ID {existing[0]}."
            )
            return existing[0]

        # Step B: Safe insert using protected value tuple variables
        cursor.execute(
            "INSERT INTO subscribers (name, address) VALUES (?, ?);",
            (name, address),
        )
        conn.commit()
        print(f"Successfully added Subscriber: {name}")
        return cursor.lastrowid

    except sqlite3.Error as error:
        print(f"Database error while adding subscriber: {error}")
        return None


def add_subscription(conn, subscriber_id, magazine_id, expiration_date):
    
    try:
        cursor = conn.cursor()

        # Step A: Ensure this person isn't already mapped to this specific magazine issue
        cursor.execute(
            """
            SELECT id FROM subscriptions 
            WHERE subscriber_id = ? AND magazine_id = ?;
        """,
            (subscriber_id, magazine_id),
        )
        existing = cursor.fetchone()

        if existing:
            print(
                f"Skipping Subscription: Mapping already exists with ID {existing[0]}."
            )
            return existing[0]

        # Step B: Final mapping ledger ingestion
        cursor.execute(
            """
            INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date) 
            VALUES (?, ?, ?);
        """,
            (subscriber_id, magazine_id, expiration_date),
        )
        conn.commit()
        print(
            f"Successfully added Subscription mapping: Subscriber {subscriber_id} ➔ Magazine {magazine_id}"
        )
        return cursor.lastrowid

    except sqlite3.Error as error:
        print(f"Database error while adding subscription: {error}")
        return None


# ==========================================
# TASK 4: READ AND JOIN QUERY FUNCTIONS
# ==========================================


def run_assignment_queries(conn):
    """Runs our assignment analysis questions and displays the clean raw rows."""
    try:
        cursor = conn.cursor()

        # QUERY 1: Retrieve all information from the subscribers table
        print("\n--- Query 1: All Subscribers ---")
        cursor.execute("SELECT * FROM subscribers;")
        # fetchall() grabs all matched rows and returns them as a list of Python tuples
        subscribers = cursor.fetchall()
        for row in subscribers:
            print(row)

        # QUERY 2: Retrieve all magazines sorted by name alphabetically (A-Z)
        print("\n--- Query 2: Magazines Sorted Alphabetically ---")
        cursor.execute("SELECT * FROM magazines ORDER BY name ASC;")
        magazines = cursor.fetchall()
        for row in magazines:
            print(row)

        # QUERY 3: Find magazines for a specific publisher using a relational JOIN
        # We look for 'OREILLY MEDIA INC' (ID generated dynamically during seed phase)
        print("\n--- Query 3: Magazines Published by O'Reilly Media ---")
        cursor.execute("""
            SELECT magazines.id, magazines.name, publishers.name 
            FROM magazines
            INNER JOIN publishers ON magazines.publisher_id = publishers.id
            WHERE publishers.name = 'OReilly Media Inc';
        """)
        joined_results = cursor.fetchall()
        for row in joined_results:
            print(row)

    except sqlite3.Error as error:
        print(f"An error occurred while executing analytics: {error}")


# ==========================================
# MAIN SCRIPT EXECUTION TRACK
# ==========================================
if __name__ == "__main__":
    # Step 1: Open communication block line
    connection = connect_to_db()

    if connection:
        try:
            # Step 2: Ensure infrastructure tables exist
            create_tables(connection)

            print("\n=== Beginning Data Seeding Phase ===")

            # Step 3: Populate Table 1 (Publishers) - Generates 3 items
            pub1_id = add_publisher(connection, "OReilly Media Inc")
            pub2_id = add_publisher(connection, "Condé Nast")
            pub3_id = add_publisher(connection, "Hearst Communications")

            # Step 4: Populate Table 2 (Magazines) - Linked directly to parent IDs
            mag1_id = add_magazine(connection, "Python Performance Tuning", pub1_id)
            mag2_id = add_magazine(connection, "Vogue", pub2_id)
            mag3_id = add_magazine(connection, "Cosmopolitan", pub3_id)

            # Step 5: Populate Table 3 (Subscribers) - Generates 3 unique people
            sub1_id = add_subscriber(
                connection, "Alice Smith", "123 Python Way"
            )
            sub2_id = add_subscriber(
                connection, "Bob Jones", "456 Database Drive"
            )
            sub3_id = add_subscriber(
                connection, "Charlie Brown", "123 Python Way"
            )  # Same name, different address rule confirmation check

            # Step 6: Populate Table 4 (Subscriptions) - Map links together with dates
            add_subscription(connection, sub1_id, mag1_id, "2027-01-01")
            add_subscription(connection, sub2_id, mag2_id, "2026-12-31")
            add_subscription(connection, sub3_id, mag3_id, "2028-06-15")

            print("\n=== Executing Verification Queries ===")
            run_assignment_queries(connection)

        finally:
            # Task 1 Requirement: Always cleanly close connections when done
            # putting it in a finally block guarantees it runs even if code crashes!
            connection.close()
            print("\nDatabase connection closed cleanly.")
            