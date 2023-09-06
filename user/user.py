from flask import Flask,render_template,request,redirect,url_for,session,Blueprint
import user.user_method as user_method
from datetime import timedelta


user_bp = Blueprint('user', __name__, url_prefix='/user')
@user_bp.route('/')
def index():
    msg = request.args.get('msg')
    return render_template('index.html', msg=msg)


@user_bp.route('/login',methods=['POST'])
def login():
    
    mail  =request.form.get('mail')
    password  =request.form.get('password')
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
        
        return render_template('home.html')
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
            else :
                error_list.append('登録に失敗しました')
        else:
            error_list.append("パスワードが一致しません")
    return render_template('register.html', error_list=error_list,name=name,password=password,password2=password2)
