from flask import Flask, request, jsonify
from config import *
from model.qa_chain import get_chain

app = Flask(__name__)
qa_chain = get_chain()

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get("question")

    if not query:
        return jsonify({"error": "질문이 비어 있습니다"}), 400

    result = qa_chain.invoke({"question": query})
    return jsonify({"answer": result["answer"]})

if __name__ == '__main__':
    app.run(debug=True)