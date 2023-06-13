import time
import pymysql
import pymysql.cursors
import random
try:
    from src import db
except:
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
    if info['PWD'] != info['REPWD']:
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
    if len(val) >= 3:
        ans = {
            'class': 'reader',
            'ID': remove_blank(val[0]),
            'NAME': remove_blank(val[1]),
            'EMAIL': remove_blank(val[2])
        }
    else:
        ans = {'class': 'master', 'ID': remove_blank(val[0])}
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
        cursor.execute('''DROP DATABASE library''')
        cursor.execute('''CREATE DATABASE IF NOT EXISTS library''')
        conn.autocommit(False)
        cursor.execute('''
        USE library
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS reader(
            ID char(8) PRIMARY KEY,
            name varchar(10),
            email varchar(30),
            pwd char(64),
            headshot varchar(255)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS master(
            ID char(8) PRIMARY KEY,
            name varchar(10),
            pwd char(64)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS book(
            ID char(8) PRIMARY KEY,
            name varchar(10),
            author varchar(10),
            price float,
            status int,
            borrow_Times int,
            reserve_Times int
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrow(
            reader_ID char(8),
            book_ID char(8),
            borrow_Date date,
            return_Date date,
            PRIMARY KEY(book_ID, reader_ID)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS reserve(
            reader_ID char(8),
            book_ID char(8),
            reserve_Date date,
            take_Date date,
            PRIMARY KEY(book_ID, reader_ID)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS violation(
            reader_ID char(8),
            book_ID char(8),
            borrow_Date date,
            PRIMARY KEY(reader_ID, book_ID, borrow_Date)
        );
        ''')
        cursor.execute('''
        INSERT
        INTO master (ID,name,pwd)
        VALUES('master', 'master','123456');
        ''')
        # book: ID:char(8),name:varchar(10),author:varchar(10),price:float,status:int,borrow_Times:int,reserve_Times:int
        cursor.execute('''
        INSERT
        INTO book(ID, name, author, price, status, borrow_Times,reserve_Times)
        VALUES('b1', '数据库系统实现', 'Ullman', 59.0, 1, 4,1);
        ''')
        cursor.execute('''
        INSERT 
        INTO book(ID, name, author, price, status, borrow_Times,reserve_Times) 
        VALUES('b2', '数据结构', 'MAL', 70.0, 2,7,9);
        ''')
        cursor.execute('''
        INSERT 
        INTO book(ID, name, author, price, status, borrow_Times,reserve_Times) 
        VALUES('b3', '组成原理', 'zxh', 68.0, 0,5,2);
        ''')
        cursor.execute('''
        INSERT
        INTO reader(ID,name,email,pwd,headshot)
        VALUES('r1', 'lihua', 'a@qq.com', 'r1', './headshot/r1.png');
        ''')

        cursor.execute('''
        INSERT
        INTO reader(ID,name,email,pwd,headshot)
        VALUES('r2', 'lilin', 'b@ustc.edu.cn', 'password', './headshot/r1.png');
        ''')

        cursor.execute('''
        INSERT
        INTO borrow(reader_ID,book_ID,borrow_Date)
        VALUES('r1','b1','2023-5-8') 
        ''')

        cursor.execute('''
        INSERT
        INTO borrow(reader_ID,book_ID,borrow_Date,return_Date)
        VALUES('r2','b1','2023-7-8','2023-9-30') 
        ''')
        db.create_procedure_add_book(cursor)
        db.create_procedure_delete_book(cursor)
        db.create_borrow_view(cursor)
        db.create_reserve_view(cursor)
        db.create_violation_view(cursor)
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
        'PWD': str,
        'SNAME': str,
        'DEPARTMENT': str,
        'MAJOR': str,
        'MAX': int
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
            WHERE SID=%s
            ''', (user_message['SID']))
        if len(cursor.fetchall()) != 0:
            raise Exception('用户已存在!')
        cursor.execute(
            '''
        INSERT
        INTO reader
        VALUES(%s, %s, %s, %s, %s, %s)
        ''', (user_message['SID'], user_message['PWD'], user_message['SNAME'],
              user_message['DEPARTMENT'], user_message['MAJOR'],
              str(user_message['MAX'])))
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


# 更新学生信息
def update_reader(user_message: dict) -> bool:
    '''
    传入字典格式如下
    user_message{
        'ID': str,
        'NAME': str,
        'EMAIL': str,
        'DEPARTMENT': str,
        'MAJOR': str,
        'MAX': int
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
        cursor.execute(
            '''
            UPDATE reader
            SET NAME=%s, EMAIL=%s
            WHERE ID=%s
            ''',
            (user_message['NAME'], user_message['email'], user_message['ID']))
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
            SELECT ID, NAME, EMAIL
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
def delete_reader(SID: str) -> bool:
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
        # 先强制把书还掉
        cursor.execute(
            '''
            SELECT BID
            FROM borrowing_book
            WHERE SID=%s
        ''', (SID))
        BID_list = cursor.fetchall()
        for BID in BID_list:
            return_book(BID, SID)
        # 再删除学生信息
        cursor.execute(
            '''
            DELETE
            FROM reader
            WHERE SID=%s
            DELETE
            FROM log
            WHERE SID=%s
            ''', (SID, SID))
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
        elif BID:
            cursor.execute(
                '''
                SELECT *
                FROM borrow_view
                WHERE book_ID=%s
                ''', (ID))
        else:
            cursor.execute(
                '''
                SELECT *
                FROM borrow_view
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
                ''', (ID))
        else:
            cursor.execute(
                '''
                SELECT *
                FROM reserve_view
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
def return_book(BID: str, SID: str) -> bool:
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
        # 先把借书日期，书本剩余数量，罚金等信息找出
        cursor.execute(
            '''
        SELECT BORROW_DATE, NUM, PUNISH
        FROM book, borrowing_book
        WHERE SID=%s AND borrowing_book.BID=%s AND borrowing_book.BID=book.BID
        ''', (SID, BID))
        book_mes = cursor.fetchall()
        NUM = book_mes[0][1]
        BORROW_DATE = book_mes[0][0]
        PUNISH = book_mes[0][2]
        BACK_DATE = time.strftime("%Y-%m-%d-%H:%M")

        # book表内NUM加一，删除borrowing_book表内的记录，把记录插入log表
        cursor.execute(
            '''
        UPDATE book
        SET NUM=%d
        WHERE BID=%s
        DELETE
        FROM borrowing_book
        WHERE SID=%s AND BID=%s
        INSERT
        INTO log
        VALUES(%s, %s, %s, %s, %d)
        ''',
            (NUM + 1, BID, SID, BID, BID, SID, BORROW_DATE, BACK_DATE, PUNISH))
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
            UPDATE borrowing_book
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
    except:
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
        # 先把借书日期，书本剩余数量，罚金等信息找出
        # cursor.execute(
        #     '''
        # SELECT NUM
        # FROM book
        # WHERE BID=%s
        # ''', (BID))
        # book_mes = cursor.fetchall()
        # # print(book_mes)
        # NUM = book_mes[0][0]
        BORROW_DATE = time.strftime("%Y-%m-%d-%H:%M")
        DEADLINE = postpone(BORROW_DATE)

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
        INTO borrow
        VALUES('{BID}', '{SID}', '{BORROW_DATE}', '{DEADLINE}')''')
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
    # temp = {
    #     'SID': '201603',
    #     'PWD': 'ustc',
    #     'SNAME': '小王',
    #     'DEPARTMENT': '数学与信息科学学院',
    #     'MAJOR': 'SE',
    #     'MAX': 5,
    #     'PUNISHED': 0
    # }
    # user_message = {
    #     'SID': '1',
    #     'SNAME': '1',
    #     'PWD': '123456',
    #     'DEPARTMENT': '1',
    #     'MAJOR': '2',
    #     'MAX': 5
    # }
    # temp_login = {'ID': '1', 'PWD': 'ustc'}
    # book_msg = {
    #     'BID': '444',
    #     'BNAME': 'Java',
    #     'AUTHOR': 'kak',
    #     'PUBLICATION_DATE': '2009-05',
    #     'PRESS': '电子出版社',
    #     'POSITION': 'C05',
    #     'SUM': 5,
    #     'CLASSIFICATION': 'a s ad das d'
    # }
    # 注册测试
    # print(signup(temp))

    # 还书测试
    # print(get_borrow_list('', True))
    # print(return_book('0001', '1'))
    # print(get_borrow_list('1'))

    # 登录测试
    # print(signin(temp_login))

    # 查书测试
    # print(search_book('3', 'CLASSIFICATION'))

    # 推迟日期方法测试
    # print(postpone('2019-7-5-10:58'))

    # 借书测试
    # print(borrow_book('2', '1'))

    # 获取借书日志测试
    # print(get_log('1', True))

    # 更新学生信息测试
    # print(update_reader(user_message))

    # 加入新书测试
    # print(new_book(book_msg))

    # 获取书本详细信息
    # print(get_book_info('444'))

    # 删除书籍
    # print(delete_book('3'))

    # 查找学生
    # print(search_reader('a 1'))

    # 获取学生信息
    # print(get_reader_info('1'))

    # 删除学生
    # print(delete_reader('3'))

    # 初始化数据库
    # init_database()
