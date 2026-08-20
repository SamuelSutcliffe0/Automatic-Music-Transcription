from .imports import *

def auto_reconnect(func):
    @functools.wraps(func)   
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except errors.OperationalError as e:
            if e.errno == 2013: 
                self.cursor,self.db = connect()
                return func(self, *args, **kwargs)
            else:
                raise
    return wrapper

def connect():
    load_dotenv()
    db = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    connect_timeout=100,
    autocommit=True
    )
    cursor = db.cursor()

    return db, cursor