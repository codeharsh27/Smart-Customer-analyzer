# Smart Customer Support Ticket Analyzer

A Python-based CLI tool that accepts customer support tickets (JSON), analyzes their content to automatically assign Priority and Category, stores them in a SQLite database, and generates summary reports.

## Project Structure
*   `main.py`: The entry point. It orchestrates the ETL (Extract, Transform, Load) process.
*   `database.py`: Handles all SQL database interactions (SQLite).
*   `analyzer.py`: Contains the logic/heuristics to categorize tickets based on keywords.
*   `reporter.py`: Generates insights from the database.
*   `data/tickets.json`: The raw input data.

## How to Run

### Prerequisities
*   Python 3.x installed.

### Execution Steps
1.  Open your terminal/command prompt.
2.  Navigate to the project directory:
    ```bash
    cd "c:/Users/asus/App projects/Customer_analyzer"
    ```
3.  Run the main script:
    ```bash
    python main.py
    ```

### Expected Output
You will see the script:
1.  Connect to the database `tickets.db`.
2.  Load tickets from `data/tickets.json`.
3.  Analyze and save them (handling any bad data gracefully).
4.  Print a summary report of Ticket counts by Priority and Category.

## Resetting the Data
To start fresh (wipe the database):
*   Simply delete the `tickets.db` file. The script will automatically recreate it next time you run it.
    ```bash
    del tickets.db
    ```
