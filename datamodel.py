import mysql.connector
import time
from werkzeug.security import generate_password_hash, check_password_hash
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

        def __exit__(self, exc_type, exc_value, tb):
            self.cursor.close()
            self.cnx.close()

    def users(self, email, password):
        with self.MysqlConnector(self.sqlconfig, self.retries, self.waitTime) as (cursor, conn):
            try:
                query = "SELECT * FROM users WHERE email = %s"
                cursor.execute(query, (email,))
                userRes = cursor.fetchone()
                if userRes is not None:
                    isAuthenticated = check_password_hash(userRes[2], password)
                    return userRes[1], isAuthenticated
                current_time = datetime.now()
                password_hash = generate_password_hash(password)
                query = "INSERT INTO users (email, password_hash, updated) VALUES (%s,%s,%s)"
                cursor.execute(query, (email,password_hash,current_time))
                conn.commit()
                return email, True

            except Exception as e:
                conn.rollback()
                print(f"Exception occured: {str(e)}")
                return '', False

    def url_share(self, url, title, description, user):
        with self.MysqlConnector(self.sqlconfig, self.retries, self.waitTime) as (cursor, conn):
            try:
                current_time = datetime.now()
                query = "INSERT IGNORE INTO urls (url, title, description, updated_by, upload) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (url, title, description, user, current_time))
                conn.commit()

                return True

            except Exception as e:
                conn.rollback()
                print(f"Exception occured: {str(e)}")
                return False

    def get_video_shared(self):
        with self.MysqlConnector(self.sqlconfig, self.retries, self.waitTime) as (cursor, conn):
            results = []
            try:
                query = "SELECT * FROM urls"
                cursor.execute(query)
                urlRes = cursor.fetchall()
                if urlRes is not None:
                    for result in urlRes:
                        url = result[1]
                        if 'watch?v=' in url:
                            url = url.split('watch?v=')[1].split('&')[0]
                        if 'youtu.be' in url:
                            url = url.split('youtu.be/')[1].split('?')[0]
                        results.append({'url': result[1], 'title': result[2], 'description': result[3], 'user': result[4]})
                return results
            except Exception as e:
                conn.rollback()
                print(f"Exception occured: {str(e)}")
                return results