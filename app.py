from flask import Flask,render_template,request,redirect,url_for,session
from datetime import timedelta
from user.user import user_bp
from admin.admin import admin_bp
import string, random


app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters,k=256))

# app.secret_key
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/notification',methods=['GET'])
def notification():
    return render_template('notification.html')

    
if __name__ == '__main__':
    app.run(debug=True)