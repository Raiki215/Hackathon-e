import psycopg2
import sys
sys.path.append('..')
import db

def select_task_game_list():
    sql = 'SELECT id,title, goal FROM task_game WHERE private_key = %s and delete_key = %s'
    
    try :
        connection = db.get_connection()
        cursor =  connection.cursor()
        cursor.execute(sql,('f','f'))
        rows = cursor.fetchall()
    except psycopg2.DatabaseError:
        rows = 0
    finally :
        cursor.close()
        connection.close()
    
    return rows