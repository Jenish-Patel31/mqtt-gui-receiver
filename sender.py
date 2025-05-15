import paho.mqtt.client as mqtt
import base64
import json

MQTT_BROKER = "YOUR_BROKER_IP"
MQTT_PORT = 1883
MQTT_TOPIC="YOUR_TOPIC"


with open("sender_pics/jenish_Good.png", "rb") as f:
    encoded_image = base64.b64encode(f.read()).decode()

# message = {
#     "type": "image_with_text",
#     "message": "this is the message1",
#     "image": encoded_image
# }


# message = {
#     "type": "image_with_text",
#     "name": "Jenish Patel",
#     "email": "jenishkp07@gmail.com",
#     "phone": "9979891854",
#     "age": 20,
#     "is_employee": True,
#     "message": "Welcome Jenish!",
#     "image": encoded_image
# }


# message = {
#     "type": "image_with_text",
#     "name": "",
#     "email": "",
#     "phone": "",
#     "age": "",
#     "is_employee":"" ,
#     "message": "",
#     "image": encoded_image
# }


message= {
    "Name":" null ",
    "Time":" 09/05/2025 17:34:00 ",
    "EmployeeId":" null ",
    "Response":" Access Denied ",
    "url":"/url_to_image.jpeg"
}

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT)
client.publish(MQTT_TOPIC, json.dumps(message))
print("Image with the Caption is sent!")

client.disconnect()
