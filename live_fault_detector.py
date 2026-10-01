import psycopg2
import time

conn = psycopg2.connect(
    host="localhost",
    database="railway_monitoring",
    user="postgres",
    password="123@abesec",
    port="5432"
)

cursor = conn.cursor()

print("🚆 Live Fault Detection Started...")

last_id = 0

while True:

    cursor.execute("""
        SELECT id, train_id, speed, vibration,
               temperature, brake_pressure
        FROM sensor_readings
        WHERE id > %s
        ORDER BY id ASC
    """, (last_id,))

    rows = cursor.fetchall()

    for row in rows:

        id, train_id, speed, vibration, temperature, brake_pressure = row

        faults = []

        if vibration > 4:
            faults.append("High Vibration")

        if temperature > 75:
            faults.append("High Temperature")

        if brake_pressure < 65:
            faults.append("Low Brake Pressure")

        if speed > 95:
            faults.append("High Speed")

        if len(faults) == 0:
            risk = "LOW"
        elif len(faults) == 1:
            risk = "MEDIUM"
        else:
            risk = "HIGH"

        print("\n---------------------------")
        print("Train:", train_id)
        print("Speed:", speed)
        print("Vibration:", vibration)
        print("Temperature:", temperature)
        print("Brake Pressure:", brake_pressure)
        print("Faults:", faults)
        print("Risk:", risk)

        # Save fault result to PostgreSQL
        cursor.execute("""
            INSERT INTO fault_results
            (sensor_id, train_id, faults, risk)
            VALUES (%s, %s, %s, %s)
        """, (
            id,
            train_id,
            ", ".join(faults) if faults else "No Fault",
            risk
        ))

        conn.commit()

        print("✅ Fault result saved to PostgreSQL!")

        last_id = id

    time.sleep(2)