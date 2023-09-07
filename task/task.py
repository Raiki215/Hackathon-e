from flask import Flask,render_template,request,redirect,url_for,session,Blueprint
import task.task_method as task_method
task_bp = Blueprint('task', __name__, '/task')
# @task_bp.route()

@task_bp.route('/task_practice_list', methods=['GET'])
def task_practice_list():
    task = task_method.select_task_game_list()
    return render_template('task_practice_list.html',task=task)

@task_bp.route('/task_practice_data', methods=['GET'])
def task_practice_data():
    num = request.args.get('data')
    return render_template('task_practice_data.html')

@task_bp.route('/task_practice_q1', methods=['GET'])
def task_practice_q1():
    return render_template('task_practice_q1.html')

@task_bp.route('/task_practice_a1', methods=['GET'])
def task_practice_a1():
    return render_template('task_practice_a1.html')