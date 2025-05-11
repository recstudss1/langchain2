from flask import Flask, request, jsonify
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from flask_cors import CORS  

load_dotenv()

app = Flask(__name__)
CORS(app)

llm = ChatGroq()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message", "")

    messages = [
        SystemMessage("You are Agent 47 Hitman"),
        HumanMessage(user_input)
    ]

    # Get AI response
    result = llm.invoke(messages)

    # ✅ Extract only the text part of AIMessage
    response_text = result.content if hasattr(result, 'content') else str(result)

    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True)
