#用 Flask 生成一个服务器端程序，只支持 GET 请求，请求的参数是一个字符串，返回一个字符串
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process', methods=['GET'])
def process_request():
    input_string = request.args.get('input')
    # 处理输入字符串
    output_string = f"Processed: {input_string}"
    return jsonify({"output": output_string})

if __name__ == '__main__':
    app.run(debug=True)


