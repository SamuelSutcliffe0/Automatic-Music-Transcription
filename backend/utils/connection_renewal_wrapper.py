def auto_reconnect(func):
    @functools.wraps(func)   
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except errors.OperationalError as e:
            if e.errno == 2013: 
                self.db = mysql.connector.connect(
                host=os.environ.get("DB_HOST"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                database=os.environ.get("DB_NAME"),
                connection_timeout=10,
                autocommit=True
                )
                self.cursor = self.db.cursor()
                return func(self, *args, **kwargs)
            else:
                raise
    return wrapper
