from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import os
import paho.mqtt.client as mqtt  # For IoT

app = Flask(__name__)
CORS(app)

# Configure Gemini API Key
GENAI_API_KEY = "your-gemini-api-key"  # Replace with your Gemini API key
genai.configure(api_key=GENAI_API_KEY)

# Initialize Text-to-Speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# MQTT Setup (For IoT)
mqtt_client = mqtt.Client()
mqtt_client.connect("MQTT_BROKER_IP", 1883, 60)  # Replace with your MQTT broker IP

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data["message"]

    try:
        # Generate response using Gemini API
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_input)
        reply = response.text

    except Exception as e:
        reply = f"Error: {str(e)}"

    # Speak the response
    engine.say(reply)
    engine.runAndWait()

    return jsonify({"reply": reply})

@app.route("/execute", methods=["POST"])
def execute():
    data = request.json
    command = data["command"].lower()

    if "open youtube" in command:
        os.system("start https://www.youtube.com")
        return jsonify({"status": "Opened YouTube"})

    elif "play music" in command:
        os.system("start spotify")
        return jsonify({"status": "Playing Music"})

    elif "turn on lights" in command:
        mqtt_client.publish("home/lights", "ON")
        return jsonify({"status": "Lights Turned On"})

    return jsonify({"status": "Command Not Found"})

if __name__ == "__main__":
    app.run(debug=True)
