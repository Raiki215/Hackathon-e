from flask import Blueprint, Flask, render_template, redirect, session, url_for, request
import admin.admin_method as admin_method
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def admin():
    error = request.args.get('error')
    return render_template('admin_login.html', error=error)

@admin_bp.route('/login', methods=['POST'])
def admin_login():
    id = request.form.get('id')
    password = request.form.get('password')
    if id == '' and password == '':
        error = 'IDとpasswordが未入力です。' 
        return render_template('admin_login.html',error=error) 
    
    elif id == '':
        error = 'IDが未入力です。'
        return render_template('admin_login.html',error=error)

    elif password == '':
        error = 'passwordが未入力です。'
        return render_template('admin_login.html',error=error, id=id)
        
    
    flg = admin_method.admin_login(id, password)
    if flg == True:
        session['admin'] = True
        return redirect(url_for('admin.admin_home'))
    else :
        error = 'パスワードかIDが間違っています'
        return redirect(url_for('admin'),error=error)
    
@admin_bp.route('/admin_home')
def admin_home():
    if 'admin' in session:
        return render_template('admin_home.html')
    else:
        return redirect(url_for('admin.admin'))
    
@admin_bp.route('/admin_logout')
def admin_logout():
    session.pop('admin', None)
    session.permanent = True
    return redirect(url_for('admin.admin'))
    
    