import os
import json
import logging
from flask import Flask, request, jsonify
from speech_service import transcribe_audio, synthesize_text
from chat_service import get_gpt_response


app = Flask(__name__)

def get_logger():
    # log on console and file (log/app.log)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("log/app.log")
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger

logger = get_logger()

# 서비스 계정 키 파일 경로 설정
service_file = "credentials/google_service_account.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_file

with open(service_file, "r") as f:
    google_config = json.load(f)


@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        audio_content = file.read()

        # STT 호출
        response = transcribe_audio(google_config["project_id"], audio_content)
        
        transcripts = []
        for result in response.results:
            transcripts.append(result.alternatives[0].transcript)
        
        return jsonify({"transcripts": transcripts}), 200


@app.route('/synthesize', methods=['POST'])
def synthesize():
    text = request.json.get("text")
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    audio_content = synthesize_text(google_config["project_id"], text)
    
    # You can also save this as a file if you want to
    # with open("output.mp3", "wb") as out:
    #     out.write(audio_content)

    # Here, I'm returning the audio content directly
    # You might want to encode it in a specific format or return as a file download
    return audio_content, 200, {'Content-Type': 'audio/mp3'}


@app.route('/chat', methods=['POST'])
def chat():
    request_data = request.json

    if 'messages' not in request_data:
        return jsonify({"error": "No messages provided"}), 400

    messages = request_data['messages']
    response_content = get_gpt_response(messages)

    return jsonify({"response": response_content}), 200


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=35950)
    # app.run(debug=True, host="0.0.0.0", port=35950)

