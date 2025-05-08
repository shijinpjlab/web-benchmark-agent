import os
import fitz  # PyMuPDF
from flask import Flask, render_template, request, jsonify, send_from_directory
import threading
import uuid
import json
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# 支持的解析工具
TOOLS = {
    'openai': 'OpenAI GPT',
    'claude': 'Anthropic Claude',
    'llamaindex': 'LLamaIndex',
    'pypdf2': 'PyPDF2',
    'pdfminer': 'PDFMiner'
}


# 模拟不同解析工具的处理函数
def parse_with_tool(pdf_path, tool_name):
    # 这里只是模拟，实际应用中需要接入真正的API或库
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        if tool_name == 'openai':
            # 模拟OpenAI处理 - 更简洁
            text += f"Page {page.number + 1} (OpenAI):\n" + page.get_text()[:500].replace('\n', ' ') + "...\n\n"
        elif tool_name == 'claude':
            # 模拟Claude处理 - 保留更多格式
            text += f"=== Page {page.number + 1} (Claude) ===\n" + page.get_text()[:600] + "\n\n"
        elif tool_name == 'llamaindex':
            # 模拟LLamaIndex处理 - 带标记
            text += f"📄 Page {page.number + 1} (LLamaIndex):\n" + page.get_text()[:400] + "...[truncated]\n\n"
        elif tool_name == 'pypdf2':
            # 模拟PyPDF2处理 - 原始提取
            text += f"Page {page.number + 1} (PyPDF2):\n" + page.get_text() + "\n\n"
        else:  # pdfminer
            # 模拟PDFMiner处理 - 更详细
            text += f"Page {page.number + 1} (PDFMiner):\n" + page.get_text()[:700] + "\n\n"
    return text


@app.route('/')
def index():
    return render_template('index.html', tools=TOOLS)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    tool1 = request.form.get('tool1')
    tool2 = request.form.get('tool2')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not all([tool1, tool2]) or tool1 == tool2:
        return jsonify({'error': 'Please select two different tools'}), 400

    # 生成唯一ID保存文件
    file_id = str(uuid.uuid4())
    pdf_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.pdf")
    file.save(pdf_path)

    # 并行处理PDF
    results = {}
    threads = []

    def process_tool(tool_name):
        results[tool_name] = parse_with_tool(pdf_path, tool_name)

    for tool in [tool1, tool2]:
        t = threading.Thread(target=process_tool, args=(tool,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # 保存结果
    result_data = {
        'id': file_id,
        'tools': [tool1, tool2],
        'results': results,
        'timestamp': datetime.now().isoformat()
    }

    with open(os.path.join(RESULTS_FOLDER, f"{file_id}.json"), 'w') as f:
        json.dump(result_data, f)

    # 提取第一页作为预览
    doc = fitz.open(pdf_path)
    first_page = doc[0].get_text()
    doc.close()

    return jsonify({
        'file_id': file_id,
        'tool1': {'name': TOOLS[tool1], 'result': results[tool1]},
        'tool2': {'name': TOOLS[tool2], 'result': results[tool2]},
        'preview': first_page[:500] + '...' if len(first_page) > 500 else first_page
    })


@app.route('/pdf/<file_id>')
def serve_pdf(file_id):
    return send_from_directory(UPLOAD_FOLDER, f"{file_id}.pdf")


@app.route('/save_choice', methods=['POST'])
def save_choice():
    data = request.json
    file_id = data.get('file_id')
    chosen_tool = data.get('chosen_tool')

    result_file = os.path.join(RESULTS_FOLDER, f"{file_id}.json")
    if not os.path.exists(result_file):
        return jsonify({'error': 'Result not found'}), 404

    with open(result_file, 'r') as f:
        result_data = json.load(f)

    result_data['user_choice'] = chosen_tool
    result_data['choice_timestamp'] = datetime.now().isoformat()

    with open(result_file, 'w') as f:
        json.dump(result_data, f)

    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True)