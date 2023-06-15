-- # �˴������ڳ�ʼ�����ݣ���ע�ͱ����÷ֺŽ�β;

delimiter \\
CREATE TRIGGER takedates AFTER INSERT
ON reserve for each row
begin
SELECT book_ID INTO @ID FROM INSERTED ;
SELECT DATE_ADD((select reserve_Date FROM INSERTED) ,INTERVAL 10 DAY) INTO @TAKE_DATE;
UPDATE reserve SET take_Date=@TAKE_DATE WHERE book_ID=@ID;
end;
\\

-- # master;
INSERT INTO master (ID, name, pwd, email, headshot)
VALUES(
		'master',
		'master',
		'123456',
		'master@qq.com',
		'./headshot/default.jpg'
	);
-- # book;
insert into Book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b1', '���ݿ�ϵͳʵ��', 'Ullman', 59.0, 4, 2,0);
insert into Book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b2', '���ݿ�ϵͳ����', 'Abraham', 59.0, 0, 0,0);
insert into Book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b3', 'C++ Primer', 'Stanley', 78.6, 0, 0,0);
insert into Book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b4', 'Redis�����ʵ��', '�ƽ���', 79.0, 0, 0,0);
insert into Book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b5', 'Creature', 'John', 114514.00, 0, 0,0);
insert into Book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b6', 'ʷ��(����)', '˾��Ǩ', 220.2, 0, 0,0);
insert into Book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b7', 'Oracle�������', 'Thomas', 43.1, 0, 0,0);
insert into Book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b8', '�ֲ�ʽϵͳ����Ӧ��', '����Ӣ', 30.0, 0, 0,0);
insert into Book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b9', 'Oracle����', '������', 51.9, 0, 0,0);
insert into Book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b10', '�����߼�', '����ͥ', 22.0, 0, 0,0);
insert into Book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b11', '����', '������', 23.0, 0, 0,0);
insert into Book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b12', 'Fun python', 'Luciano', 354.2, 0, 0,0);
insert into Book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b13', 'Learn SQL', 'Seyed', 23.0, 0, 0,0);
insert into Book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b14', 'Perl&MySQL', '����ƽ', 23.0, 0, 0,0);
insert into Book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b15', 'Shadows', 'John', 1919.0, 0, 0,0);
insert into Book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b16', 'Ʒ��ӭ����', '����Ժ', 810.0, 0, 0,0);
insert into Book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b17', '��˯���', '�����ƶ�', 114.0, 0, 0,0);

-- # reader;
INSERT INTO reader(ID, name, email, pwd, headshot)VALUES('r1','lihua','a@qq.com','r1','./headshot/r1.png');
INSERT INTO reader(ID, name, email, pwd, headshot)VALUES('r2','lilin','b@ustc.edu.cn','password','./headshot/default.png');
INSERT INTO reader(ID, name, email, pwd, headshot)VALUES('r3','zs','c@qq.com','r3','./headshot/default.png');
INSERT INTO reader(ID, name, email, pwd, headshot)VALUES('r4','ls','d@ustc.edu.cn','password','./headshot/default.png');
INSERT INTO reader(ID, name, email, pwd, headshot)VALUES('r5','ww','e@qq.com','r5','./headshot/default.png');
INSERT INTO reader(ID, name, email, pwd, headshot)VALUES('r6','a','f@ustc.edu.cn','password','./headshot/default.png');
INSERT INTO reader(ID, name, email, pwd, headshot)VALUES('r7','b','g@qq.com','r7','./headshot/default.png');
INSERT INTO reader(ID, name, email, pwd, headshot)VALUES('r8','c','h@ustc.edu.cn','password','./headshot/r1.png');

-- # borrow;
INSERT INTO borrow(reader_ID, book_ID, borrow_Date)VALUES('r1', 'b1', '2023-2-9');
INSERT INTO borrow(reader_ID, book_ID, borrow_Date, return_Date)VALUES('r2', 'b1', '2023-6-8', '2023-6-30');
-- # reserve;
INSERT INTO reserve(reader_ID, book_ID, reserve_Date)VALUES('r1', 'b2', '2023-6-12');
-- # violation;
INSERT INTO violation(reader_ID, book_ID, borrow_Date)VALUES('r1', 'b1', '2023-2-9');
