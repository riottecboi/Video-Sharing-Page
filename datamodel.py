import mysql.connector
import time

from datetime import datetime

class Datamodel:
    def __init__(self, sqlconfig, retries=3, waitTime=1):
        self.sqlconfig = sqlconfig
        self.retries = retries
        self.waitTime = waitTime

    class MysqlConnector:
        def __init__(self, sqlconfig, retries=3, waitTime=1):
            self.isSuccess = False
            self.cnx = None
            self.cursor = None
            self.sqlconfig = sqlconfig
            self.retries = retries
            self.waitTime = waitTime

        def __enter__(self):
            attempt = 0
            while attempt < self.retries and self.isSuccess == False:
                try:
                    self.cnx = mysql.connector.connect(**self.sqlconfig)
                    self.cursor = self.cnx.cursor()
                    self.isSuccess = True
                    if attempt > 0:  # show logs to inform connection is back
                        print('Retry mysql connection successfully.')
                except Exception as e:
                    print('Warning: Mysql error: "{}" - attempt retrying {}/{} after {} seconds.'.format(e, attempt + 1,
                                                                                                         self.retries,
                                                                                                         self.waitTime))
                    time.sleep(self.waitTime)
                finally:
                    attempt += 1

            if self.isSuccess == True:
                self.isSuccess = False
                return self.cursor, self.cnx
            else:
                return None

        def __exit__(self):
            self.cursor.close()
            self.cnx.close()

    def users(self, email):
        with self.MysqlConnector(self.sqlconfig, self.retries, self.waitTime) as (cursor, conn):
            try:
                query = "SELECT * FROM users WHERE email = %s"
                cursor.execute(query, (email,))
                emailRes = cursor.fetchone()
                if emailRes is not None:
                    return emailRes[1]
                query = "INSERT INTO users (email) VALUES (%s)"
                cursor.execute(query, (email,))
                conn.commit()
                return email

            except Exception as e:
                conn.rollback()
                print(f"Exception occured: {str(e)}")
                return ''

    def url_share(self, url):
        with self.MysqlConnector(self.sqlconfig, self.retries, self.waitTime) as (cursor, conn):
            try:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = "INSERT IGNORE INTO urls (url, created_at) VALUES (%s, %s)"
                cursor.execute(query, (url,current_time))
                conn.commit()
                return True

            except Exception as e:
                conn.rollback()
                print(f"Exception occured: {str(e)}")
                return False