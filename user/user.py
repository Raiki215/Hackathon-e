from flask import Flask,render_template,request,redirect,url_for,session,Blueprint
import psycopg2,string,random,datetime,db
from datetime import timedelta
user_bp = Blueprint('user', __name__, '/user')

@user_bp.route()


@user_bp.route('/',methods=['POST'])
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
    
@user_bp.route('/logout')
def logout():
    session.pop('user', None)
    session.permanent = True
    user_bp.permanent_session_lifetime = timedelta(minutes=1)
    return redirect(url_for('index'))

@user_bp.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@user_bp.route('/register')
def register_form():
    return render_template('register.html')

@user_bp.route('/register_exe', methods=['POST'])
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
    user_bp.run(debug=True)
