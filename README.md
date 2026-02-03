# Smart Customer Support Ticket Analyzer

## Problem Statement
In modern customer support environments, support teams are often overwhelmed by the volume of incoming tickets. Manually categorizing and prioritizing these requests is time-consuming and prone to human error. A delay in identifying "High Priority" issues (such as system outages or billing failures) can lead to significant customer dissatisfaction and churn.

There is a need for an automated system to continually ingest, analyze, and organize support tickets to ensure critical issues are addressed immediately.

## Solution Overview
The **Smart Customer Support Ticket Analyzer** is an end-to-end data processing pipeline and visualization dashboard. It automates the classification of support tickets using Keyword Heuristics to determine:
1.  **Category**: (e.g., Technical, Billing, Access, Feature Request)
2.  **Priority**: (High, Medium, Low)

The solution provides a unified interface for both data ingestion (via API or Bulk JSON) and real-time analytics (via a Dashboard).

## Architecture Diagram

```mermaid
graph LR
    User[User / Client] -->|Input Data| API[FastAPI / Streamlit]
    API -->|Raw Text| Analyzer[Heuristic Analyzer Engine]
    Analyzer -->|Classified Data| DB[(SQLite Database)]
    DB -->|Aggregated Metrics| Dashboard[Streamlit Dashboard]
```

## Tech Stack
*   **Language**: Python 3.x
*   **Frontend**: Streamlit (Data Dashboard & Interactive UI)
*   **Backend API**: FastAPI (RESTful Service)
*   **Database**: SQLite (Relational Persistence)
*   **Data Processing**: Pandas (Dataframe Manipulation)
*   **Testing**: Unittest

## How to Run

### Prerequisites
*   Python 3.8 or higher
*   Git

### Installation
1.  Clone the repository:
    ```bash
    git clone https://github.com/codeharsh27/Smart-Customer-analyzer.git
    cd Smart-Customer-analyzer
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Execution
**Option 1: Run the Dashboard (Recommended)**
This launches the full UI with data entry and visualization.
```bash
streamlit run app.py
```

**Option 2: Run the CLI Pipeline**
This processes the `data/tickets.json` file and outputs a report to the console.
```bash
python main.py
```

**Option 3: Run the API Server**
This starts a REST server awaiting external requests.
```bash
uvicorn api:app --reload
```
*Access Swagger Documentation at `http://127.0.0.1:8000/docs`*

## Sample Input / Output

**Input (JSON):**
```json
{
  "customer": "Alice",
  "content": "The system crashes immediately upon login."
}
```

**Output (Processed Record):**
```json
{
  "id": "TICKET-A1B2",
  "category": "technical",
  "priority": "high",
  "status": "new"
}
```

## Future Improvements
*   **Machine Learning**: Replace keyword heuristics with an NLP model (e.g., BERT or OpenAI API) for semantic understanding.
*   **Authentication**: Add user login for support agents to manage ticket status.
*   **Notifications**: Implement email/Slack alerts for "High Priority" tickets.
*   **Database**: Migrate from SQLite to PostgreSQL for production scalability.

---
*Developed by [Harsh]*
