import json
from database import TicketDB
from analyzer import TicketAnalyzer
from reporter import Reporter

def load_tickets(filename):
    print(f"Loading tickets from: {filename}")
    with open(filename, 'r') as file:
        data = json.load(file)
        return data

if __name__ == "__main__":
    db = TicketDB()
    db.connect()
    db.create_table()
    
    analyzer = TicketAnalyzer()
    
    try:
        tickets = load_tickets("data/tickets.json")
        print(f"\nProcessing & Analyzing {len(tickets)} tickets...")
        
        for ticket in tickets:
            try:
                # DEFENSIVE CODING: Use .get() to avoid KeyError if 'content' is missing
                # Default to empty string if missing
                content = ticket.get('content', "") 
                
                category, priority = analyzer.analyze_ticket(content)
                
                ticket['category'] = category
                ticket['priority'] = priority
                
                db.insert_ticket(ticket)
            except Exception as e:
                # If ONE ticket fails, print error but CONTINUE loop
                print(f"Skipping bad ticket {ticket.get('id', 'Unknown')}: {e}")
                
    except Exception as e:
        print(f"Fatal Error: {e}")
    finally:
        db.close()
        
    reporter = Reporter()
    reporter.generate_report()
