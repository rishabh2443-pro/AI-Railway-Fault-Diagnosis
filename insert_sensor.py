import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="railway_monitoring",
    user="postgres",
    password="123@abesec",
    port="5432"
)

cursor = conn.cursor()

query = """
INSERT INTO sensor_readings
(train_id, speed, vibration, temperature, brake_pressure)
VALUES (%s, %s, %s, %s, %s)
"""

data = ("TRAIN_002", 95.2, 3.1, 72.5, 68.4)

cursor.execute(query, data)

conn.commit()

print("Sensor data inserted successfully!")

cursor.close()
conn.close()