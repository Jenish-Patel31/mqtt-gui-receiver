import json
import io
import threading
import time
from datetime import datetime
import urllib3
import requests
from PIL import Image, ImageTk, ImageOps
import tkinter as tk
import paho.mqtt.client as mqtt

# === Configuration ===
MQTT_BROKER = "YOUR_BROKER_IP"
MQTT_PORT = 1883
MQTT_TOPIC = "Your_Topic"
IMAGE_BASE_URL = "https://YOUR_SERVER_IP:PORT/public"


# === Disable SSL warnings ===
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# === Initialize Fullscreen Window ===
root = tk.Tk()
root.title("MQTT Media Display")
root.configure(bg="#1e1e1e")
root.attributes("-fullscreen", True)
root.bind("<Alt-j>", lambda e: (root.attributes("-fullscreen", False), root.quit()))

# === UI Layout ===
img_label = tk.Label(root, bg="#1e1e1e")
img_label.place(x=10, y=50, width=1000, height=900)  

text_frame = tk.Frame(root, bg="#1e1e1e", width=875, height=500)
text_frame.pack_propagate(False)  
text_frame.place(x=1030, y=270)   

msg_label = tk.Label(
    text_frame, text="Waiting for message...", wraplength=750,
    justify="left", font=("Helvetica", 26, "bold"), fg="white", bg="#1e1e1e"
)
msg_label.pack(anchor="n", padx=10, pady=10)


info_label =tk.Label(
    text_frame, text="", wraplength=750,  # Ensure it wraps
    font=("Helvetica", 20), fg="lightgray", bg="#1e1e1e",
    justify="left", anchor="nw"
)
info_label.pack(anchor="nw", padx=10, pady=10)


debug_label = tk.Label(
    root, text="", font=("Helvetica", 12),
    fg="lightgray", bg="#333333", anchor="w",
    wraplength=root.winfo_screenwidth() - 40
)
debug_label.pack(side="bottom", fill="x", padx=20, pady=10)

# === Utility: Retry-based Image Fetcher ===
def fetch_image_with_retry(url, retries=5, delay=5):
    for attempt in range(retries):
        print(f"[Info] Attempt {attempt+1} to fetch image...")
        resp = requests.get(url, verify=False)
        if resp.status_code == 200:
            return resp.content
        print(f"[Warning] Image not found (status {resp.status_code}). Retrying in {delay}s...")
        time.sleep(delay)
    print("[Error] All attempts failed.")
    return None

# === MQTT: Connection Callback ===
def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

# === MQTT: Message Handler ===
def on_message(client, userdata, msg):
    print("[MQTT] Message received.")
    try:
        payload = json.loads(msg.payload.decode())
        
        response = payload.get("Response", "Denied").strip().lower()
        if "allowed" in response:
            name = payload.get("Name", "Unknown").strip()
            emp_id = payload.get("EmployeeId", "").strip()
        else:
            name = "Unknown"
            emp_id = "N/A"

        entry_time = payload.get("Time", "").strip()
        img_path = payload.get("url", "").strip()

        # Display response & details
        msg_label.config(text=f"🚪 {response.upper()}")
        
        if emp_id != 'N/A':
            info_label.config(
                text=(
                    f"\n 👤 {name}"
                    f"\n\n 🆔 {emp_id}"
                    f"\n\n ⏱️ {entry_time}"
                    f"\n\n 🔐 {'Employee ✅' if 'allowed' in response.lower() else 'Visitor ❌'}"
                ),
                font=("Helvetica", 28   )
            )
        else:
            info_label.config(
                text=(
                    f"\n 👤 {name}"
                    f"\n\n ⏱️ {entry_time}"
                    f"\n\n 🔐 {'Employee ✅' if 'allowed' in response.lower() else 'Visitor ❌'}"
                ),
                font=("Helvetica", 28   )
            )
            


        text_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        debug_label.config(text=f"🕒 Txt: {text_time}")

        # Full image URL
        full_url = f"{IMAGE_BASE_URL}/{img_path}"
        print(f"[Debug] Fetching image from: {full_url}")

        def process_image():
            image_data = fetch_image_with_retry(full_url)
            if image_data:
                try:
                    image = Image.open(io.BytesIO(image_data))
                    screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
                    image.thumbnail((screen_w // 2, screen_h - 200), Image.LANCZOS)

                    border_color = "green" if "allowed" in response.lower() else "red"
                    bordered_img = ImageOps.expand(image, border=20, fill=border_color)
                    photo = ImageTk.PhotoImage(bordered_img)

                    def update_image():
                        img_label.config(image=photo)
                        img_label.image = photo
                        img_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                        debug_label.config(
                            text=f"🕒 Txt: {text_time}\n🖼️ Img: {img_time}",
                            font=("Helvetica", 11)
                        )
                    root.after(0, update_image)

                except Exception as e:
                    print("[Image Error]", e)
            else:
                root.after(0, lambda: img_label.config(image="", text="❌ Image not found."))

        threading.Thread(target=process_image, daemon=True).start()

    except Exception as e:
        print("[Payload Error]", e)

# === MQTT Client Setup ===
client = mqtt.Client(protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message
client.on_log = lambda c, u, l, b: print("[MQTT LOG]", b)
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

print("[System] GUI running. Press Alt+J to exit.")
root.mainloop()
