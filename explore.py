import sqlite3

def explore_data():
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()
    
    print("Welcome to the Ticket Explorer!")
    print("Categories: billing, technical, access, feature_request")
    
    while True:
        print("\n-------------------------------------------")
        user_input = input("Enter a category to view (or 'exit' to quit): ").strip().lower()
        
        if user_input == 'exit':
            break
            
        # SQL QUERY EXPLANATION:
        # SELECT * FROM tickets : "Get me everything from the table..."
        # WHERE category = ?    : "...but ONLY if the category matches my input."
        sql = "SELECT id, customer, content, priority FROM tickets WHERE category = ?"
        
        results = cursor.execute(sql, (user_input,)).fetchall()
        
        if not results:
            print(f"No tickets found for category: '{user_input}'")
        else:
            print(f"Found {len(results)} matches:\n")
            for row in results:
                # row is a tuple: (id, customer, content, priority)
                print(f"[{row[3].upper()}] {row[0]} ({row[1]}): {row[2]}")

    conn.close()
    print("Goodbye!")

if __name__ == "__main__":
    explore_data()
