from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from database import TicketDB
from analyzer import TicketAnalyzer

app = FastAPI(title="Ticket Analyzer API", version="1.0.0")

# Initialize Service Components
db = TicketDB()
analyzer = TicketAnalyzer()

class TicketInput(BaseModel):
    customer: str
    content: str

@app.post("/tickets/", status_code=201)
def create_ticket(ticket: TicketInput):
    """
    Creats a new support ticket.
    
    Performs real-time analysis to assign category and priority before persistence.
    """
    try:
        db.connect()
        db.create_table()
        
        category, priority = analyzer.analyze_ticket(ticket.content)
        new_id = f"TICKET-{str(uuid.uuid4())[:8].upper()}"
        
        record = {
            "id": new_id,
            "customer": ticket.customer,
            "content": ticket.content,
            "status": "new",
            "category": category,
            "priority": priority
        }
        
        db.insert_ticket(record)
        
        return {
            "ticket_id": new_id,
            "status": "created",
            "analysis_result": {
                "category": category,
                "priority": priority
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "healthy"}
