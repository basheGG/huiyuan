import MySQLdb

def curs_db():

    DBHOST = "127.0.0.1"
    DBUSER = "root"
    DBPASSWD = "root"
    DB = "test_demo"
    PORT = 3306
    CHARSET = "utf8"


    db_args = {}
    db_args = {
        "DBHOST":DBHOST,
        "DBUSER": DBUSER,
        "DBPASSWD": DBPASSWD,
        "DB": DB,
        "PORT": PORT,
        "CHARSET": CHARSET
    }


    return db_args
