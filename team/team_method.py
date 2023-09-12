import psycopg2
import psycopg2.extras
import sys
sys.path.append('..')
import db

def insert_team(name, team_admin_id):
    sql = 'INSERT INTO team VALUES(default, %s, %s, false)'
    try:
        connection = db.get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql,(name, team_admin_id))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
    
    return count


def insert_team_member(user_id, team_id):
    sql = 'INSERT INTO team_member VALUES(%s, %s, false)'
    try:
        connection = db.get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (user_id, team_id))
        
        count = cursor.rowcount
        connection.commit()
        
    except psycopg2.DatabaseError:
        count = 0
    finally :
        cursor.close()
        connection.close()
    
    return count


def mail_search(mail,id):
    sql = "SELECT id,email FROM task_account WHERE email = %s and email NOT LIKE 'admin@morijyobi.ac.jp'and id NOT IN (%s) "
    
    try:
        connection = db.get_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        cursor.execute(sql,(mail,id))
        
        results = cursor.fetchall()
        
        dict_result = []
        for row in results:
            dict_result.append(dict(row))
        print(dict_result)
        return dict_result
        
                
        
    except psycopg2.DatabaseError:
        results = None
    finally:
        cursor.close()
        connection.close()
        
    return results

def team_id(user_id):
    sql = 'SELECT MAX(id) FROM team WHERE team_admin_id = %s'
    try:
        connection = db.get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql,(user_id,))
        
        result = cursor.fetchone()
        
    except psycopg2.DatabaseError:
        result = 0
    finally:
        cursor.close()
        connection.close()
    return result