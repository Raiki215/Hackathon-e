import psycopg2
import sys
sys.path.append('..')
import db
def admin_login(id, password):
    sql = "SELECT pass, salt FROM task_account WHERE email = 'admin@morijyobi.ac.jp' "
    flg = False
    
    try :
        if id == 'admin':
            connection = db.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql) # ここでエラーが起きる
            admin = cursor.fetchone()                
            salt = admin[1]
            hashed_passwword = db.get_hash(password, salt)
            
            if hashed_passwword == admin[0]:
                flg = True
        
    except psycopg2.DatabaseError:
        flg = False
    finally:
        cursor.close()
        connection.close()
    
    return flg