DB_DRIVER = 'mysql'
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = 'rhodes'
DB_NAME = 'rhodes'

DB_DSN = '{driver}://{user}:{passw}@{host}/{name}?charset=utf8&use_unicode=0'.format(driver=DB_DRIVER,
                                                                                     user=DB_USER,
                                                                                     passw=DB_PASS,
                                                                                     host=DB_HOST,
                                                                                     name=DB_NAME)


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'