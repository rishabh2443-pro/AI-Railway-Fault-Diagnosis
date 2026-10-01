import paho.mqtt.client as mqtt


BROKER = "574fb463b0ca435e8d68dec3f4bee00a.s1.eu.hivemq.cloud"
PORT = 8883

USERNAME = "Rishabhydv01"
PASSWORD = "123@abesec"

TOPIC = "railway/train001"


def on_connect(client, userdata, flags, reason_code, properties):

    print("Connected to HiveMQ!")

    print("Subscribing to:", TOPIC)

    client.subscribe(TOPIC)


def on_message(client, userdata, msg):

    print("\nReceived:")

    print(msg.payload.decode())


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.username_pw_set(
    USERNAME,
    PASSWORD
)

client.tls_set()

client.on_connect = on_connect

client.on_message = on_message


print("Connecting to HiveMQ...")

client.connect(
    BROKER,
    PORT
)

client.loop_forever()