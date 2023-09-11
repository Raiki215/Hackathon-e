from flask import Flask,render_template,request,redirect,url_for,session,Blueprint
import task.task_method as task_method
from datetime import timedelta
task_bp = Blueprint('task', __name__, url_prefix='/task')

@task_bp.route('/task')
def add_task():
    if 'user' in session:
        category=task_method.select_category_id()
        if category is None:
            print('home')
            return render_template('home.html')
        else :
            print('task_register')
            return render_template('task_register.html',category=category,id=id)
    else:
        print('user.index')
        return redirect(url_for('user.index'))

@task_bp.route('/post_add_task',methods=['POST'])
def post_add_task():
    name  =request.form.get('name')
    category  =int(request.form.get('category'))##受け取る名前違う
    print(category)
    deadline  =request.form.get('deadline')
    progres  =int(request.form.get('progres'))
    user_id=session['user'][0]
    print(user_id)
    print(deadline)
    count=task_method.insert_task(name,user_id,category,deadline,progres)
    
    if count==1:
        return render_template('home.html')
    else:
        return redirect(url_for('task.add_task'))
    
