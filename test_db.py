import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="railway_monitoring",
    user="postgres",
    password="123@abesec",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = 'fault_results'
    ORDER BY ordinal_position;
""")

print("Columns in fault_results:")

for row in cur.fetchall():
    print(row[0])

cur.close()
conn.close()