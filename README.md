# Flask-based Speech-to-Text and ChatGPT API Server

## Description

This is a Flask server that provides an API for Google's Speech-to-Text and OpenAI's GPT-4. This server acts as a middleware, allowing you to easily integrate these services into your application.

## Prerequisites

- Python 3.x
- Flask
- Google Cloud SDK
- OpenAI SDK

## Installation

1. Clone the repository.

    ```bash
    git clone https://github.com/your-repo/flask-api-server.git
    ```

2. Install the required packages.

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask server.

    ```bash
    python app.py
    ```

2. Use your API client to make requests to the server.

    - Speech-to-Text: POST request to `/transcribe`
    - ChatGPT: POST request to `/chat`

## Running Tests

To run tests, execute:

```bash
pytest
```

## Author

Yang Jongyeol
