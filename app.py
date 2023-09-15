import os
import json
import logging
from flask import Flask, request, jsonify
from speech_service import transcribe_audio
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
