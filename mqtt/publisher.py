import paho.mqtt.client as mqtt
import json
import time
import random


# ============================================================
# HIVEMQ CONFIGURATION
# ============================================================

BROKER = "574fb463b0ca435e8d68dec3f4bee00a.s1.eu.hivemq.cloud"
PORT = 8883

USERNAME = "Rishabhydv01"
PASSWORD = "123@abesec"

TOPIC = "railway/train001"


# ============================================================
# MQTT CLIENT
# ============================================================

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.username_pw_set(
    USERNAME,
    PASSWORD
)

client.tls_set()


# ============================================================
# CONNECT
# ============================================================

print("Connecting to HiveMQ...")

client.connect(
    BROKER,
    PORT
)

print("Connected to HiveMQ!")


# ============================================================
# SEND SENSOR DATA
# ============================================================

for i in range(10):

    sensor_data = {

        "train_id": "train001",

        "speed_kmph": round(
            random.uniform(70, 120), 2
        ),

        "bearing_temperature_c": round(
            random.uniform(50, 90), 2
        ),

        "track_vibration": round(
            random.uniform(2, 9), 2
        ),

        "brake_pressure_psi": round(
            random.uniform(65, 100), 2
        ),

        "wheel_wear_percent": round(
            random.uniform(10, 90), 2
        ),

        "timestamp": time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }


    message = json.dumps(sensor_data)


    client.publish(
        TOPIC,
        message
    )


    print(
        "Published:",
        message
    )


    time.sleep(2)


# ============================================================
# DISCONNECT
# ============================================================

client.disconnect()

print("Disconnected from HiveMQ.")