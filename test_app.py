import pytest
import json
from app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_chat_endpoint(client):
    sample_request_data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
    }
    response = client.post('/chat', json=sample_request_data)
    assert response.status_code == 200

    response_data = json.loads(response.data.decode('utf-8'))
    print(response_data)
    assert 'response' in response_data


def test_transcribe_audio(client):
    # 오디오 파일 업로드와 함께 POST 요청을 보냄
    with open('test_files/hello.wav', 'rb') as f:
        response = client.post('/transcribe', data={'file': f})

    # 응답 코드와 응답 데이터 검증
    assert response.status_code == 200
    
    response_data = json.loads(response.data.decode('utf-8'))
    assert 'transcripts' in response_data
    assert isinstance(response_data['transcripts'], list)


def test_synthesize_text(client):
    sample_request_data = {"text": "안녕하세요. 좋은 하루입니다."}
    
    response = client.post('/synthesize', json=sample_request_data)
    assert response.status_code == 200
    
    # You may also want to check if the audio is of a non-zero length,
    # meaning something was synthesized.
    assert len(response.data) > 0

    # You may additionally want to save the output audio for manual verification
    with open('test_output.mp3', 'wb') as f:
        f.write(response.data)
