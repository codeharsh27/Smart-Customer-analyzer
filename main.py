import json
import logging
from database import TicketDB
from analyzer import TicketAnalyzer
from reporter import Reporter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_tickets(filename):
    """Parses the JSON input file safely."""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
        return []
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in file: {filename}")
        return []

def main():
    logging.info("Starting Ticket Processing Pipeline")
    
    db = TicketDB()
    db.connect()
    db.create_table()
    
    analyzer = TicketAnalyzer()
    
    tickets = load_tickets("data/tickets.json")
    
    if not tickets:
        logging.warning("No tickets to process.")
        return

    processed_count = 0
    for ticket in tickets:
        try:
            content = ticket.get('content', "")
            category, priority = analyzer.analyze_ticket(content)
            
            ticket['category'] = category
            ticket['priority'] = priority
            
            db.insert_ticket(ticket)
            processed_count += 1
        except Exception as e:
            logging.error(f"Failed to process ticket {ticket.get('id', 'Unknown')}: {e}")

    logging.info(f"Successfully processed {processed_count} tickets.")
    db.close()
    
    # Generate summary report
    print("\n--- Execution Report ---")
    reporter = Reporter()
    reporter.generate_report()

if __name__ == "__main__":
    main()
