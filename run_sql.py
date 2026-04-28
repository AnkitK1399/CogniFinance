import sqlite3

def run_query(sql):
    try:
        # Connect to your Django DB
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        # Execute the SQL
        cursor.execute(sql)
        
        # If it's a SELECT query, show results
        if sql.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        else:
            conn.commit()
            print("Query executed successfully.")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

# --- TYPE YOUR QUERY BELOW ---
query = "SELECT city from users_user WHERE user_id = 6 AND  transaction_type = 'EXPENSE' AND date BETWEEN '2026-03-02' AND '2026-03-22'; "
run_query(query)