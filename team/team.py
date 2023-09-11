from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
import team.team_method as team_method
import asyncio
import json
import cgi



team_bp = Blueprint('team', __name__, url_prefix='/team')

@team_bp.route('/team_register')
def team_register():
        return render_template('team_register.html')
  

@team_bp.route('/team_register_exe', methods=['POST'])
def team_register_exe():
    team_name = request.form.get('team_name')
    # team_name = ''
    team_id = 2
    
    count = team_method.insert_team(team_name, team_id)
    
    if count == 1:
        return render_template('member_register.html')
    else :
        return redirect(url_for('team.team_register'))

@team_bp.route('/mail_search',methods=['POST'])
def mail_search():
    mail = request.data
    
    # data = request.data
    # print(data)
    # print(mail)
    mail = mail.decode()
    
    
    print(json.loads(mail)["word"])
    
    
    result = team_method.mail_search(json.loads(mail)["word"])
    
    return jsonify(result)