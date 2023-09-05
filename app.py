from flask import Flask,render_template,request,redirect,url_for,session
import psycopg2,string,random,datetime,db
from datetime import timedelta

app = Flask(__name__)
# app.secret_key

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/task_practice_list', methods=['GET'])
def task_practice_list():
    return render_template('task_practice_list.html')

@app.route('/task_practice_data', methods=['GET'])
def task_practice_data():
    return render_template('task_practice_data.html')

@app.route('/task_practice_q1', methods=['GET'])
def task_practice_q1():
    return render_template('task_practice_q1.html')

@app.route('/task_practice_a1', methods=['GET'])
def task_practice_a1():
    return render_template('task_practice_a1.html')


@app.route('/notification',methods=['GET'])
def notification():
    return render_template('notification.html')

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')
    if msg == None:
        return render_template('index.html')
    else :
        return render_template('index.html', msg=msg)
    
@app.route('/',methods=['POST'])
def login():
    user_name  =request.form.get('username')
    password  =request.form.get('password')
    if db.login(user_name, password):
        session['user'] = True # session にキー：'user', バリュー:True を追加
        return redirect(url_for('mypage'))
    else :
        error = 'ログインに失敗しました'
        input_data = {
            'user_name': user_name,
            'password': password
        }
        return render_template('index.html',error=error, data=input_data)
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)
    return redirect(url_for('index'))

@app.route('/mypage', methods=['GET'])
def mypage():
    if 'user' in session:
        return render_template('mypage.html')
    else :
        return redirect(url_for('index'))
    
@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    password = request.form.get('password')
    if user_name == '':
        error = 'ユーザー名が未入力です'
        return render_template('register.html', error=error,user_name=user_name,password=password)
    if password == '':
        error = 'パスワードが未入力です'
        return render_template('register.html', error=error,user_name=user_name,password=password)
    count = db.insert_user(user_name, password)
    if count == 1:
        msg = '登録が完了しました'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました'
        return render_template('register.html', error=error)
    
if __name__ == '__main__':
    app.run(debug=True)