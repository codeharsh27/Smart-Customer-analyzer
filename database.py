import sqlite3

class TicketDB:
    def __init__(self, db_name="tickets.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print(f"Connected to database: {self.db_name}")

    def create_table(self):
        """Create the tickets table if it doesn't exist."""
        sql = """
        CREATE TABLE IF NOT EXISTS tickets (
            id TEXT PRIMARY KEY,
            customer TEXT,
            content TEXT,
            status TEXT,
            priority TEXT,   -- New column
            category TEXT    -- New column
        )
        """
        self.cursor.execute(sql)
        self.conn.commit()
        print("Table 'tickets' is ready.")

    def insert_ticket(self, ticket_data):
        """Insert a single ticket into the database."""
        # UPDATED SQL to include new columns
        # We use REPLACE INTO to update existing rows if re-run
        sql = """
        REPLACE INTO tickets (id, customer, content, status, priority, category)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        values = (
            ticket_data['id'],
            ticket_data['customer'],
            ticket_data['content'],
            ticket_data['status'],
            ticket_data['priority'], # Now passing value
            ticket_data['category']  # Now passing value
        )
        
        self.cursor.execute(sql, values)
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
