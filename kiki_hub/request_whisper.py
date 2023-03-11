import requests
import base64

def transcribe_audio_question():
    # Load audio file as base64 encoded string
    with open("recording.wav", "rb") as audio_file:
        audio_data = base64.b64encode(audio_file.read()).decode("utf-8")

    response = requests.post("http://127.0.0.1:7860/run/predict", json={
        "data": [
            "transcribe",
            "gpu",
            "en",
            "base.en",
            {"name": "recording.wav", "data": f"data:audio/wav;base64,{audio_data}"},
            {"name": "recording.wav", "data": f"data:audio/wav;base64,{audio_data}"}
        ]
    }).json()

    data = response["data"][0]
    print("-------") 
    print("text from audio question: " + data)
    print("-------")
    return data

#give me __main
if __name__ == "__main__":
    transcribe_audio_question()


