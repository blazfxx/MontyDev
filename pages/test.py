from database import init_finance_db, get_db_connection

username = "bob"  # set this to a real username

# 1. Make sure the finance tables exist
init_finance_db()

# 2. Open a connection using your helper
conn = get_db_connection()
c = conn.cursor()

# 3. Now your table WILL exist
c.execute("SELECT * FROM expenses WHERE username = ?", (username,))
print("Raw expenses rows:", c.fetchall())

c.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE username = ?", (username,))
print("Total spent:", c.fetchone())

conn.close()