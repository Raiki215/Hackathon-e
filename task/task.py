from flask import Flask,render_template,request,redirect,url_for,session,Blueprint
import random
import task.task_method as task_method

from datetime import timedelta
import datetime


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
        return redirect(url_for('user.home'))
    else:
        return redirect(url_for('task.add_task'))
    
@task_bp.route('/task_list')
def task_list():
    user_id = session['user'][0]
    task_classification = task_method.task_user_category(user_id)
    # task = task_method.select_task(user_id)
    t_classid = []
    for id in task_classification:
        t_classid.append(id[0])
    tasks = []
    for id in t_classid:
        tasks.append(task_method.select_task(id, user_id))
    days = []
    for task in  tasks:
        for t in task:
            dt_now = datetime.datetime.now()
            task_d_day = t[8]
            difference = task_d_day - dt_now
            days.append([t[0],difference.days])
    return render_template('task_list.html', tasks = tasks,task_classification = task_classification,days=days)
    
@task_bp.route('/task_sharing_list')
def task_shar_list():
    user_id = session['user'][0]
    team_list_id = task_method.select_team_id(user_id)
    team_list = []
    for team in team_list_id:
        team_list.append(task_method.select_team(team[1]))
    return render_template('team_list.html',team_list=team_list)

# [(1, 'チーム名', 1, False), (4, 'ぼかろP', 5, False)]


@task_bp.route('/task_sharing',methods=['GET'])
def task_sher():
    # task_category_id = 1
    team_id = request.args.get('data')
    team_name = task_method.select_team(team_id)
    
    # チームのカテゴリを表示
    # カテゴリをチームIDから取得
    task_classification = task_method.task_team_category(team_id)
    # タスクをカテゴリとチームID
    t_classid = []
    for id in task_classification:
        t_classid.append(id[0])
    task_shers = []
    for id in t_classid:
        task_shers.append(task_method.task_sher(id, team_id))
    days = []
    for tasks in  task_shers:
        for task in tasks:
            dt_now = datetime.datetime.now()
            task_d_day = task[8]
            difference = task_d_day - dt_now
            days.append([task[0],difference.days])
        
    return render_template('team.html', team_name=team_name,task_shers = task_shers,task_classification = task_classification,team_id=team_id,t_classid=t_classid,days=days)
  
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
