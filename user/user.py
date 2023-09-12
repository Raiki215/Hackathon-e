from flask import Flask,render_template,request,redirect,url_for,session,Blueprint
import user.user_method as user_method
from datetime import timedelta

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/',methods=['POST'])
def login():
    
    mail = request.form.get('mail')
    password = request.form.get('password')
    if user_method.login(mail, password):
        user=user_method.after_login(mail)
        if user != None:
            session['user'] = [user[0], user[1], mail] # session にキー：'user', 0にid 1に名前
            return redirect(url_for('user.home'))
        else :
            error = 'ログインに失敗しました'
            input_data = {
            'mail': mail,
            'password': password
            }
            return render_template('index.html',error=error, data=input_data)
    
@user_bp.route('/logout')
def logout():
    session.pop('user', None)
    session.permanent = True
    return redirect(url_for('index'))

@user_bp.route('/home', methods=['GET'])
def home():
    if 'user' in session:
        
        return render_template('home.html')
    else :
        
        return redirect(url_for('index'))

@user_bp.route('/register')
def register_form():
    return render_template('register.html')

@user_bp.route('/register_exe', methods=['POST'])
def register_exe():
    name = request.form.get('username')
    mail = request.form.get('mail')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if name == '':
        error = 'ユーザー名が未入力です'
        return render_template('register.html', error=error,name=name,password=password,password2=password2)
    if mail == '':
        error = 'メールアドレスが未入力です'
        return render_template('register.html', error=error,name=name,password=password,password2=password2)
    if password == '':
        error = 'パスワードが未入力です'
        return render_template('register.html', error=error,name=name,password=password,password2=password2)
    if password2 == '':
        error = 'メールアドレス(確認用)が未入力です'
        return render_template('register.html', error=error,name=name,password=password,password2=password2)
    if password==password2:
        count = user_method.insert_user(mail,name,password)
    if count == 1:
        msg = '登録が完了しました'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました'
        return render_template('register.html', error=error)

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