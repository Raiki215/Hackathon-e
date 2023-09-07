import psycopg2
import sys
sys.path.append('..')
import db

def insert_task(name,user_id,category_id,deadline,prog):
    sql='INSERT INTO task(id, task_name, category_id, user_id, progress, registration_date, completion_date, delete_key) VALUES(default, %s, %s, %s, %s, current_timestamp, %s, false)'
    
    try :
        connection = db.get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql,(name, user_id, category_id, prog, deadline))
        count = cursor.rowcount #更新件数取得
        connection.commit()
    
    except psycopg2.DatabaseError :
        count = 0
        
    finally :
        cursor.close()
        connection.close()
    
    return count

def select_category_id():
    sql='SELECT id,task_category_name FROM task_classification'
    
    try :
        connection = db.get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql)
        category=cursor.fetchall()    
    except psycopg2.DatabaseError :
        category==None
    finally :
        cursor.close()
        connection.close()
    return category
  
def select_task_game_list():
    sql = 'SELECT id,title, goal FROM task_game WHERE private_key = %s and delete_key = %s'
    
    try :
        connection = db.get_connection()
        cursor =  connection.cursor()
        cursor.execute(sql,('f','f'))
        rows = cursor.fetchall()
    except psycopg2.DatabaseError:
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
    except psycopg2.DatabaseError:
        flg = False
    return flg

def select_task_game(id):
    sql = 'SELECT * FROM task_game WHERE id = %s and private_key = %s and delete_key = %s'
    
    try :
        connection = db.get_connection()
        cursor =  connection.cursor()
        cursor.execute(sql,(id,'f','f'))
        row = cursor.fetchone()
    except psycopg2.DatabaseError:
        row = 0
    return row

def select_task_game_problem(id):
    sql = 'SELECT * FROM game_problem WHERE task_game_id = %s and delete_key = %s'
    
    try :
        connection = db.get_connection()
        cursor =  connection.cursor()
        cursor.execute(sql,(id,'f'))
        rows = cursor.fetchall()
    except psycopg2.DatabaseError:
        rows = 0
    return rows