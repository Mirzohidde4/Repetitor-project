import sqlite3, requests


def sql_connect():
    try:
        connection = sqlite3.connect("./db.sqlite3")  # SQLite3 bazasiga bog'lanish
        connection.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False


def sql_connection():
    connection = sqlite3.connect("./db.sqlite3")  # SQLite3 bazasiga bog'lanish
    connection.commit()
    return connection


def OylikStatus(user, user_id, gruppa, narx, sana, malumot, oy, status):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO main_oylik (user, user_id, gruppa, narx, date, info, month, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (user, user_id, gruppa, narx, sana, malumot, oy, status),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False
        finally:
            conn.close()
    else:
        return False


def PeopleTable(user_id, username, fullname, phone, toifa, birthday, region, second_phone, age, goal, monthly, start):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO main_oylik (user_id, username, fullname, phone, toifa, birthday, region, second_phone, age, goal, monthly, start) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (user_id, username, fullname, phone, toifa, birthday, region, second_phone, age, goal, monthly, start),
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False
        finally:
            conn.close()
    else:
        return False


def ReadDb(table):
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")

        res = cursor.fetchall()
        l = list()
        if not res:
            return False
        else:
            for i in res:
                l.append(i)
            return l
    else:
        return False
print(ReadDb('main_group'))

def ReadUserStatus(user_id, gruppa):
    if sql_connect() == True:
        conn = sql_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT status FROM main_oylik WHERE user_id = ? AND gruppa = ?", (user_id, gruppa))

        res = cursor.fetchone()
        conn.close()
        return res[0] if res else False
    return False 
 

def UpdateOylik(argument, status, user_id, group):
    try:
        with sqlite3.connect("../db.sqlite3") as con:
            cur = con.cursor()
            cur.execute(f"UPDATE main_oylik SET {argument} = ? WHERE user_id = ? AND gruppa = ?", (status, user_id, group))
            con.commit()
            print(f"Updated {argument} for user_id: {user_id} in group: {group}")  # Logging
            return True
    except sqlite3.Error as err:
        print(f"SQLite Error: {err}")  # Error logging
        return False
    finally:
        if con:
            con.close()  # Ulanishni yopish shart emas, chunki "with" operatori avtomatik yopadi


def DeleteOylik(userid, gruppa):
    if sql_connect():
        try:
            conn = sql_connection()
            cursor = conn.cursor()
            query = "DELETE FROM main_oylik WHERE user_id = ? AND gruppa = ?"
            cursor.execute(query, (userid, gruppa))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")  # Xato haqida batafsilroq ma'lumot
            return False
        finally:
            if conn:
                conn.close()  # Har doim aloqani yopishni unutmang
    return False


    
# def CreateTableAPI():
#     if sql_connect() == True:
#         conn = sql_connection()
#         cursor = conn.cursor()
#         create_table = """ CREATE TABLE Admin (
#                 id BIGINT NOT NULL,
#                 username TEXT NOT NULL,
#                 token TEXT NOT NULL,
#                 api_1 TEXT NOT NULL,
#                 api_2 TEXT NOT NULL,
#                 api_3 TEXT NOT NULL,
#                 group_1 BIGINT NOT NULL,
#                 group_2 BIGINT NOT NULL,
#                 group_3 BIGINT NOT NULL,
#                 price INTEGER NOT NULL
#             ); """
#         cursor.execute(create_table)
#         conn.commit()
#     else:
#         return False  


# def CreateTableCard():
#     if sql_connect() == True:
#         conn = sql_connection()
#         cursor = conn.cursor()
#         create_table = """ CREATE TABLE Card (
#                 photo TEXT NOT NULL,
#                 number BIGINT NOT NULL,
#                 username TEXT NOT NULL
#             ); """
#         cursor.execute(create_table)
#         conn.commit()
#     else:
#         return False  


# def CreateTableBool():
#     if sql_connect() == True:
#         conn = sql_connection()
#         cursor = conn.cursor()
#         create_table = """ CREATE TABLE Oylik (
#                 user TEXT NOT NULL,
#                 user_id BIGINT NOT NULL,
#                 gruppa INTEGER NOT NULL,
#                 status BOOLEAN NOT NULL,
#                 narx INTEGER NOT NULL,
#                 sana INTEGER NOT NULL,
#                 malumot BOOLEAN NOT NULL,
#                 oy INTEGER NOT NULL
#             ); """
#         cursor.execute(create_table)
#         conn.commit()
#     else:
#         return False  
# 
# 
# def Admin(id, username, token, api_1, api_2, api_3, group_1, group_2, group_3, price):
#     if sql_connect() == True:
#         try:
#             conn = sql_connection()
#             cursor = conn.cursor()

#             cursor.execute(
#                 """INSERT INTO Admin (id, username, token, api_1, api_2, api_3, group_1, group_2, group_3, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
#                 (id, username, token, api_1, api_2, api_3, group_1, group_2, group_3, price),
#             )
#             conn.commit()
#             return True
#         except sqlite3.Error as e:
#             print(f"SQLite error: {e}")
#             return False
#         finally:
#             conn.close()
#     else:
#         return False
# Admin(795303467, 'https://t.me/xudoybergan0v', '6842270549:AAEVq-VSV96HcbKmrHuTWwqIB-d4Q2cbUZQ', 'https://sheetdb.io/api/v1/6l88e9ljvile7', 'https://sheetdb.io/api/v1/y2cl3rwvjwc9e', 'https://sheetdb.io/api/v1/y2cl3rwvjwc9e', -4504435403, -4579819207, -4591173539, 100)


# def AdminCard(photo, number, name):
#     if sql_connect() == True:
#         try:
#             conn = sql_connection()
#             cursor = conn.cursor()

#             cursor.execute(
#                 """INSERT INTO Card (photo, number, username) VALUES (?, ?, ?)""",
#                 (photo, number, name),
#             )
#             conn.commit()
#             return True
#         except sqlite3.Error as e:
#             print(f"SQLite error: {e}")
#             return False
#         finally:
#             conn.close()
#     else:
#         return False
# AdminCard('https://avatars.mds.yandex.net/i?id=bdb3d43628f5588e30bbb991bf9fb01eb5e08d61-5666974-images-thumbs&n=13', 1111222233334444, 'Mirzohid')