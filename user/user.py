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
        else :
            error_list.append('ログインに失敗しました')
            input_data = {
            'mail': mail,
            'password': password
            }
            return render_template('index.html',error=error, data=input_data)
    
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


@user_bp.route('/user_edit')
def user_edit():
    user_id = session['user']
    if user_id:
        id = user_id[0]
        user_list = user_method.get_user_list(id)
    else:
        redirect(url_for('login'))
    print(user_list)

    return render_template('user_edit.html',user=user_list)

@user_bp.route('/edit',methods=['POST'])
def edit():
    
    user_id = session['user']
    id = user_id[0]
    name  = request.form.get('name')
    mail  = request.form.get('mail')
    pass1 = request.form.get('pass1')
    pass2 = request.form.get('pass2')
    
    user_list = [id,mail,name,pass1,pass2] #配列に格納する
    user_method.edit_user(mail,name,pass1,id)
    

    if not name or not mail or not pass1 or not pass2: #全部に入力されているか
        return render_template('edit_user.html',user=user_list)
    if pass1 != pass2: #パスワードが一致しているか
        return render_template('edit_user.html',user=user_list)
    
    return redirect(url_for('user.logout'))
