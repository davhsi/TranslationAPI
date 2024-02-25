from modules.helperFunctions import *
from pytube import extract
from modules.voiceCloning import *

def translate_video(url, target_language):
    id = extract.video_id(url)
    target_audience = target_language

    installVideo(url)
    get_transcript(id, "data/transcript.txt")
    extract_audio("videos/Original_Video", "audios/sample.mp3")
    get_translation("data/transcript.txt", "data/translated_transcript.txt", target_audience)

    with open("data/translated_transcript.txt", "r") as file:
        voiceOver(file.read(), "audios/VoiceOver.mp3")
        delete_cloned_voice()

    replace_audio("videos/Original_Video", "audios/VoiceOver.mp3", "videos/Final_Video.mp4")

# Example usage:
# translate_video("https://www.youtube.com/watch?v=yourvideoid", "en")
# Replace "https://www.youtube.com/watch?v=yourvideoid" with the actual URL, and "en" with the target language code.

# If you want to integrate this into a Flask API hosted on Heroku:

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/translate_video", methods=["POST"])
def translate_video_endpoint():
    data = request.get_json()
    url = data["url"]
    target_language = data["target_language"]
    
    translate_video(url, target_language)
    
    return jsonify({"message": "Video translated successfully."})

if __name__ == "__main__":
    app.run(debug=True)
