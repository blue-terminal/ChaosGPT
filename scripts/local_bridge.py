
from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

OLLAMA_API = "http://127.0.0.1:11434/api"

@app.route('/v1/embeddings', methods=['POST'])
def embeddings():
    data = request.json
    text = data.get("input", [""])[0]
    model = data.get("model", "llama3.2:1b")
    
    response = requests.post(f"{OLLAMA_API}/embeddings", json={
        "model": model,
        "prompt": text
    })
    
    if response.status_code == 200:
        emb = response.json().get("embedding")
        return jsonify({
            "data": [{"embedding": emb}],
            "model": model,
            "object": "list"
        })
    return jsonify({"error": "Ollama error"}), 500

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json
    messages = data.get("messages", [])
    model = data.get("model", "llama3.2:1b")
    
    # Convert messages to Ollama prompt or use Ollama chat API
    response = requests.post(f"{OLLAMA_API}/chat", json={
        "model": model,
        "messages": messages,
        "stream": False
    })
    
    if response.status_code == 200:
        ollama_res = response.json()
        content = ollama_res.get("message", {}).get("content", "")
        return jsonify({
            "choices": [{
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop"
            }]
        })
    return jsonify({"error": "Ollama error"}), 500

if __name__ == '__main__':
    app.run(port=5000)
