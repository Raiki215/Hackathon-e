from flask import Blueprint,render_template
import task.task_method as task_method
task_bp = Blueprint('task', __name__, url_prefix='/task')

@task_bp.route('/task_sharing')
def task_sher():
    # task_category_id = 1
    team_id = 2
    
    # チームのカテゴリを表示
    # カテゴリをチームIDから取得
    task_classification = task_method.task_team_category(team_id)
    # タスクをカテゴリとチームID
    for t_class in task_classification:
        task_shers = task_method.task_sher(t_class[0], team_id)

        
    return render_template('team.html', task_shers = task_shers,task_classification = task_classification)

    
    
