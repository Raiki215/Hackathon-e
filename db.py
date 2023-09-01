import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection


def get_salt():
    charset = string.ascii_letters + string.digits
    
    salt = ''.join(random.choices(charset, k=30))
    return salt


def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1246).hex()
    return hashed_password

def insert_user(email,name,salt,password):
    sql = 'INSERT INTO task_account VALUES(default, %s, %s, %s, %s,0)'
    
    salt = get_salt()
    hashed_password = get_hash(password, salt)
    
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (email,name, salt,hashed_password))
        count = cursor.rowcount #更新件数取得
        connection.commit()
    
    except psycopg2.DatabaseError :
        count = 0
        
    finally :
        cursor.close()
        connection.close()
    
    return count

def login(mail, password):
    sql = 'SELECT pass, salt FROM task_account WHERE mail = %s'
    flg = False
    
    try :
        connection = get_connection()
        cursor =  connection.cursor()
        cursor.execute(sql, (mail, ))
        user = cursor.fetchone()
        
        if user != None:
            salt = user[1]
            
            hashed_password = get_hash(password,  salt)
            
            if hashed_password == user[0]:
                flg = True
    
    except psycopg2.DatabaseError:
        flg = False
    
    finally :
        cursor.close()
        connection.close()
    
    return flg