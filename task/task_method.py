from flask import Flask,render_template
import db
import sys

import pdb
import psycopg2 as pg
import pandas as pd

def  task_sher(id, team_id):
    sql = 'SELECT task_name, progress, registration_date, completion_date from Task WHERE task_category_id = %s AND team_id = %s'
    
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
    
    
                

