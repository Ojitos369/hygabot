from datetime import datetime
from conexion import conexion, ConnectionDB

def consulta(query):
    mi_conexion = conexion()
    cursor = mi_conexion.cursor()
    cursor.execute(query)
    mi_conexion.commit()
    res = cursor.fetchall()
    mi_conexion.close()

    return res

def ejecutar(query):
    mi_conexion = conexion()
    cursor = mi_conexion.cursor()
    cursor.execute(query)
    mi_conexion.commit()
    mi_conexion.close()

def get_id(username):
    mi_conexion = conexion()
    cursor = mi_conexion.cursor()
    query = f"SELECT id FROM player WHERE username='{username}'"
    cursor.execute(query)
    mi_conexion.commit()
    id = cursor.fetchall()
    id = id[0][0]
    mi_conexion.close()
    return id

def get_mochila(user_id, username):
    try:
        user_id = get_id(username)
    except:
        # creacion de usuario
        ahora = datetime.now()
        ahora_junto = ahora.strftime("%Y%m%d%H%M%S")
        user_id = str(user_id)
        query = f"INSERT INTO player (id, username, register_at) VALUES ('{user_id}', '{username}', '{ahora}')"
        ejecutar(query)
    query = f"SELECT * FROM mochila WHERE user_id='{user_id}'"
    mochila = consulta(query)
    return mochila
