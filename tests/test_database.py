from backend.database.connection import get_connection


conn = get_connection()
cur = conn.cursor()

cur.execute(
    """
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    ORDER BY table_name
    """
)

tables = cur.fetchall()

print("TABLES VISIBLE TO PACKSHO:")
print()

for table in tables:
    print(table)

cur.close()
conn.close()