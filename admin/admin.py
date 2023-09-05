from flask import Blueprint, Flask, render_template, redirect, session, url_for, request
import admin.admin_method as admin_method
from datetime import timedelta
admin_bp = Blueprint('admin', __name__, '/admin')

@admin_bp.route('/')
def admin():
    return render_template('admin_login.html')

@admin_bp.route('/login')
def admin_login():
    id = request.form.get('id')
    password = request.form.get('password')
    if id == '' and password == '':
        error = 'IDとpasswordが未入力です。' 
        return render_template('admin_login.html',error=error) 

    if id == '':
        error = 'IDが未入力です。'
        return render_template('admin_login.html',error=error)

    if password == '':
        error = 'passwordが未入力です。'
        return render_template('admin_login.html',error=error, id=id)
        
    
    flg = admin_method.admin_login(id, password)
    if flg == True:
        session['admin'] = True
        return render_template('admin_menu.html')
    else :
        error = 'パスワードかIDが間違っています'
        return redirect('admin_login.html',error=error,id=id)
    
@admin_bp.route('/logout')
def admin_logout():
    session.pop('admin', None)
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)
    return redirect(url_for('admin'))
    
    