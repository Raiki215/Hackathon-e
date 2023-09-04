from flask import Flask,render_template,request,redirect,url_for,session
from datetime import timedelta
from user.user import *

app = Flask(__name__)
# app.secret_key
app.register_blueprint(user_bp)

@app.route('/notification',methods=['GET'])
def notification():
    return render_template('notification.html')

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')
    if msg == None:
        return render_template('index.html')
    else :
        return render_template('index.html', msg=msg)
    

@app.route('/mypage', methods=['GET'])
def mypage():
    if 'user' in session:
        return render_template('mypage.html')
    else :
        return redirect(url_for('index'))
    

    
if __name__ == '__main__':
    app.run(debug=True)