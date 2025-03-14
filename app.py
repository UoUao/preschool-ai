from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)  # 解决跨域问题

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_KEY")

def load_knowledge():
    """自动加载知识库内容"""
    knowledge = ""
    for root, dirs, files in os.walk("knowledge"):
        for file in files:
            if file.endswith(".md"):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    knowledge += f.read() + "\n\n"
    return knowledge

KNOWLEDGE_BASE = load_knowledge()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = f"""
    [系统指令] 你是一名拥有10年经验的幼儿园教师助手，请结合以下专业知识回答：
    {KNOWLEDGE_BASE}
    
    [用户问题] {data['question']}
    [回答要求] 使用通俗易懂的中文，分步骤给出可操作建议
    """
    
    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    
    return jsonify({
        "answer": response.json()['choices'][0]['message']['content']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
