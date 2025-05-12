from flask import Flask, request, jsonify
from config import *
from model.qa_chain import get_chain
import re

app = Flask(__name__)
qa_chain = get_chain()

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get("question")

    if not query:
        return jsonify({"error": "질문이 비어 있습니다"}), 400

    result = qa_chain.invoke({"question": query})
    text = result["answer"]

    response = {
        "name": extract_name(text),
        "description": extract_description(text),
        "ingredients": extract_ingredients(text),
        "instructions": extract_instructions(text),
        "user": {
            "id": 1,
            "name": "신짱구"
        }
    }

    return jsonify(response)

# 레시피 이름 추출
def extract_name(text):
    match = re.search(r"- name\s*:\s*(.+)", text)
    return match.group(1).strip() if match else "이름 없음"

# 설명 추출
def extract_description(text):
    match = re.search(r"- description\s*:\s*(.+)", text)
    return match.group(1).strip() if match else "설명 없음"

# 재료 리스트 추출
def extract_ingredients(text):
    ingredients = []
    match = re.search(r"- ingredients\s*:\s*((?:\n\s*\*.+)+)", text)
    if match:
        raw = match.group(1).strip().split('\n')
        for line in raw:
            item = re.sub(r"^\*\s*", "", line).strip()
            if item:
                parts = item.split(' ', 1)
                if len(parts) == 2:
                    name, amount = parts
                else:
                    name, amount = parts[0], ""
                ingredients.append({"name": name.strip(), "amount": amount.strip()})
    return ingredients

# 조리 단계 추출
def extract_instructions(text):
    instructions = []
    matches = re.findall(r"###\s*(\d+)단계\s*###\n(.+?)(?=\n###|\Z)", text, re.DOTALL)
    for step, desc in matches:
        instructions.append({
            "step": int(step),
            "text": desc.strip()
        })
    return instructions


if __name__ == '__main__':
    app.run(debug=True)