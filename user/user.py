from flask import Flask,render_template,request,redirect,url_for,session,Blueprint
import user.user_method as user_method
import task.task_method as task_method
from datetime import timedelta
import datetime

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/')
def index():
    msg = request.args.get('msg')
    if msg == None:
        msg = ""
    return render_template('index.html',msg=msg)

@user_bp.route('/login',methods=['POST'])
def login():
    
    mail = request.form.get('mail')
    password = request.form.get('password')
    
    if user_method.login(mail, password):
        user=user_method.after_login(mail)
        
        if user != None:
            session['user'] = [user[0], user[1], mail] # session にキー：'user', 0にid 1に名前
            return redirect(url_for('user.home'))
        else:
            return redirect(url_for(''))
    
    else :

        error = 'ログインに失敗しました'
        mail= mail
        
        return render_template('index.html',error=error,mail=mail)
    
@user_bp.route('/logout')
def logout():
    session.pop('user', None)
    session.permanent = True
    return redirect(url_for('user.index'))

@user_bp.route('/home', methods=['GET'])
def home():
    if 'user' in session:
        task = task_method.select_latest_task(session['user'][0])
        task_list = []
        for t in task:
            task_day = t[8].strftime('%Y/%m/%d')
            dt_now = datetime.datetime.now()
            task_d_day = t[8]
            difference = task_d_day - dt_now
            task_progress = task_method.select_progress(t[5])
            task_list.append([t[1],task_day,difference.days,task_progress[0],task_progress[1]])
        return render_template('home.html',task=task,task_list=task_list)
    else :
        
        return redirect(url_for('user.index'))

@user_bp.route('/register')
def register_form():
    return render_template('register.html')

@user_bp.route('/register_exe', methods=['POST'])
def register_exe():
    name = request.form.get('username')
    mail = request.form.get('mail')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_list = []

    if name == '':
        error_list.append('ユーザー名が未入力です')
    if mail == '':
        error_list.append('メールアドレスが未入力です')
    if password == '':
        error_list.append('パスワードが未入力です')
    if password2 == '':
        error_list.append('メールアドレス(確認用)が未入力です')
        
    if len(error_list) == 0:   
        
        if password==password2:
            count = user_method.insert_user(mail,name,password)
            if count == 1:
                msg = '登録が完了しました'
                return redirect(url_for('user.index', msg=msg))
            else:
                error_list.append('登録に失敗しました')
                return render_template('register.html', error=error_list)
    else :
        return render_template('register.html',error=error_list)

