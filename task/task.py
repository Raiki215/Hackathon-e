from flask import Flask,render_template,request,redirect,url_for,session,Blueprint
import random
import task.task_method as task_method

from datetime import timedelta
task_bp = Blueprint('task', __name__, '/task')
# @task_bp.route()

@task_bp.route('/task')
def add_task():
    category=task_method.select_category_id()
    return render_template('task_register.html',category=category)

@task_bp.route('/task_practice_list', methods=['GET'])
def task_practice_list():
    task = task_method.select_task_game_list()
    return render_template('task_practice_list.html',task=task)

@task_bp.route('/task_practice_data', methods=['GET'])
def task_practice_data():
    num = request.args.get('data')
    if task_method.check_task_game(num):
        return redirect(url_for('/task_practice_list'))
        
    data = task_method.select_task_game(num)
    if data != 0:
        return render_template('task_practice_data.html',data=data)
    else:
        return redirect(url_for('/task_practice_list'))

@task_bp.route('/task_practice_q1', methods=['GET'])
def task_practice_q1():
    num = request.args.get('data')
    if task_method.check_task_game(num):
        return redirect(url_for('/task_practice_list'))
    
    original_data = task_method.select_task_game_problem(num)
    if original_data != 0:
        choices_data = random.sample(original_data,len(original_data))
        return render_template('task_practice_q1.html',data=choices_data)
    
    # else:
    #     return redirect(url_for('/task_practice_list'))

@task_bp.route('/task_practice_a1', methods=['GET'])
def task_practice_a1():
    return render_template('task_practice_a1.html')
