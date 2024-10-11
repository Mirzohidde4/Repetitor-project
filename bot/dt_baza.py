import sqlite3, requests


def sql_connect():
    try:
        connection = sqlite3.connect("../db.sqlite3")  # SQLite3 bazasiga bog'lanish
        connection.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False


def sql_connection():
    connection = sqlite3.connect("../db.sqlite3")  # SQLite3 bazasiga bog'lanish
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


def PeopleTable(user_id, username, fullname, phone, gruppa, start, toifa, birthday, region, second_phone, age, goal, monthly):
    if sql_connect() == True:
        try:
            conn = sql_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO main_people (user_id, username, fullname, phone, gruppa, start, toifa, birthday, region, second_phone, age, goal, monthly) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (user_id, username, fullname, phone, gruppa, start, toifa, birthday, region, second_phone, age, goal, monthly),
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


def UpdatePeople(argument, status, user_id, group):
    try:
        with sqlite3.connect("../db.sqlite3") as con:
            cur = con.cursor()
            cur.execute(f"UPDATE main_people SET {argument} = ? WHERE user_id = ? AND gruppa = ?", (status, user_id, group))
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


def DeletePeople(userid, gruppa):
    if sql_connect():
        try:
            conn = sql_connection()
            cursor = conn.cursor()
            query = "DELETE FROM main_people WHERE user_id = ? AND gruppa = ?"
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

