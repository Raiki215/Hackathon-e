from flask import Flask,render_template,request,redirect,url_for,session,Blueprint
import task.task_method as task_method
from datetime import timedelta
task_bp = Blueprint('task', __name__, '/task')

@task_bp.route('/task')
def add_task():
    category=task_method.select_category_id()
    return render_template('task_register.html',category=category)



