from flask import Flask, render_template, request
import speech_recognition as sr
import pyttsx3
import pickle

app = Flask(__name__)

# Load the trained model and vectorizer
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio"
        except sr.RequestError:
            return "Sorry, there seems to be an issue with the request"

def speak_text(text):
    """Uses TTS to speak the provided text."""
    engine.say(text)
    engine.runAndWait()

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        text = recognize_speech()
        if text:
            text_transformed = vectorizer.transform([text])
            prediction = model.predict(text_transformed)
            result = "Positive" if prediction == 0 else "Negative"
            speak_text(f"The result is {result}")
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5002)
