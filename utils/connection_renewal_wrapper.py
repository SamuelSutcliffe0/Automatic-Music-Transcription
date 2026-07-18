def auto_reconnect(func):
    @functools.wraps(func)   
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except errors.OperationalError as e:
            if e.errno == 2013: 
                print(f"Lost connection in {func.__name__}, reconnecting...")
                self.db, self.cursor = self.website.initiate_db()
                return func(self, *args, **kwargs)
            else:
                raise
    return wrapper
