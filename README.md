<div align="center">

# Smart Customer Support Ticket Analyzer

**An end-to-end data pipeline that automatically classifies,
prioritizes, and visualizes customer support tickets —
so support teams spend time solving problems,
not sorting them.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-red?logo=streamlit)](https://smart-customer-analyzer.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)](https://streamlit.io)

[Live Demo](https://smart-customer-analyzer.streamlit.app/) ·
[Portfolio](https://harshmule.vercel.app) ·
[LinkedIn](https://linkedin.com/in/harshmule27)

</div>

---

## The Problem

Support teams at growing startups drown in ticket volume.

Every incoming ticket needs to be read, understood,
categorized, and prioritized — manually. A billing
failure and a feature request look identical in an
inbox. The billing failure needs to be resolved in
minutes. The feature request can wait days.

Delays in identifying high-priority issues cause
customer churn. The fix shouldn't require hiring
more people to read tickets faster.

---

## What This Does

An automated pipeline that ingests support tickets,
classifies them by category and priority, stores them,
and surfaces real-time analytics on a dashboard.

```
Ticket comes in
     ↓
Heuristic Analyzer Engine
(category + priority classification)
     ↓
SQLite Database
(structured storage + status tracking)
     ↓
Streamlit Dashboard
(real-time visualization + filtering)
```

**Category classification:**
Technical · Billing · Access · Feature Request

**Priority classification:**
High · Medium · Low

A billing failure gets flagged High automatically.
A feature request gets Low. No human needed to triage.

---

## Architecture

```
User / Client
     ↓
FastAPI (REST API) + Streamlit (Dashboard UI)
     ↓
Heuristic Analyzer Engine
     ↓
SQLite Database
     ↓
Streamlit Dashboard (aggregated metrics + filters)
```

The system has three entry points:
- **Dashboard** — submit tickets via UI, view analytics
- **API** — send tickets programmatically via REST
- **CLI** — batch process a JSON file of tickets

All three feed the same pipeline and the same database.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| Dashboard | Streamlit |
| Backend API | FastAPI |
| Database | SQLite |
| Data Processing | Pandas |
| Testing | Unittest |

---

## Project Structure

```
smart-customer-analyzer/
├── app.py          # Streamlit dashboard — main UI
├── api.py          # FastAPI REST endpoints
├── analyzer.py     # Heuristic classification engine
├── database.py     # SQLite operations + schema
├── reporter.py     # Report generation logic
├── explore.py      # Data exploration utilities
├── main.py         # CLI pipeline entry point
├── data/
│   └── tickets.json    # Sample ticket data
├── tests/              # Unittest suite
└── requirements.txt
```

---

## Getting Started

### Prerequisites
```bash
Python 3.8+
Git
```

### Install
```bash
git clone https://github.com/codeharsh27/Smart-Customer-analyzer.git
cd Smart-Customer-analyzer
pip install -r requirements.txt
```

### Run — 3 ways

**Option 1: Dashboard (recommended)**
Launches the full UI with ticket submission and analytics.
```bash
streamlit run app.py
```

**Option 2: CLI Pipeline**
Batch processes `data/tickets.json` and outputs a report.
```bash
python main.py
```

**Option 3: REST API**
Starts the FastAPI server for programmatic access.
```bash
uvicorn api:app --reload
```
Swagger docs available at `http://127.0.0.1:8000/docs`

---

## Sample Input / Output

**Input:**
```json
{
  "customer": "Alice",
  "content": "The system crashes immediately upon login."
}
```

**Output:**
```json
{
  "id": "TICKET-A1B2",
  "category": "technical",
  "priority": "high",
  "status": "new"
}
```

Crashes → Technical. Crashes on login → High priority.
Classified and stored in under a second.

---

## Honest Limitations + What's Next

The current classifier uses keyword heuristics —
fast to build, explainable, and works well for
clear-cut cases. But it misses nuance.

"I can't access my account because my card expired"
is a Billing issue. A keyword classifier might
call it Access.

The right next step is replacing the heuristic layer
with an LLM-based classifier that understands context,
not just keywords. I built it this way intentionally —
get something working and deployed first,
then improve with real usage data.

Planned improvements:

- **LLM classifier** — replace heuristics with
  Claude or GPT-4o for semantic understanding
- **Agent authentication** — role-based access
  for support agents to manage ticket status
- **Alerting** — email/Slack notifications
  for High priority tickets in real time
- **Database** — migrate SQLite to PostgreSQL
  for production scale

---

## Why I Built This

This was an exercise in building a complete
data system — not just a script.

Ingestion → classification → persistence →
visualization → API layer → CLI → tests.
Every layer has a reason for existing.

The architecture decisions (why FastAPI separate
from Streamlit, why SQLite for this stage,
why heuristics before ML) were deliberate product
engineering choices, not defaults.

---

## Built By

**Harsh Mule** — Product Engineer

I build products end to end — from problem to
deployed system. This is one of them.

[harshmule.vercel.app](https://harshmule.vercel.app) ·
[code.harsh26@gmail.com](mailto:code.harsh26@gmail.com) ·
[LinkedIn](https://linkedin.com/in/harshmule27)
