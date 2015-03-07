DB_DRIVER = 'mysql'
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = ''
DB_NAME = 'rhodes'

DB_DSN = '{driver}://{user}:{passw}@{host}/{name}?charset=utf8'.format(driver=DB_DRIVER,
                                                                       user=DB_USER,
                                                                       passw=DB_PASS,
                                                                       host=DB_HOST,
                                                                       name=DB_NAME)