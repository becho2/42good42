from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

## 메인 HTML 화면 보여주기
# @app.route('/')
# def index():
#     return render_template('index.html')

## 메인 HTML 화면 보여주기
@app.route('/')
def main():
    return render_template('main.html')

## 메인 HTML 화면 보여주기
@app.route('/result')
def result():
    return render_template('result.html')





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)