from flask import Flask, render_template, jsonify, request, flash, session, redirect
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Set mongo db
conn = MongoClient()
conn = MongoClient('mongodb://test:test@localhost', 27017)
db = conn.good42


## 메인 HTML 화면 보여주기
# @app.route('/')
# def index():
#     return render_template('index.html')


## 메인 HTML 화면 보여주기
@app.route('/')
def main():
    return render_template('main.html')

## 퀴즈페이지 HTML 화면 보여주기
## GET으로 들어오면 단순히 화면을 보여주고, POST로 들어오면 DB에서 다음 문제 정보를 전달하는 api
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'GET':
        return render_template('quiz.html')
    elif request.method == 'POST':
        seq = request.form['seq']
        quiz = db.quiz.find_one({'no': seq}, {'_id': False})
        return jsonify({'msg': '성공', 'quiz': quiz})

# 문제별 정답률: 퀴즈 하나를 풀 때마다 그 시도에서 해당 문제의 정답을 맞혔는지 여부를 DB에 저장하기
# author 김진회
# date 21.08.29
@app.route('/saveone', methods=['POST'])
def saveone():
    quizno = request.form['quizno']
    device = request.form['device']
    correct = request.form['correctOrNot']
    now = datetime.datetime.now()
    doc = {
        "quizno": quizno,
        "device": device,
        "correct": correct,
        "time": now,
    }
    db.quizanswers.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})

# 평균 성적: 퀴즈를 완료했을 때 몇 개의 정답을 맞혔는지를 DB에 저장하기
# author 김진회
# date 21.08.29
@app.route('/savetotal', methods=['POST'])
def savetotal():
    device = request.form['device']
    corrects = request.form['countCorrect']
    now = datetime.datetime.now()
    doc = {
        "device": device,
        "corrects": corrects,
        "time": now,
    }
    db.totalcorrects.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})


## 결과페이지 HTML 화면 보여주기
@app.route('/result')
def result():
    return render_template('result.html')


## quiz에서 다음 문제로 넘어갈 때 문제 데이터를 요청하면 다음 문제를 주기
## mongo DB에 문제를 넣을까? 나중에 문제 수정도 가능하게 구현하는 건 어떨까?
## 문제번호, 문제, 답 이런 형태로 DB에 넣어놓고 /admin 페이지에서는 문제를 수정할 수 있게 하고?
# 로그인기능 및 페이지 구현
# author 김진회
@app.route('/admin', methods=['GET', 'POST'])
def member_login():
    ids = ['진회','형준','은정','나현']
    password = 'good42'
    if request.method == 'GET':
        return render_template('admin.html')
    elif request.method == 'POST':
        userid = request.form.get("userid", type=str)
        pw = request.form.get("userPW", type=str)

        if userid == "":
            flash("아이디를 입력하세요")
            return render_template('admin.html')
        elif pw == "":
            flash("비밀번호를 입력하세요")
            return render_template('admin.html')
        else:
            if userid not in ids:
                flash("아이디가 존재하지 않습니다.")
                return render_template('admin.html')
            elif pw == password:
                session["logged_in"] = userid
                return render_template('admin.html', userid = userid)
            else:
                flash("비밀번호가 틀렸습니다.")
                return render_template('admin.html')

## 퀴즈를 DB에 넣을 때 받는 api
@app.route('/admin_quiz', methods=['GET', 'POST'])
def admin_quiz():
    if request.method == 'GET':
        quiz = list(db.quiz.find({}, {'_id': False}))
        return jsonify({'msg': '성공', 'quiz': quiz})
    elif request.method == 'POST':
        no = request.form['quizno']
        category = request.form['category']
        content = request.form['content']
        answer = request.form['answer']
        description = request.form['description']
        # 이미 DB에 있는 퀴즈번호로 요청이 들어오면 기존의 해당 번호 퀴즈를 삭제하고 재등록
        check_cnt = db.quiz.find({"no": no}).count()
        if check_cnt > 0:
            db.quiz.delete_one({"no": no})
        doc = {
            "no": no,
            "category": category,
            "content": content,
            "answer": answer,
            "description": description,
        }
        db.quiz.insert_one(doc)
        return jsonify({'msg': '퀴즈 등록(수정) 완료!'})
    else:
        return None

## 로그아웃
@app.route("/logout", methods=["GET"])
def logout():
    session.pop('logged_in',None)
    return redirect('/admin')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)