from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from database import TicketDB
from analyzer import TicketAnalyzer

# Initialize App and Logic
app = FastAPI(title="Ticket Analyzer API")
db = TicketDB()
analyzer = TicketAnalyzer()

# Pydantic Model: Defines what the input JSON MUST look like
class TicketInput(BaseModel):
    customer: str
    content: str

@app.post("/tickets/")
def create_ticket(ticket: TicketInput):
    """
    Endpoint to receive a new ticket, analyze it, and save it.
    """
    try:
        # 1. Setup DB
        db.connect()
        db.create_table()
        
        # 2. Analyze
        category, priority = analyzer.analyze_ticket(ticket.content)
        
        # 3. Create Record
        new_id = f"TICKET-{str(uuid.uuid4())[:8].upper()}" # Generate a random ID like 'TICKET-A1B2'
        
        record = {
            "id": new_id,
            "customer": ticket.customer,
            "content": ticket.content,
            "status": "new",
            "category": category,
            "priority": priority
        }
        
        # 4. Save
        db.insert_ticket(record)
        db.close()
        
        # 5. Return Response
        return {
            "message": "Ticket created successfully",
            "ticket_id": new_id,
            "analysis": {
                "category": category,
                "priority": priority
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Customer Support Analyzer API is running!"}
