import paho.mqtt.client as mqtt
import json
import time
import random

broker = "localhost"
port = 1883
topic = "railway/sensors"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(broker, port, 60)

print("🚆 Sensor simulator started...")

while True:

    sensor_data = {
        "train_id": "TRAIN_001",
        "speed": round(random.uniform(70, 100), 2),
        "vibration": round(random.uniform(1, 5), 2),
        "temperature": round(random.uniform(55, 80), 2),
        "brake_pressure": round(random.uniform(60, 90), 2)
    }

    message = json.dumps(sensor_data)

    client.publish(topic, message)

    print("Published:", message)

    time.sleep(3)