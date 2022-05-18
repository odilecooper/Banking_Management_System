import MySQLdb
from MySQLdb._exceptions import OperationalError


def db_login(user, passwd, server_addr, dbname):
    try:
        db = MySQLdb.connect(server_addr, user, passwd, dbname)
    except OperationalError:
        db = None

    return db

def db_showbanks(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Banks")
    res = cursor.fetchall()
    cursor.close()
    return res

def db_showassists(db):
    cursor = db.cursor()
    cursor.execute("SELECT id, bank_name FROM Assistants")
    res = cursor.fetchall()
    cursor.close()
    return res

def db_close(db):
    if db is not None:
        db.close()

if __name__ == "__main__":
    db = db_login("lyp1234", "1234", "127.0.0.1", "test")

    tabs = db_showtable(db)
    
    db_close(db)
