from flask import Flask,render_template,request,redirect,url_for,session, Blueprint
from datetime import timedelta
from user.user import user_bp
from admin.admin import admin_bp
<<<<<<< HEAD
from task.task import task_bp
=======
>>>>>>> 30c8a310f0f6dd81b5f0cb79d1f5f5388827426e
from team.team import team_bp
import string, random


app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters,k=256))

# app.secret_key
app.register_blueprint(user_bp)
app.register_blueprint(task_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(team_bp)
<<<<<<< HEAD
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')
    if msg == None:
        return render_template('index.html')
    else :
        return render_template('index.html', msg=msg)
    
# @app.route('/')
# def index():
#     return redirect(url_for('user.index'))
    
@app.route('/mypage', methods=['GET'])
def mypage():
    if 'user' in session:
        return render_template('mypage.html')
    else :
        return redirect(url_for('index'))
=======
app.permanent_session_lifetime = timedelta(minutes=5)
>>>>>>> 30c8a310f0f6dd81b5f0cb79d1f5f5388827426e

@app.route('/notification',methods=['GET'])
def notification():
    return render_template('notification.html')

    
if __name__ == '__main__':
    app.run(debug=True)