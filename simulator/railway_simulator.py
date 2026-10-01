import random
import time
from datetime import datetime

# Railway sensor simulator

TRAIN_ID = "TRAIN_001"

while True:

    speed = random.randint(60, 120)
    temperature = round(random.uniform(60, 90), 2)
    vibration = round(random.uniform(2, 8), 2)
    brake_pressure = round(random.uniform(4, 7), 2)

    print("\n-----------------------------")
    print("Train ID:", TRAIN_ID)
    print("Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("Speed:", speed, "km/h")
    print("Temperature:", temperature, "°C")
    print("Vibration:", vibration, "mm/s")
    print("Brake Pressure:", brake_pressure, "bar")
    print("-----------------------------")

    time.sleep(5)