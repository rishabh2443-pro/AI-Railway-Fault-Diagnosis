import paho.mqtt.client as mqtt
import psycopg2
import json

# MQTT settings
broker = "localhost"
port = 1883
topic = "railway/sensors"

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="railway_monitoring",
    user="postgres",
    password="123@abesec",
    port="5432"
)

cursor = conn.cursor()


def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to MQTT Broker!")
    client.subscribe(topic)
    print("Subscribed to:", topic)


def on_message(client, userdata, msg):

    data = json.loads(msg.payload.decode())

    print("\nMessage received:")
    print(data)

    query = """
    INSERT INTO sensor_readings
    (train_id, speed, vibration, temperature, brake_pressure)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        data["train_id"],
        data["speed"],
        data["vibration"],
        data["temperature"],
        data["brake_pressure"]
    )

    cursor.execute(query, values)
    conn.commit()

    print("✅ Data saved to PostgreSQL!")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)

client.loop_forever()