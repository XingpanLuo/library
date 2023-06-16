import time
import pymysql
import pymysql.cursors
# import random
import datetime

try:
    from src import db
except ...:
    import db

CONFIG = {
    "host": '127.0.0.1',
    "user": 'root',
    "pwd": 'ustc',
    "port": 3306,
    "db": 'library'
}


# 检查注册信息
def check_user_info(info: dict) -> dict:
    ans = {'res': 'fail', 'reason': ''}
    if len(info['SID']) > 15:
        ans['reason'] = 'ID长度超过15'
        return ans
    if not info['SID'].isalnum():
        ans['reason'] = 'ID存在非法字符'
        return ans
    if info['PASSWORD'] != info['REPASSWORD']:
        ans['reason'] = '两次输入密码不一致'
        return ans
    ans['res'] = 'seccuss'
    return ans


# 去掉字符串末尾的0
def remove_blank(val):
    if type(val) is not str:
        return val
    while len(val) != 0 and val[-1] == ' ':
        val = val[:-1]
    return val


# 把book元组转换为list
def tuple_to_list(val: list):
    '''
    传入tuple列表把里面的tuple都转换为list同时去掉字符串里的空格
    '''
    ans = []
    for tuple_ in val:
        temp = []
        for item in tuple_:
            temp.append(item)
            if type(temp[-1]) is str:
                temp[-1] = remove_blank(temp[-1])
        ans.append(temp)
    return ans


# 将元组列表转换为字典
def convert(val: list):
    if len(val) == 0:
        return None
    val = val[0]
    # 如果是学生
    # 疑似在某个地方有bug
    if len(val) >= 3:
        ans = {
            'class': 'reader',
            'ID': remove_blank(val[0]),
            'NAME': remove_blank(val[1]),
            'EMAIL': remove_blank(val[2]),
            'headshot': remove_blank(val[-1])
        }
    else:
        ans = {'class': 'master', 'ID': remove_blank(val[0])}
    return ans


def convert_master(val: list):
    print(val)
    if len(val) == 0:
        return None
    val = val[0]
    ans = {
        'class': 'master',
        'ID': remove_blank(val[0]),
        'NAME': remove_blank(val[1]),
        'EMAIL': remove_blank(val[2]),
        'headshot': remove_blank(val[3])
    }
    return ans


# 将日期延后两个月
def postpone(start: str):
    temp = start.split('-')
    temp[0] = int(temp[0])
    temp[1] = int(temp[1])
    temp[2] = int(temp[2])
    temp[1] += 2
    if temp[1] > 12:
        temp[1] -= 12
        temp[0] += 1
    ans = '{:d}-{:0>2d}-{:0>2d}-{}'.format(temp[0], temp[1], temp[2], temp[3])
    return ans


# 两个日期之间间隔的天数
def days_between(start: str, end: str):
    start = start.split('-')
    end = end.split('-')
    start[0] = int(start[0])
    start[1] = int(start[1])
    start[2] = int(start[2])

    end[0] = int(end[0])
    end[1] = int(end[1])
    end[2] = int(end[2])

    s = start[0] * 365 + start[1] * 30 + start[2]
    e = end[0] * 365 + end[1] * 30 + end[2]
    return e - s


# 数据库初始化
def init_database():
    try:
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'])
        cursor = conn.cursor()
        conn.autocommit(True)
        cursor.execute('''DROP DATABASE IF EXISTS library''')
        cursor.execute('''CREATE DATABASE IF NOT EXISTS library''')
        conn.autocommit(False)
        cursor.execute('''
        USE library
        ''')
        db.db_init_table(cursor)
        db.db_init_data(cursor)
        db.create_procedure_add_book(cursor)
        db.create_procedure_delete_book(cursor)
        db.create_borrow_view(cursor)
        db.create_reserve_view(cursor)
        db.create_violation_view(cursor)
        db.create_trigger(cursor)
        conn.commit()
    except Exception as e:
        # print('Init fall 如果数据库已经成功初始化则无视此条警告')
        print(e)
    finally:
        if conn:
            conn.close()


# 注册
def signup(user_message: dict) -> bool:
    '''
    传入以下格式的字典
    user_message{
        'SID': str,
        'PASSWORD': str,
        'SNAME': str,
        'EMAIL': str
    }
    '''
    res = True
    try:
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT *
            FROM reader
            WHERE ID=%s
            ''', (user_message['SID']))
        if len(cursor.fetchall()) != 0:
            raise Exception('用户已存在!')
        cursor.execute(
            '''
        INSERT
        INTO reader (ID, name, email, pwd)
        VALUES(%s, %s, %s, %s)
        ''', (
                user_message['SID'],
                user_message['SNAME'],
                user_message['EMAIL'],
                user_message['PASSWORD'],
            ))
        conn.commit()
    except Exception as e:
        print('Signup error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


# 登录
def signin(user_message: dict) -> dict:
    '''
    传入以下格式的字典
    user_message{
        'ID': str,
        'PWD': str
    }
    如果管理员用户存在返回以下字典
    {
        'class': 'master'
        'AID': str
    }
    如果学生用户存在返回以下格式的字典
    {
        'class': 'stu'
        'SID': str,
        'SNAME': str,
        'DEPARTMENT': str,
        'MAJOR': str,
        'MAX': int
    }
    否则返回None
    '''
    ans = None
    try:
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()
        # 每次登录时，查阅
        cursor.execute(
            "SELECT reader_ID,book_ID, borrow_Date,return_Date FROM borrow WHERE return_Date is NULL"
        )
        # 将读者加入到违期表中
        violation_list = cursor.fetchall()
        for reader_ID, book_ID, borrow_Date, return_Date in violation_list:
            now_time = datetime.datetime.today().date()
            ddl = borrow_Date + datetime.timedelta(days=60)
            if (now_time > ddl) and return_Date is None:
                # 检查是否已经存在记录
                cursor.execute(
                    "SELECT * FROM violation WHERE reader_ID=%s AND book_ID=%s",
                    (reader_ID, book_ID))
                record = cursor.fetchone()
                if record is None:
                    # 如果不存在记录，执行插入操作
                    cursor.execute(
                        "INSERT INTO violation (reader_ID,book_ID,borrow_Date) VALUES (%s,%s,%s)",
                        (reader_ID, book_ID, borrow_Date.strftime('%Y-%m-%d')))

        cursor.execute(
            '''
        SELECT ID
        FROM master
        WHERE ID=%s AND pwd=%s
        ''', (user_message['ID'], user_message['PWD']))
        temp = cursor.fetchall()
        # 管理员表内没有找到则在reader表内匹配
        if len(temp) == 0:
            cursor.execute(
                '''
            SELECT ID, name,email,pwd,headshot
            FROM reader
            WHERE ID=%s AND pwd=%s
            ''', (user_message['ID'], user_message['PWD']))
            temp = cursor.fetchall()
        ans = temp
        conn.commit()
    except Exception as e:
        print('Signin error!')
        print(e)
    finally:
        if conn:
            conn.close()
        try:
            result = convert(ans)
            return result
        except TypeError:
            print('No user found.')
            return None


# 更新学生信息 新增
def update_reader(user_message: dict, state) -> bool:
    '''
    传入字典格式如下
    user_message{
        'ID': str,
        'NAME': str,
        'EMAIL': str,
        'PWD': str,
        'headshot': str
    }
    返回bool
    '''
    try:
        res = True
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()
        print(user_message)
        if state == 1:
            cursor.execute(
                '''
                UPDATE reader
                SET name=%s, email=%s, pwd=%s, headshot=%s
                WHERE ID=%s
                ''', (user_message['NAME'], user_message['EMAIL'],
                      user_message['PWD'], user_message['headshot'],
                      user_message['ID']))
            conn.commit()
        if state == 0:
            cursor.execute(
                '''
                UPDATE reader
                SET name=%s, email=%s, headshot=%s
                WHERE ID=%s
                ''', (user_message['NAME'], user_message['EMAIL'],
                      user_message['headshot'], user_message['ID']))
            conn.commit()
    except Exception as e:
        print('Update error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


def update_master(user_message: dict, state) -> bool:
    '''
    传入字典格式如下
    user_message{
        'ID': str,
        'NAME': str,
        'EMAIL': str,
        'PWD': str,
        'headshot': str
    }
    返回bool
    '''
    try:
        res = True
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()
        print(user_message, state)
        if state == 1:
            cursor.execute(
                '''
                UPDATE master
                SET NAME=%s, EMAIL=%s, PWD=%s, headshot=%s
                WHERE ID=%s
                ''', (user_message['NAME'], user_message['EMAIL'],
                      user_message['PWD'], user_message['headshot'],
                      user_message['ID']))
            conn.commit()
        if state == 0:
            cursor.execute(
                '''
                UPDATE master
                SET name=%s, email=%s, headshot=%s
                WHERE ID=%s
                ''', (user_message['NAME'], user_message['EMAIL'],
                      user_message['headshot'], user_message['ID']))
            conn.commit()
    except Exception as e:
        print('Update error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


# 获取学生信息
def get_reader_info(ID: str) -> dict:
    try:
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT ID, NAME, EMAIL, headshot
            FROM reader
            WHERE ID=%s
            ''', (ID))
        ans = cursor.fetchall()
    except Exception as e:
        print(e)
        print('get reader info error')
    finally:
        if conn:
            conn.close()
        return convert(ans)


def get_master_info(ID: str) -> dict:
    try:
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT ID, NAME, EMAIL, headshot
            FROM master
            WHERE ID=%s
            ''', (ID))
        ans = cursor.fetchall()
    except Exception as e:
        print(e)
        print('get reader info error')
    finally:
        if conn:
            conn.close()
        return convert_master(ans)


# 查找学生
def search_reader(info: str) -> list:
    try:
        res = []
        val = info.split()
        val = [(i, '%' + i + '%') for i in val]
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()
        # 显示所有书信息
        if info == 'ID/姓名' or info == '':
            cursor.execute('''
            SELECT ID, name, email
            FROM reader
            ''')
            res += cursor.fetchall()
        else:
            # 按条件查找
            for i in val:
                cursor.execute(
                    '''
                SELECT ID, name, email
                FROM reader
                WHERE ID=%s OR name LIKE %s
                ''', i)
                res += cursor.fetchall()
        res = list(set(res))
        temp = []
        for i in res:
            temp_ = []
            for j in i:
                temp_.append(remove_blank(j))
            temp.append(temp_)
        res = temp
    except Exception as e:
        print('Search reader error!')
        print(e)
        res = []
    finally:
        if conn:
            conn.close()
        return res


# 删除学生信息
def delete_reader(rid: str) -> bool:
    '''
    传入SID
    删除reader表内记录,
    找出book表内所借的书强制还书
    删除log表内的记录
    '''
    try:
        res = True
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()
        # 先强制把书还掉 new检测是否有在借的书（如果有则不允许删除）
        cursor.execute(
            '''
          SELECT book_ID
           FROM borrow
            WHERE reader_ID=%s and return_Date is NULL
        ''', rid)
        bid_list = cursor.fetchall()
        print(rid)
        print(bid_list)
        if len(bid_list) != 0:
            print(bid_list)
            print("有未归还的书")
            res = False
        # for bid in bid_list:
        #    return_book(bid, rid)
        # 再删除学生信息
        else:
            cursor.execute(
                '''
                DELETE
                FROM reader
                WHERE ID=%s;
                ''', rid)
            conn.commit()
    except Exception as e:
        print('delete book error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


# 获取学生的借书信息
def get_borrow_list(ID: str, BID: bool = False) -> list:
    try:
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()
        if ID == '' or ID == 'ID':
            cursor.execute('''
                SELECT *
                FROM borrow_view;
                ''')
        elif BID is True:
            cursor.execute(
                '''
                SELECT *
                FROM borrow_view
                WHERE book_ID=%s
                ''', ID)
        else:
            cursor.execute(
                '''
                SELECT *
                FROM borrow_view
                WHERE reader_ID=%s
            ''', ID)
        res = cursor.fetchall()
        temp = []
        for i in res:
            temp_ = []
            for j in i:
                temp_.append(remove_blank(j))
            temp.append(temp_)
        res = temp
    except Exception as e:
        print('get borrowing books error!')
        print(e)
        res = []
    finally:
        if conn:
            conn.close()
        return res


# 新增预约函数
def reserve(rid: str, bid: str) -> bool:
    try:
        res = True
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()
        BACK_DATE = time.strftime("%Y-%m-%d-%H:%M")
        cursor.execute(
            '''
            insert into reserve(reader_ID, book_ID, reserve_Date) values(%s,%s,%s)
            ''', (rid, bid, BACK_DATE))
        conn.commit()
    except Exception as e:
        print('get borrowing books error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


# 获取学生的预约信息
def get_reserve_list(ID: str, BID: bool = False) -> list:
    try:
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()
        if ID == '' or ID == 'ID':
            cursor.execute('''
                SELECT *
                FROM reserve_view;
                ''')
        elif BID:
            cursor.execute(
                '''
                SELECT *
                FROM reserve_view
                WHERE book_ID=%s
                ''', ID)
        else:
            cursor.execute(
                '''
                SELECT *
                FROM reserve_view
                WHERE reader_ID=%s
            ''', ID)
        res = cursor.fetchall()
        temp = []
        for i in res:
            temp_ = []
            for j in i:
                temp_.append(remove_blank(j))
            temp.append(temp_)
        res = temp
    except Exception as e:
        print('get borrowing books error!')
        print(e)
        res = []
    finally:
        if conn:
            conn.close()
        return res


def get_violation_list(ID: str, BID: bool = False) -> list:
    try:
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()
        if ID == '' or ID == 'ID':
            cursor.execute('''
                SELECT *
                FROM violation_view;
                ''')
        elif BID:
            cursor.execute(
                '''
                SELECT *
                FROM violation_view
                WHERE book_ID=%s
                ''', (ID))
        else:
            cursor.execute(
                '''
                SELECT *
                FROM violation_view
                WHERE reader_ID=%s
            ''', (ID))
        res = cursor.fetchall()
        temp = []
        for i in res:
            temp_ = []
            for j in i:
                temp_.append(remove_blank(j))
            temp.append(temp_)
        res = temp
    except Exception as e:
        print('get borrowing books error!')
        print(e)
        res = []
    finally:
        if conn:
            conn.close()
        return res


# 还书
def return_book(bid: str, rid: str) -> bool:
    '''
    传入BID, SID，删除borrowing_book表内的记录在log表内新建记录
    返回bool型
    '''
    try:
        res = True
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()
        cursor.execute(
            '''
        SELECT BORROW_DATE
        FROM book, borrow
        WHERE reader_ID=%s AND borrow.book_ID=%s AND borrow.book_ID=book.ID
        ''', (rid, bid))
        # book_mes = cursor.fetchall()
        BACK_DATE = datetime.datetime.now().date()
        # book表内NUM加一，删除borrowing_book表内的记录，把记录插入log表
        # new 更新借阅表中的记录，删除违期表中的记录
        cursor.execute(
            '''
        UPDATE borrow
        SET return_Date=%s
        WHERE reader_ID=%s AND book_ID=%s
        ''', (BACK_DATE, rid, bid))
        cursor.execute(
            '''
        DELETE
        FROM violation
        WHERE reader_ID=%s AND book_ID=%s
        ''', (rid, bid))
        cursor.execute(
            '''
        UPDATE book
        SET status=-3+3*status
        WHERE ID=%s
        ''', bid)
        conn.commit()
    except Exception as e:
        print('Return error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


# 交罚金
def pay(BID: str, SID: str, PUNISH: int) -> bool:
    '''
    传入BID, SID, PUNISH把当前数的DEADLINE往后延长两个月
    返回bool型
    '''
    try:
        res = True
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()

        # book表内NUM加一，删除borrowing_book表内的记录，把记录插入log表
        cursor.execute(
            '''
            UPDATE borrow
            SET DEADLINE=%s, PUNISH=%d
            WHERE BID=%s AND SID=%s
            ''', (postpone(time.strftime('%Y-%m-%d-%H:%M')), PUNISH, BID, SID))
        conn.commit()
    except Exception as e:
        print('Pay error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


# 获取历史记录
def get_log(ID: str, BID: bool = False) -> list:
    try:
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()
        if ID == '' or ID == 'ID':
            cursor.execute('''
                SELECT SID, book.BID, BNAME, BORROW_DATE, BACK_DATE, PUNISHED
                FROM log, book
                WHERE book.BID=log.BID
                ORDER BY BACK_DATE
            ''')
        elif BID:
            cursor.execute(
                '''
                SELECT SID, book.BID, BNAME, BORROW_DATE, BACK_DATE, PUNISHED
                FROM log, book
                WHERE log.BID=%s AND book.BID=log.BID
                ORDER BY BACK_DATE
            ''', (ID, ))
        else:
            cursor.execute(
                '''
                SELECT SID, book.BID, BNAME, BORROW_DATE, BACK_DATE, PUNISHED
                FROM log, book
                WHERE SID=%s AND book.BID=log.BID
                ORDER BY BACK_DATE
            ''', (ID, ))
        res = cursor.fetchall()
    except Exception as e:
        print('get log error!')
        print(e)
        res = []
    finally:
        if conn:
            conn.close()
        temp = []
        for i in res:
            temp_ = []
            for j in i:
                temp_.append(remove_blank(j))
            temp.append(temp_)
        return temp


# 加入新书
def new_book(book_info: dict) -> bool:
    '''
    传入以下格式的字典
    book_msg{
        'ID': str,
        'NAME': str,
        'AUTHOR': str,
        'PRICE': str,
        'BORROW_TIMES': str,
        'RESERVE_TIMES': int,
        'STATUS': str
    }
    返回bool
    '''
    res = True
    try:
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT *
            FROM book
            WHERE ID=%s
            ''', (book_info['ID']))
        if len(cursor.fetchall()) != 0:
            raise Exception('书ID已存在!')

        # 插入新书
        result_args = cursor.callproc('add_book',
                                      args=(book_info['ID'], book_info['NAME'],
                                            book_info['AUTHOR'],
                                            book_info['PRICE'], 0))
        print(result_args)
        conn.commit()
    except Exception as e:
        print('add book error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


# 获取新书详细信息
def get_book_info(ID: str) -> dict:
    '''
    传入ID
    返回book_msg{
        'ID': str,
        'NAME': str,
        'AUTHOR': str,
        'PRICE': str,
        'BORROW_TIMES': str,
        'RESERVE_TIMES': int,
        'STATUS': str
    }
    '''
    try:
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()
        # 获取book表内的书本信息
        cursor.execute(
            '''
            SELECT *
            FROM book
            WHERE ID=%s
            ''', (ID))
        res = cursor.fetchall()
        if len(res) == 0:
            raise Exception('查无此书')

        res = list(res[0])
        key_list = [
            'ID', 'NAME', 'AUTHOR', 'PRICE', 'BORROW_TIMES', 'RESERVE_TIMES',
            'STATUS'
        ]
        ans = {}
        for i, key in zip(res, key_list):
            ans[key] = i
            if type(i) is str:
                ans[key] = remove_blank(i)
        res = ans
    except Exception as e:
        print('get book info error!')
        print(e)
        res = None
    finally:
        if conn:
            conn.close()
        return res


# 更新书籍信息
def update_book(book_info: dict) -> bool:
    try:
        res = True
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()
        # 更新book表
        cursor.execute(
            '''
            UPDATE book
            SET NAME=%s, AUTHOR=%s, PRICE=%s
            WHERE ID=%s
            ''', (book_info['NAME'], book_info['AUTHOR'], book_info['PRICE'],
                  book_info['ID']))

        conn.commit()
    except Exception as e:
        print('Update book error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


def delete_book(ID: str):
    try:
        res = True
        conn = pymysql.connect(
            host=CONFIG['host'],
            user=CONFIG['user'],
            passwd=CONFIG['pwd'],
            port=CONFIG['port'],
            db=CONFIG['db'],
        )
        cursor = conn.cursor()
        cursor.execute("START TRANSACTION")
        # 执行存储过程
        print(ID)
        cursor.callproc('delete_book', args=(ID, "", ""))

        res = cursor.execute("SELECT @_delete_book_1, @_delete_book_2")
        print(res)
        result = cursor.fetchall()

        result_bool = bool(result[0][0])
        result_str = str(result[0][1])
        print(result_bool, result_str)
        # 根据存储过程的返回值来提交或回滚事务
        if not result:
            conn.rollback()
        else:
            conn.commit()

        return result_bool, result_str
    except ...:
        conn.rollback()
        raise
    finally:
        # 恢复自动提交
        conn.autocommit(True)


# 搜索书籍
def search_book(info: str, restrict: str, SID: str = '') -> list:
    '''
    传入搜索信息，并指明BID或AUTHOR或PRESS或BNAME或CLASSIFYICATION进行查找，如果传入SID则匹配这个学生的借书状态
    返回[[BID, BNAME, AUTHOR, PUBLICATION_DATE, PRESS, POSITION, SUM, NUM, CLASSIFICATION, STATE],...]
    '''
    try:
        res = []
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()

        # 显示所有书信息
        if info == 'ID/书名/作者' or info == '':
            cursor.execute('''
            SELECT *
            FROM book;
            ''')
            res = tuple_to_list(cursor.fetchall())
        elif restrict == 'name' or restrict == 'author':
            # AUTHOR或PRESS或BNAME
            info = '\"%' + info + '%\"'
            cursor.execute(f'''
            SELECT *
            FROM book
            WHERE {restrict} LIKE {info}
            ''')
            res = tuple_to_list(cursor.fetchall())
        elif restrict == 'ID':
            # BID
            cursor.execute(
                '''
            SELECT *
            FROM book
            WHERE ID = %s;
            ''', (info))
            res = tuple_to_list(cursor.fetchall())
    except Exception as e:
        print('Search error!')
        print(e)
        res = []
    finally:
        if conn:
            conn.close()
        return res


# 借书
def borrow_book(BID: str, SID: str) -> bool:
    '''
    传入BID和SID
    返回bool
    book的state变成1
    在borrow表内新建记录
    '''
    try:
        res = True
        conn = pymysql.connect(host=CONFIG['host'],
                               user=CONFIG['user'],
                               passwd=CONFIG['pwd'],
                               port=CONFIG['port'],
                               db=CONFIG['db'])
        cursor = conn.cursor()
        BORROW_DATE = time.strftime("%Y-%m-%d-%H:%M")
        # DEADLINE = postpone(BORROW_DATE)

        # book表内NUM减一，新建borrowing_book表内的记录
        cmdline = f'''
        UPDATE book
        SET status=1
        WHERE ID='{BID}'
        '''
        print(cmdline)
        cursor.execute(cmdline)
        cursor.execute(f'''
        INSERT
        INTO borrow (reader_ID,book_ID,borrow_Date)
        VALUES('{SID}', '{BID}', '{BORROW_DATE}')''')
        cursor.execute(
            '''
        DELETE
        FROM reserve
        WHERE reader_ID=%s AND book_ID=%s
                ''', (SID, BID))
        cursor.execute(
            '''
        UPDATE book
        SET borrow_Times = borrow_Times + 1
        WHERE ID = %s
        ''', BID)
        conn.commit()

    except Exception as e:
        print('borrow error!')
        print(e)
        res = False
    finally:
        if conn:
            conn.close()
        return res


# 密码   为了调试方便就先不加密了
def encrypt(val):
    import hashlib
    h = hashlib.sha256()
    password = val
    h.update(bytes(password, encoding='UTF-8'))
    result = h.hexdigest()
    # 注释下面一行即可加密
    result = val
    return result


if __name__ == '__main__':
    pass
