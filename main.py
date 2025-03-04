from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import os
import paho.mqtt.client as mqtt  # For IoT

app = Flask(__name__)
CORS(app)

# OpenAI & Gemini API Keys (Replace with your keys)

genai.configure(api_key="")

# Initialize Text-to-Speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# MQTT Setup (For IoT)
mqtt_client = mqtt.Client()
mqtt_client.connect("MQTT_BROKER_IP", 1883, 60)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data["message"]

    # Use OpenAI or Gemini API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4", messages=[{"role": "user", "content": user_input}]
        )
        reply = response["choices"][0]["message"]["content"]

    except:
        response = genai.generate_text(model="gemini-pro", prompt=user_input)
        reply = response["text"]

    # Speak the response
    engine.say(reply)
    engine.runAndWait()

    return jsonify({"reply": reply})

@app.route("/execute", methods=["POST"])
def execute():
    data = request.json
    command = data["command"]

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
