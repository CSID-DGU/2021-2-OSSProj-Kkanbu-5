import pymysql
import bcrypt
        
database = pymysql.connect(   # MySQL connection 연결
            user = 'admin',
            password = 'administer',
            host = 'kkanburis.cdattwopi4a6.ap-northeast-2.rds.amazonaws.com',
            port = 3306,
            db = 'kkanburisDB',
            charset = 'utf8'
        )

def add_id(id_text):
    curs = database.cursor()
    sql = "INSERT INTO users (user_id) VALUES (%s)"
    curs.execute(sql, id_text)
    database.commit()   # 서버로 추가 사항 보내기
    curs.close()

def add_pw(id_text, pw_text):
    hashed_pw = bcrypt.hashpw(pw_text.encode('utf-8'), bcrypt.gensalt())#비밀번호를 encoding해서 type를 byte로 바꿔서 hashpw함수에 넣기
    decode_hash_pw = hashed_pw.decode('utf-8') #비밀번호 확인할 때는 str값으로 받아 매칭해서 비번을 데베에 저장할 때 decoding 해야함
    curs = database.cursor()
    sql = "UPDATE users SET user_pw= %s WHERE user_id=%s"
    curs.execute(sql,(decode_hash_pw,id_text))
    database.commit()
    print(hashed_pw)
    print(decode_hash_pw)

    curs.close()

# 입력받은 아이디가 데이터베이스에 있는지 확인, 아이디와 비밀번호가 일치하는지 확인
# 이 부분 보완 필요
def check_info(id_text, pw_text):
    input_pw = pw_text.encode('utf-8')
    curs = database.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM users WHERE user_id=%s"
    curs.execute(sql ,id_text)
    data = curs.fetchone()  # 리스트 안에 딕셔너리가 있는 형태
    curs.close()
    check_password=bcrypt.checkpw(input_pw,data['user_pw'].encode('utf-8'))
    return check_password

def id_info(id_text):
    global user_id
    user_id = id_text
    return user_id

# 점수 기록 부분
def add_score(game_status,  ID, score): 
    #추가하기
    curs = database.cursor()
    if game_status == 'start':
        sql = "INSERT INTO single_rank (user_id, score) VALUES (%s, %s)"
    
    if game_status == 'pvp':
        sql = "INSERT INTO single_rank (user_id, score) VALUES (%s, %s)"

    curs.execute(sql, (ID, score))
    database.commit()  #서버로 추가 사항 보내기
    curs.close()

# 데이터 베이스에서 데이터 불러오기
def load_rank_data(game_status):
    curs = database.cursor(pymysql.cursors.DictCursor)
    if game_status == 'single':
        sql = "select * from single_rank order by score desc "
    elif game_status == 'pvp':
        sql = "select * from single_rank order by score desc"

    curs.execute(sql)
    data = curs.fetchall()
    curs.close()
    return data