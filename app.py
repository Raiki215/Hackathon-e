from flask import Flask,render_template,request,redirect,url_for,session
import psycopg2,string,random,datetime

app = Flask(__name__)


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

    
if __name__ == '__main__':
    app.run()