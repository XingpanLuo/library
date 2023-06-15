import pymysql

CONFIG = {
    "host": '127.0.0.1',
    "user": 'root',
    "pwd": 'ustc',
    "port": 3306,
    "db": 'library'
}


def create_procedure_add_book(cursor):
    sql = '''
    CREATE PROCEDURE add_book (
        IN book_id CHAR(8),
        IN book_name VARCHAR(10),
        IN book_author VARCHAR(10),
        IN book_price FLOAT,
        OUT result TEXT
    )
    BEGIN
        DECLARE borrow_times INT DEFAULT 0;
        DECLARE reserve_times INT DEFAULT 0;
        DECLARE status INT DEFAULT 0;
        
        SET borrow_times = FLOOR(RAND() * (7));
        SET reserve_times = FLOOR(RAND() * (11));
        SET status = FLOOR(RAND() * (3));
        
        INSERT INTO book(ID,NAME,AUTHOR,PRICE,BORROW_TIMES,RESERVE_TIMES,STATUS)
        VALUES(book_id, book_name, book_author, book_price, borrow_times, reserve_times, status);
        
    END;
    '''
    cursor.execute(sql)


def create_procedure_delete_book(cursor):
    sql = '''
    CREATE PROCEDURE delete_book (
        IN book_id CHAR(8),
        OUT result BOOL,
        OUT result_str TEXT
    )
    BEGIN
        DECLARE st INT;
        SET result=TRUE;
        SET result_str="delete book";
        SELECT status INTO st
        FROM book
        WHERE ID=book_id;
        -- 删除书籍
        IF st=0 THEN
            DELETE FROM book WHERE ID = book_id;
            SET result=TRUE;
            SET result_str="delete book";
        ELSEIF st=1 THEN
            SET result=FALSE;
            SET result_str="借出书籍不可删除";
        ELSEIF st=2 THEN
            SET result=FALSE;
            SET result_str="预约中书籍不可删除";
        END IF;
        
    END;
    '''
    cursor.execute(sql)


def create_borrow_view(cursor):
    sql = '''
    CREATE VIEW borrow_view AS
    SELECT b.reader_ID, r.name as reader_Name,b.book_ID,  bk.name as book_Name, b.borrow_Date, b.return_Date
    FROM borrow b
    JOIN reader r ON b.reader_ID = r.ID
    JOIN book bk ON b.book_ID = bk.ID;
    '''
    cursor.execute(sql)


def create_reserve_view(cursor):
    sql = '''
    CREATE VIEW reserve_view AS
    SELECT b.reader_ID, r.name as reader_Name,b.book_ID,  bk.name as book_Name, b.reserve_Date, b.take_Date
    FROM reserve b
    JOIN reader r ON b.reader_ID = r.ID
    JOIN book bk ON b.book_ID = bk.ID;
    '''
    cursor.execute(sql)


def create_violation_view(cursor):
    sql = '''
    CREATE VIEW violation_view AS
    SELECT b.reader_ID, r.name as reader_Name,b.book_ID,  bk.name as book_Name, b.borrow_Date
    FROM violation b
    JOIN reader r ON b.reader_ID = r.ID
    JOIN book bk ON b.book_ID = bk.ID;
    '''
    cursor.execute(sql)


def db_init_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reader(
        ID char(8) PRIMARY KEY,
        name varchar(10),
        email varchar(30),
        pwd char(64),
        headshot varchar(255) default './headshot/default.jpg'
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS master(
        ID char(8) PRIMARY KEY,
        name varchar(10),
        email varchar(30),
        pwd char(64),
        headshot varchar(255) default './headshot/default.jpg'
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
    return
    cursor.execute('''
    delimiter \\
    CREATE TRIGGER takedates AFTER INSERT
    ON reserve for each row
    begin
    SELECT book_ID INTO @ID FROM INSERTED ;
    SELECT DATE_ADD((select reserve_Date FROM INSERTED) ,INTERVAL 10 DAY) INTO @TAKE_DATE;
    UPDATE reserve SET take_Date=@TAKE_DATE WHERE book_ID=@ID;
    end;
    \\
    ''')


def db_init_data(cursor):
    # 提交14的新代码
    init_cmds = [
        init_cmd.strip() for init_cmd in open('src/init.sql').read().split(';')
        if init_cmd.strip() != '' and not (init_cmd.strip().startswith('#')
                                           or init_cmd.strip().startswith('-'))
    ]
    for init_cmd in init_cmds:
        # print('execing:', init_cmd)
        cursor.execute(init_cmd)
    return
    # 以下为原来的代码
    # master
    cursor.execute('''
    INSERT
    INTO master (ID,name,pwd,email,headshot)
    VALUES('master', 'master','123456','master@qq.com','./headshot/default.jpg');
    ''')
    # book
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
    # reader
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
    # borrow
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
    # reserve
    cursor.execute('''
    INSERT
    INTO reserve(reader_ID,book_ID,reserve_Date,take_Date)
    VALUES('r2','b1','2023-4-8','2023-6-9') 
    ''')

    cursor.execute('''
    INSERT
    INTO reserve(reader_ID,book_ID,reserve_Date)
    VALUES('r1','b2','2023-5-7') 
    ''')
    # violation
    cursor.execute('''
    INSERT
    INTO violation(reader_ID,book_ID,borrow_Date)
    VALUES('r1','b1','2023-2-9') 
    ''')
