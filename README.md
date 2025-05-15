# 🖥️ MQTT GUI Receiver with Systemd Autostart

A Python-based desktop GUI application that receives and visually displays MQTT messages (text and images) in real time. Built for edge-device communication using **MQTT**, the system is optimized for use in IoT, surveillance, and remote sensor networks. This solution includes a **systemd service** to auto-start the receiver on boot, making it production-ready for Raspberry Pi or other Linux-based environments.

---

## 🚀 Project Motivation

In modern IoT and real-time systems, reliable message delivery with low latency is crucial. Whether it’s a surveillance system sending images or a sensor node transmitting readings, **MQTT** (Message Queuing Telemetry Transport) is the protocol of choice due to its lightweight design.

This project was designed to:
- Learn and implement real-time data exchange using MQTT.
- Build a GUI that visually displays incoming data.
- Make the setup robust by auto-starting it on boot using **systemd**.
- Simulate practical use cases like remote image monitoring or alert displays.

---

## 🧠 Why MQTT?

**MQTT (Message Queuing Telemetry Transport)** is a lightweight messaging protocol perfect for:
- Low-bandwidth networks
- IoT and embedded systems
- Decoupled communication (publish/subscribe)

### 🔍 Key Advantages:
- Minimal overhead (ideal for constrained devices like Raspberry Pi)
- Reliable message delivery with QoS levels
- Built-in support for retain, will, and persistent sessions
- Decouples data producers (senders) and consumers (receivers)

---

## 📦 Features

- ✅ Real-time message receiving via MQTT
- 🖼️ Displays both **text** and **images**
- 📁 Image transfer via base64 encoding
- 🖥️ Built with Python `tkinter` for a lightweight GUI
- 🔁 Automatically starts on boot via **systemd service**
- 🧪 Tested with Mosquitto MQTT broker
- 📡 Sender and receiver decoupled via Pub/Sub

---

## 📂 Project Structure

```
mqtt-gui-receiver/
│
├── final_receiver_script.py # GUI Receiver subscribing to MQTT topic
├── sender.py # Simulated MQTT Publisher (base64 images + text)
├── systemd/
│ └── mqtt_gui_display.service # systemd unit file for auto-start on boot
└── README.md 
```

---

## 🛠️ Setup Instructions
### 🧳 Prerequisites

- Python 3.8+
- Virtualenv (recommended)
- MQTT broker (e.g. Mosquitto)

### 📌 Install Dependencies

```
git clone https://github.com/Jenish-Patel31/mqtt-gui-receiver.git
cd mqtt-gui-receiver
```

# Set up virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

# Install required libraries
```
pip install paho-mqtt pillow
```

---

# Running the Project
## Start the Receiver (GUI)
```
python final_receiver_script.py 
```

## Run the Sender(for testing)
```
python sender.py 
```
- This sends a base64-encoded image and message to the MQTT topic, which is displayed by the GUI.

## Systemd Autostart on Boot
To run the receiver automatically after boot:
- Copy the systemd service file:
```
sudo cp systemd/mqtt_gui_display.service /etc/systemd/system/
```
- Enable and start the service:
```
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable mqtt_gui_display.service
sudo systemctl start mqtt_gui_display.service
sudo systemctl status mqtt_gui_display.service (check status running)
```
- Check status:
```sudo systemctl status mqtt_gui_display.service```

This ensures your GUI starts even after reboot – ideal for embedded devices.

# Demo
![Screenshot from 2025-05-15 12-57-45](https://github.com/user-attachments/assets/9de596b6-c3d4-4a35-b893-e09cbca9c61c)


# Use Cases
- 🛡️ Security: Display live alerts or camera snapshots remotely.
- 🌡️ IoT Monitoring: Receive data from temperature/humidity sensors.
- 🖥️ Smart Displays: Control info screens or dashboards via MQTT.
- ⚙️ Industrial: Machine status and error reporting on factory panels.

# Tech Stack
Python 3

- paho-mqtt – MQTT communication
- tkinter – GUI
- Pillow – Image handling
- systemd – Background service (Linux boot integration)

## 🙋‍♂️ Author

**Jenish Patel**  
📧 [jenishkp07@gmail.com](mailto:jenishkp07@gmail.com)  
🌐 [LinkedIn](https://www.linkedin.com/in/jenish-patel-31k) | [GitHub](https://github.com/Jenish-Patel31)




