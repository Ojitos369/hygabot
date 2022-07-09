import os
import json
import pymysql

host = os.environ['HYGABOT_DB_HOST']
port = int(os.environ['HYGABOT_DB_PORT'])
user = os.environ['HYGABOT_DB_USER']
passwd = os.environ['HYGABOT_DB_PASSWD']
db = os.environ['HYGABOT_DB_DB']

#--------- data conect with mysql ----------
def conexion(database = ''):
    # Con puerto
    miConexion = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)

    # Sin puerto
    #miConexion = pymysql.connect(host=host, user=user, password=passwd, db=db)
    return miConexion


class ConnectionDB:
    def __init__(self, mode = 'P'):
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd)
        self.cursor = self.conn.cursor()
    
    def consulta_asociativa(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            result = [dict(zip([key[0] for key in self.cursor.description], row)) for row in result]
            return result
        except Exception as e:
            print('\n'*4)
            print(query)
            print('\n')
            print(e)
            print('\n'*4)
            return False
    
    def ejecutar(self, query):
        try:
            self.cursor.execute(query)
            return True
        except Exception as e:
            print('\n'*4)
            print(query)
            print('\n')
            print(e)
            print('\n'*4)
            self.rollback()
            self.commit()
            self.close()
            return False
    
    def associative_query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            result = [dict(zip([key[0] for key in self.cursor.description], row)) for row in result]
            return result
        except Exception as e:
            print('\n'*4)
            print(query)
            print('\n')
            print(e)
            print('\n'*4)
            return False
    
    def excute_query(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.lastrowid
        except Exception as e:
            print('\n'*4)
            print(query)
            print('\n')
            print(e)
            print('\n'*4)
            self.rollback()
            self.commit()
            self.close()
            return False
    
    def commit(self):
        try:
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    
    def rollback(self):
        try:
            self.conn.rollback()
            return True
        except Exception as e:
            print(e)
            return False

    def close(self):
        try:
            self.conn.close()
            return True
        except Exception as e:
            print(e)
            return False

