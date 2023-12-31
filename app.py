from flask import Flask,render_template,request,redirect,url_for,session, Blueprint
from datetime import timedelta
from user.user import user_bp
from admin.admin import admin_bp
from team.team import team_bp
from task.task import task_bp
import string, random


app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters,k=256))

# app.secret_key
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(team_bp)
app.register_blueprint(task_bp)
app.permanent_session_lifetime = timedelta(minutes=5)
    
@app.route('/')
def index():
    return redirect(url_for('user.index'))


@app.route('/notification',methods=['GET'])
def notification():
    return render_template('notification.html')

    
if __name__ == '__main__':
    app.run(debug=True)