import sys
import os
import pymysql
import logging
class Database:
    def __init__(self):
        self.score = pymysql.connect(   # MySQL connection 연결
            user = 'admin',
            password = 'administer',
            host = 'kkanburis.cdattwopi4a6.ap-northeast-2.rds.amazonaws.com',
            port = 3306,
            db = 'kkanburisDB',
            charset = 'utf8'
        )

    def connect_RDS(self):
        try:
            cursor = self.score.cursor(pymysql.cursors.DictCursor)

            query = "select * from user_score by score desc"
            cursor.execute(query)
            score_data = cursor.fetchall()
            cursor.close()

            return score_data
        
        except:
            logging.error('RDS에 연결되지 않았습니다.')
            sys.exit(1)

    def add_id_score(self, id, score):
        cursor = self.score.cursor()

        query = "INSERT INTO user_score (id, score) VALUES (%s)"
        cursor.execute(query, (id, score))

        self.score.commit()   # 서버로 추가 정보 전달
        cursor.close()   # connection 닫기

        
