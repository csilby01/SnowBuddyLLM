from flask import Flask, request, jsonify
from flask_cors import CORS
from functions import getModelResponse

app = Flask(__name__)
CORS(app)

#query API route
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    print("generating response...")
    # You can replace this with your LLM logic
    reply = getModelResponse(chat, user_message)
    print("response generated")
    return jsonify({'reply': reply})

if __name__ == "__main__":
    app.run(debug="true")