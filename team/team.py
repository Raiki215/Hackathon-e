from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
import team.team_method as team_method
import user.user_method as user_method
import asyncio
import json
import cgi



team_bp = Blueprint('team', __name__, url_prefix='/team')

@team_bp.route('/team_register')
def team_register():
    if 'user' in session:
        return render_template('team_register.html')
    else:
        return render_template('index.html')

@team_bp.route('/team_register_exe', methods=['POST'])
def team_register_exe():
    if 'user' in session:
        team_name = request.form.get('team_name')
        # team_name = ''
        team_admin_id = session['user'][0]
        if team_name == '':
            error = 'チーム名を入力してください'
            return render_template('team_register.html',error=error)
        
        count = team_method.insert_team(team_name, team_admin_id)
        
        if count == 1:
            return render_template('member_register.html')
        else :
            return redirect(url_for('team.team_register'))
    else:
        return render_template('index.html')
    
@team_bp.route('/mail_search',methods=['POST'])
def mail_search():
    mail = request.data
    
    # data = request.data
    # print(data)
    # print(mail)
    mail = mail.decode()
    
    user_id = session['user'][0]
    # print(json.loads(mail)["word"])
    
    
    result = team_method.mail_search(json.loads(mail)["word"],user_id)
    
    return jsonify(result)


@team_bp.route('/invite_member',methods=['POST'])
def invite_member():
    id_list = request.form.getlist("id")
    session['id_list'] = id_list
    if len(id_list) == 0:
        return render_template('member_register.html')
    else:
        mail_list = []
        for i in id_list:
            # print(i)
            mail = user_method.get_mail(int(i))
            # print(mail)
            mail_list.append(mail)
        
        
        return render_template('member_register_confirm.html',mail_list=mail_list)

@team_bp.route('/add_member',methods=['POST'])
def add_member():
    if 'user' in session:
        user_id = session['id_list']
        team_admin_id = session['user'][0]
        # team_admin_id = 2
        print(user_id)
        for id in user_id:
            print(int(id))
            team_id = team_method.team_id(team_admin_id)
            # print(team_id)
            count = team_method.insert_team_member(id, team_id[0])
            if count == 1:
                return render_template('team_task_list.html') 
    else:
        return render_template('index.html')       
             
    
