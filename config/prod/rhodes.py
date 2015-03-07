DB_DRIVER = 'mysql'
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = 'gretsch'
DB_NAME = 'rhodes'

DB_DSN = '{driver}://{user}:{passw}@{host}/{name}'.format(driver=DB_DRIVER,
                                                          user=DB_USER,
                                                          passw=DB_PASS,
                                                          host=DB_HOST,
                                                          name=DB_NAME)