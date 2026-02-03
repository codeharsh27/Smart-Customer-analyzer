from database import TicketDB

class Reporter:
    def __init__(self):
        self.db = TicketDB()
    
    def generate_report(self):
        """Generates a statistical summary of the ticket database."""
        self.db.connect()
        
        try:
            print("\n[ Database Summary ]")
            
            # Total Count
            count = self.db.cursor.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
            print(f"Total Records: {count}")
            
            # Priority Breakdown
            print("\nPriority Distribution:")
            priorities = self.db.cursor.execute("SELECT priority, COUNT(*) FROM tickets GROUP BY priority").fetchall()
            for priority, count in priorities:
                print(f"  {priority.title()}: {count}")
                
            # Category Breakdown
            print("\nCategory Distribution:")
            categories = self.db.cursor.execute("SELECT category, COUNT(*) FROM tickets GROUP BY category").fetchall()
            for category, count in categories:
                print(f"  {category.title()}: {count}")
                
        except Exception as e:
            print(f"Error generating report: {e}")
        finally:
            self.db.close()

if __name__ == "__main__":
    reporter = Reporter()
    reporter.generate_report()
