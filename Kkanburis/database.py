import pymysql
import bcrypt
from cryptography.fernet import Fernet 
        
database = pymysql.connect(   # MySQL connection 연결
            user = 'admin',
            password = 'administer',
            host = 'kkanburis.cdattwopi4a6.ap-northeast-2.rds.amazonaws.com',
            port = 3306,
            db = 'kkanburisDB',
            charset = 'utf8'
        )

# 회원가입 시 이미 존재하는 ID인지 확인
def exist_id(id_text):
    curs = database.cursor()
    sql = "SELECT * FROM users WHERE user_id = %s "
    curs.execute(sql, id_text)
    existID = curs.fetchone()
    curs.close()
    if existID:
        return True   # 입력한 ID에 해당하는 사용자가 이미 users 테이블에 존재
    else:
        return False   # 입력한 ID에 해당하는 사용자가 이미 users 테이블에 존재하지 X

# 회원가입 시 사용자 등록을 위해 ID 추가
def add_id(id_text):
    if not exist_id(id_text):
        curs = database.cursor()
        sql = "INSERT INTO users (user_id) VALUES (%s)"
        curs.execute(sql, id_text)
        database.commit()   # 서버로 추가 사항 보내기
        curs.close()
    else:
        pass   # 이미 존재하는 ID 이미지 출력

# 회원가입 시 사용자 등록을 위해 ID에 해당하는 비밀번호 추가
def add_pw(id_text, pw_text):
    hashed_pw = bcrypt.hashpw(pw_text.encode('utf-8'), bcrypt.gensalt())   # 비밀번호를 encoding해서 type를 byte로 바꿔서 hashpw 함수에 넣기
    decode_hash_pw = hashed_pw.decode('utf-8')   # 비밀번호 확인할 때는 str값으로 받아 매칭해서 비번을 데베에 저장할 때 decoding 해야함
    curs = database.cursor()
    sql = "UPDATE users SET user_pw= %s WHERE user_id=%s"
    curs.execute(sql,(decode_hash_pw,id_text))
    database.commit()
    
    print(hashed_pw)
    print(decode_hash_pw)
    curs.close()

def add_pw2(id_text, pw_text):
    curs = database.cursor()
    sql = "UPDATE users SET user_pw= %s WHERE user_id=%s"
    curs.execute(sql,(pw_text,id_text))
    database.commit()
    curs.close()

# 입력받은 아이디가 데이터베이스에 있는지 확인, 아이디와 비밀번호가 일치하는지 확인
def check_info(id_text, pw_text):
    input_pw = pw_text.encode('utf-8')
    curs = database.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM users WHERE user_id=%s"
    curs.execute(sql ,id_text)
    data = curs.fetchone()  # 리스트 안에 딕셔너리가 있는 형태
    curs.close()
    check_password = bcrypt.checkpw(input_pw, data['user_pw'].encode('utf-8'))
    
    # 수정
    input_hashed_pw = bcrypt.hashpw(input_pw, bcrypt.gensalt())
    input_decode_hashed_pw = input_hashed_pw.decode('utf-8')
    # if input_decode_hashed_pw == data['user_pw']:
    #     check_password = True
    # else:
    #     check_password = False

    print('input_pw : ', input_pw, ' type : ',type(input_pw))
    print('check_password : ', check_password)
    print("data['user_pw'] : ", data['user_pw'], ' type : ',type(data['user_pw']))
    print("data['user_pw'].encode('utf-8') : ", data['user_pw'].encode('utf-8'), ' type : ', type(data['user_pw'].encode('utf-8')))
    
    return check_password

def check_info2(id_text, pw_text):
    curs = database.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM users WHERE user_id=%s"
    curs.execute(sql ,id_text)
    data = curs.fetchone()  # 리스트 안에 딕셔너리가 있는 형태
    curs.close()
    if pw_text == data['user_pw']:
        check_password = True
    else:
         check_password = False
    return  check_password

def id_info(id_text):
    global user_id
    user_id = id_text
    return user_id

# 사용자의 점수 기록이 존재하는지 확인
def exist_score(id_text):
    curs = database.cursor()
    sql = "SELECT * FROM single_rank WHERE user_id = %s "
    curs.execute(sql, id_text)
    existScore = curs.fetchone()
    curs.close()
    if existScore:
        return True   # 입력한 ID에 해당하는 사용자가 기존 점수 기록 존재
    else:
        return False   # 입력한 ID에 해당하는 사용자가 기존 점수 기록 X

# 점수 기록 부분
def add_score(id_text, score): 
    # score 기록이 없는 사용자는 추가하고, score 기록이 있는 사용자는 등록된 score와 게임에서 얻은 score 중 높은 것으로 update 하기
    # score 테이블에서 id_text에 해당하는 사용자 데이터 있는지 확인
    if exist_id(id_text):   # 아이디가 존재하고
        if exist_score(id_text):   # 아이디에 해당하는 사용자 점수 기록이 있는 경우 - 최고 기록으로 업데이트
            curs = database.cursor()
            sql = "SELECT score from single_rank where user_id = %s"
            curs.execute(sql, id_text)
            data = curs.fetchone()
            print(data)
            if score > data[0]:   # 획득한 점수가 기존 등록된 score보다 큰 경우 -> update
                sql = "UPDATE single_rank set score = %s where user_id = %s"
                curs.execute(sql, (score, id_text))
                database.commit()
                curs.close()
            else:
                pass

        else:   # 아이디에 해당하는 사용자 점수 기록이 없는 경우
            curs = database.cursor()
            sql = "INSERT INTO single_rank (user_id, score) VALUES (%s, %s)"   # game_status 구분 X
            curs.execute(sql, (id_text, score))
            database.commit()  #서버로 추가 사항 보내기
            curs.close()  
    else:
        pass

# 데이터 베이스에서 데이터 불러오기
def load_rank_data():
    curs = database.cursor(pymysql.cursors.DictCursor)
    sql = "select * from single_rank order by score desc limit 5 "
    curs.execute(sql)
    data = curs.fetchall()
    curs.close()
    return data
class SimpleEnDecrypt:
    def __init__(self, key=None):
        if key is None:   # 키가 없다면
            key = Fernet.generate_key()   # 키를 생성
        self.key = key
        self.f   = Fernet(self.key)
    
    def encrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.f.encrypt(data)   # 바이트 형태이면, 바로 암호화
        else:
            ou = self.f.encrypt(data.encode('utf-8'))   # 인코딩 후 암호화
        if is_out_string is True:
            return ou.decode('utf-8') # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou
        
    def decrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.f.decrypt(data)   # 바이트 형태이면, 바로 복호화
        else:
            ou = self.f.decrypt(data.encode('utf-8'))   # 인코딩 후 복호화
        if is_out_string is True:
            return ou.decode('utf-8')   # 출력이 문자열이면, 디코딩 후 반환
        else:
            return ou

simpleEnDecrypt = SimpleEnDecrypt()

encrypt_pw = simpleEnDecrypt.encrypt('smegyeong')
def new_add_pw(id_text, pw_text):
    global encrypt_pw
    encrypt_pw = simpleEnDecrypt.encrypt(pw_text)
    curs = database.cursor()
    sql = "UPDATE users SET user_pw = %s WHERE user_id = %s"
    curs.execute(sql, (encrypt_pw, id_text))
    database.commit()
    curs.close()

def new_check_info(id_text, pw_text):
    # decrypt_pw = enDecrypt.decrypt(encrypt_pw)
    curs = database.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM users WHERE user_id = %s"
    curs.execute(sql ,id_text)
    user_data = curs.fetchone()  # 리스트 안에 딕셔너리가 있는 형태
    curs.close()
    decrypt_pw = simpleEnDecrypt.decrypt(user_data['user_pw'])

    print('확인용')
    print('user_data : ', user_data)
    print('pw_text : ', pw_text, 'type : ', type(pw_text))
    print('encrypt_pw : ' , encrypt_pw, 'type : ', type(encrypt_pw))
    print('decrypt_pw : ', decrypt_pw, 'type : ', type(decrypt_pw))
    if pw_text == decrypt_pw:
        check_password = True
    else:
        check_password = False

    print(check_password)
    
    return check_password

# new_check_info('sim', 'simmigyeong')
# new_check_info('smegyeong', 'smegyeong')