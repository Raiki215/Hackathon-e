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

