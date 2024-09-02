from flask import Flask, request, jsonify
import speech_recognition as sr
import pyttsx3
from datetime import datetime

app = Flask(__name__)

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

@app.route('/voice-command', methods=['GET'])
def voice_command():
    command = recognize_speech()
    response = ""

    if "time" in command:
        response = f"The time is {datetime.now().strftime('%H:%M:%S')}"
    elif "date" in command:
        response = f"Today's date is {datetime.now().strftime('%Y-%m-%d')}"
    else:
        response = "I can only tell you the time or the date."

    speak(response)
    return jsonify({"response": response})
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
