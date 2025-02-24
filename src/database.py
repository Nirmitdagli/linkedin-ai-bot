import sqlite3

DB_PATH = "database/bot_memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            status TEXT CHECK(status IN ('Pending', 'Approved', 'Posted')),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")

def store_post(content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (content, status) VALUES (?, 'Pending')", (content,))
    conn.commit()
    conn.close()

def fetch_pending_posts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, content FROM posts WHERE status='Pending'")
    posts = cursor.fetchall()
    conn.close()
    return posts

def approve_post(post_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE posts SET status='Approved' WHERE id=?", (post_id,))
    conn.commit()
    conn.close()

