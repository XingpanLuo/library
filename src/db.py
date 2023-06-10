

def create_procedure_add_book(cursor):
    sql='''
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
    sql='''
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
    sql='''
    CREATE VIEW borrow_view AS
    SELECT b.reader_ID, r.name as reader_Name,b.book_ID,  bk.name as book_Name, b.borrow_Date, b.return_Date
    FROM borrow b
    JOIN reader r ON b.reader_ID = r.ID
    JOIN book bk ON b.book_ID = bk.ID;
    '''
    cursor.execute(sql)
    
def create_reserve_view(cursor):
    sql='''
    CREATE VIEW reserve_view AS
    SELECT b.reader_ID, r.name as reader_Name,b.book_ID,  bk.name as book_Name, b.reserve_Date, b.take_Date
    FROM reserve b
    JOIN reader r ON b.reader_ID = r.ID
    JOIN book bk ON b.book_ID = bk.ID;
    '''
    cursor.execute(sql)
    
def create_violation_view(cursor):
    sql='''
    CREATE VIEW violation_view AS
    SELECT b.reader_ID, r.name as reader_Name,b.book_ID,  bk.name as book_Name, b.borrow_Date
    FROM violation b
    JOIN reader r ON b.reader_ID = r.ID
    JOIN book bk ON b.book_ID = bk.ID;
    '''
    cursor.execute(sql)

