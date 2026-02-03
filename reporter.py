from database import TicketDB

class Reporter:
    def __init__(self):
        self.db = TicketDB()
    
    def generate_report(self):
        """Runs SQL queries to find insights."""
        self.db.connect()
        
        print("\n========== SUPPORT TEAM REPORT ==========")
        
        # Insight 1: Total Ticket Count
        # COUNT(*): A standard SQL function to count rows
        count = self.db.cursor.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
        print(f"Total Tickets: {count}")
        
        # Insight 2: Tickets by Priority
        # GROUP BY: Groups rows that have the same value in 'priority'
        print("\n--- Tickets by Priority ---")
        sql_priority = "SELECT priority, COUNT(*) FROM tickets GROUP BY priority"
        results = self.db.cursor.execute(sql_priority).fetchall()
        for priority, count in results:
            print(f"- {priority.upper()}: {count}")
            
        # Insight 3: Tickets by Category
        print("\n--- Tickets by Category ---")
        sql_category = "SELECT category, COUNT(*) FROM tickets GROUP BY category"
        results = self.db.cursor.execute(sql_category).fetchall()
        for category, count in results:
            print(f"- {category.title()}: {count}")
            
        print("=========================================")
        self.db.close()

if __name__ == "__main__":
    reporter = Reporter()
    reporter.generate_report()
