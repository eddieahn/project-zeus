import sqlite3

def setup_database():
    conn=sqlite3.connect('feedback.db')
    c=conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            response TEXT,
            feedback INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

setup_database()

# def delete_table(table_name):
#     conn = sqlite3.connect('feedback.db')
#     c = conn.cursor()
#     c.execute(f'DROP TABLE IF EXISTS {table_name}')
#     conn.commit()
#     conn.close()

# # Example usage
# delete_table('feedback')