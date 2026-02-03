import sqlite3
import os

class TicketDB:
    def __init__(self, db_name="tickets.db"):
        """
        Initialize the database connection handler.
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Establish a connection to the SQLite database.
        """
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        """
        Create the tickets table schema if it does not exist.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS tickets (
            id TEXT PRIMARY KEY,
            customer TEXT,
            content TEXT,
            status TEXT,
            priority TEXT,
            category TEXT
        )
        """
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_ticket(self, ticket_data):
        """
        Insert or update a ticket record in the database.
        """
        sql = """
        REPLACE INTO tickets (id, customer, content, status, priority, category)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        values = (
            ticket_data['id'],
            ticket_data['customer'],
            ticket_data.get('content', ''),
            ticket_data.get('status', 'new'),
            ticket_data.get('priority', 'low'),
            ticket_data.get('category', 'general')
        )
        
        self.cursor.execute(sql, values)
        self.conn.commit()

    def close(self):
        """
        Close the database connection if active.
        """
        if self.conn:
            self.conn.close()
