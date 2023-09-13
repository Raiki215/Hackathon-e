import psycopg2
import sys
sys.path.append('..')
import db

def get_mail(id):
    sql = 'SELECT email FROM task_account WHERE id = %s'
    try:
        connection = db.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(id,))
        result = cursor.fetchone()
        for result in result:
            mail = result
    except psycopg2.DatabaseError:
        mail = None
    finally:
        cursor.close()
        connection.close()
    return mail

def insert_user(email,name,password):
    sql = 'INSERT INTO task_account VALUES(default, %s, %s, %s, %s, false)'
    
    salt = db.get_salt()
    hashed_password = db.get_hash(password, salt)
    
    try :
        connection = db.get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql,(email,name,salt,hashed_password))
        count = cursor.rowcount #更新件数取得
        connection.commit()
    
    except psycopg2.DatabaseError :
        count = 0
        
    finally :
        cursor.close()
        connection.close()
    
    return count

def login(mail, password):
    sql = 'SELECT pass, salt FROM task_account WHERE email = %s'
    
    flg = False
    
    try :
        connection = db.get_connection()
        cursor =  connection.cursor()
        cursor.execute(sql, (mail, ))
        
        user = cursor.fetchone()
        
        if user != None:
            salt = user[1]
            
            hashed_password = db.get_hash(password,  salt)
            
            if hashed_password == user[0]:
                flg = True
    
    except psycopg2.DatabaseError:
        flg = False
    
    finally :
        cursor.close()
        connection.close()
    
    return flg

def after_login(mail):
    sql='SELECT id,name FROM task_account WHERE email=%s'
    
    try :
        connection = db.get_connection()
        cursor =  connection.cursor()
        cursor.execute(sql, (mail, ))
        user = cursor.fetchone()
    except psycopg2.DatabaseError:
        user = None
        
    finally :
        cursor.close()
        connection.close()
    
    return user