from flask import Flask,render_template,request,redirect,url_for,session,Blueprint
import random
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
  
@task_bp.route('/task_practice_list', methods=['GET'])
def task_practice_list():
    # if session['score'] != None:
    #     session.pop('score', None)
    task = task_method.select_task_game_list()
    return render_template('task_practice_list.html',task=task)

@task_bp.route('/task_practice_data', methods=['GET','POST'])
def task_practice_data():
    # if session['score'] != None:
    #     session.pop('score', None)
    num = int(request.form.get('data'))
    if task_method.check_task_game(num):
        return redirect(url_for('/task_practice_list'))
        
    data = task_method.select_task_game(num)
    if data != 0:
        return render_template('task_practice_data.html',data=data)
    else:
        return redirect(url_for('/task_practice_list'))

@task_bp.route('/task_practice_q1', methods=['GET','POST'])
def task_practice_q1():
    # if session['score'] != None:
    #     session.pop('score', None)
    num = request.form.get('data')
    if task_method.check_task_game(num):
        return redirect(url_for('/task_practice_list'))
    
    original_data = task_method.select_task_game_problem(num)
    if original_data != 0:
        choices_data = random.sample(original_data,len(original_data))
        return render_template('task_practice_q1.html',data=choices_data)
    
    # else:
    #     return redirect(url_for('/task_practice_list'))

@task_bp.route('/task_practice_a1', methods=['GET','POST'])
def task_practice_a1():
    task_q = request.form.get('q')
    user_answer = request.form.getlist('event')
    original_data = task_method.select_task_game_problem(task_q)
    user_answer_list = []
    for id in user_answer:
        user_answer_list.append(task_method.select_task_game_user_answer(id))
    score = 10 * len(original_data)
    user_score = 0
    for i in range(len(original_data)):
        if original_data[i][0] == int(user_answer[i]):
            user_score += 10
    session['score'] = user_score
             
    return render_template('task_practice_a1.html',answer=original_data,user_answer=user_answer_list,user_score=user_score,score=score,task_q=task_q)

@task_bp.route('/task_practice_q2', methods=['GET','POST'])
def task_practice_q2():
    task_q = request.form.get('q')
    information = task_method.select_task_game(task_q)
    choice = task_method.select_task_game_problem(task_q)
    # score = session['score']
    return render_template('task_practice_q2.html',q=task_q,task_game=information,choice=choice)

@task_bp.route('/task_practice_a2', methods=['GET','POST'])
def task_practice_a2():
    task_q = request.form.get('q')
    user_answer = request.form.getlist('date')
    original_data = task_method.select_task_game_problem(task_q)
    
    score = 10 * len(original_data)
    user_score = 0
    user_score_list = []
    for i in range(len(original_data)):
        if abs(original_data[i][3] - int(user_answer[i])) == 0:
            user_score += 10
            user_score_list.append(abs(original_data[i][3] - int(user_answer[i])))
        elif abs(original_data[i][3] - int(user_answer[i])) == 5:
            user_score += 5
            user_score_list.append(abs(original_data[i][3] - int(user_answer[i])))
            
        elif abs(original_data[i][3] - int(user_answer[i])) == 10:
            user_score += 3
            user_score_list.append(abs(original_data[i][3] - int(user_answer[i])))
            
        else:
            user_score += 1
            user_score_list.append(abs(original_data[i][3] - int(user_answer[i])))
            
    return render_template('task_practice_a2.html',answer=original_data,user_answer=user_answer,user_score=user_score,score=score,task_q=task_q,user_score_list=user_score_list)

@task_bp.route('/task_practice_evaluation', methods=['GET','POST'])
def task_practice_evaluation():
    task_q = request.form.get('q')
    user_answer2 = int(request.form.get('score'))
    user_answer1 = int(session['score'])
    
    score_list = []
    score = 10 * len(task_method.select_task_game_problem(task_q))
    score_list.append(int(user_answer1/score*100))
    score_list.append(int(user_answer2/score*100))
    if score_list[0] + score_list[1] == 200:
        score_list.append("SS")
    elif score_list[0] + score_list[1] >= 190:
        score_list.append("S")
    elif score_list[0] + score_list[1] >= 150:
        score_list.append("A")
    elif score_list[0] + score_list[1] >= 100:
        score_list.append("B")
    elif score_list[0] + score_list[1] >= 50:
        score_list.append("C")
    
    original_score = task_method.select_score(task_q,session['user'][0])
    if original_score == None:
        if task_method.insert_score(task_q,session['user'][0],user_answer1,user_answer2,score_list[2]) == 1:
            return render_template('task_practice_evaluation.html',user_id=session['user'][0],score_list=score_list)
        else:
            msg = "スコアの登録に失敗しました"
            task = task_method.select_task_game_list()
            return render_template('task_practice_list.html',task=task,msg=msg)
    else:
        if task_method.update_score(task_q,session['user'][0],user_answer1,user_answer2,score_list[2]) != 0:
            return render_template('task_practice_evaluation.html',user_id=session['user'][0],score_list=score_list)
        else:
            msg = "スコアの登録に失敗しました"
            task = task_method.select_task_game_list()
            return render_template('task_practice_list.html',task=task,msg=msg)

    
  
