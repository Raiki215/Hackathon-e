from flask import Flask,render_template
import psycopg2 as pg
# import pandas as pd
import sys
sys.path.append('..')
import db
import sys
import pdb

def insert_task(name,user_id,category_id,deadline,prog):
    sql='INSERT INTO task(id, task_name, task_category_id, user_id, progress, registration_date, completion_date, delete_key) VALUES(default, %s, %s, %s, %s, current_timestamp, %s, false)'
    
    try :
        connection = db.get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql,(name, category_id, user_id, prog, deadline))
        count = cursor.rowcount #更新件数取得
        connection.commit()
    
    except pg.DatabaseError :
        count = 0
        
    finally :
        cursor.close()
        connection.close()
    
    return count

def select_latest_task(user_id):
    sql = 'SELECT * FROM task WHERE user_id = %s and delete_key = %s ORDER BY completion_date ASC LIMIT 5'
    
    try :
        connection = db.get_connection()
        cursor =  connection.cursor()
        cursor.execute(sql,(user_id,'f'))
        rows = cursor.fetchall()
    except pg.DatabaseError:
        rows = 0
    return rows


def select_category_id():
    sql='SELECT id,task_category_name FROM task_classification'
    
    try :
        connection = db.get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql)
        category=cursor.fetchall()    
    except pg.DatabaseError :
        category==None
    finally :
        cursor.close()
        connection.close()
    return category
  
def select_progress(id):
    sql = 'SELECT * FROM degree_of_progress WHERE id = %s'
    try :
        connection = db.get_connection()
        cursor =  connection.cursor()
        cursor.execute(sql,(id,))
        row = cursor.fetchone()
    except pg.DatabaseError:
        row = 0
    return row

def select_team_id(id):
    sql = 'SELECT * from team_member WHERE user_id = %s'
    
    try:
        connection = db.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (id, ))
        results=cursor.fetchall()
    except pg.DatabaseError:
        print('database error')
    finally:
        cursor.close()
        connection.close()
    return results

def select_team(id):
    sql = 'SELECT * from team WHERE id = %s'
    
    try:
        connection = db.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (id, ))
        results=cursor.fetchone()
    except pg.DatabaseError:
        print('database error')
    finally:
        cursor.close()
        connection.close()
    return results

def task_sher(id, team_id):
    sql = 'SELECT * from task WHERE task_category_id = %s AND team_id = %s'
    
    try:
        connection = db.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (id, team_id))
        results=cursor.fetchall()
    except pg.DatabaseError:
        print('database error')
    finally:
        cursor.close()
        connection.close()
    return results

def task_team_category(id):
    sql = 'SELECT id,task_category_name from task_classification WHERE team_id = %s'
    
    try:
        connection = db.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (id,))
        results=cursor.fetchall()
    except pg.DatabaseError:
        print('database error')
    finally:
        cursor.close()
        connection.close()
    return results

def select_task_game_list():
    sql = 'SELECT id,title, goal FROM task_game WHERE private_key = %s and delete_key = %s'
    
    try :
        connection = db.get_connection()
        cursor =  connection.cursor()
        cursor.execute(sql,('f','f'))
        rows = cursor.fetchall()
    except pg.DatabaseError:
        rows = 0
    return rows

def check_task_game(id):
    sql = 'SELECT private_key,delete_key FROM task_game WHERE id = %s'
    
    flg = False
    
    try :
        connection = db.get_connection()
        cursor =  connection.cursor()
        cursor.execute(sql,(id,))
        row = cursor.fetchone()
        if row != None:
            if row[0] == 'f':
                flg = True
            if row[1] == 'f':
                flg = True
    except pg.DatabaseError:
        flg = False
    return flg

def select_task_game(id):
    sql = 'SELECT * FROM task_game WHERE id = %s and private_key = %s and delete_key = %s'
    
    try :
        connection = db.get_connection()
        cursor =  connection.cursor()
        cursor.execute(sql,(id,'f','f'))
        row = cursor.fetchone()
    except pg.DatabaseError:
        row = 0
    return row

def select_task_game_problem(id):
    sql = 'SELECT * FROM game_problem WHERE task_game_id = %s and delete_key = %s'
    
    try :
        connection = db.get_connection()
        cursor =  connection.cursor()
        cursor.execute(sql,(id,'f'))
        rows = cursor.fetchall()
    except pg.DatabaseError:
        rows = 0
    return rows

def select_task_game_user_answer(id):
    sql = 'SELECT * FROM game_problem WHERE id = %s and delete_key = %s'
    
    try :
        connection = db.get_connection()
        cursor =  connection.cursor()
        cursor.execute(sql,(id,'f'))
        row = cursor.fetchone()
    except pg.DatabaseError:
        row = 0
    return row

def insert_score(task_id,user_id,score1,score2,comprehensive_evaluation):
    sql='INSERT INTO score_management(id, task_game_id, user_id, score_1, score_2, comprehensive_evaluation, delete_key) VALUES(default, %s, %s, %s, %s, %s, false)'
    
    try :
        connection = db.get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql,(task_id, user_id, score1, score2, comprehensive_evaluation))
        count = cursor.rowcount #更新件数取得
        connection.commit()
    
    except pg.DatabaseError :
        count = 0
        
    finally :
        cursor.close()
        connection.close()
    
    return count

def select_score(task_game_id,user_id):
    sql = 'SELECT * FROM score_management WHERE task_game_id = %s and user_id = %s and delete_key = %s'
    
    try :
        connection = db.get_connection()
        cursor =  connection.cursor()
        cursor.execute(sql,(task_game_id,user_id,'f'))
        row = cursor.fetchone()
    except pg.DatabaseError:
        row = 0
    return row

def update_score(task_id,user_id,score1,score2,comprehensive_evaluation):
    sql = 'UPDATE score_management SET score_1 = %s,score_2 = %s,comprehensive_evaluation = %s WHERE task_game_id = %s and user_id = %s'
    try :
        connection = db.get_connection()
        cursor =  connection.cursor()
        cursor.execute(sql, (score1,score2,comprehensive_evaluation,task_id,user_id))
        count = cursor.rowcount
        connection.commit()
    except pg.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
    return count
