-- # This is only used for initializing data, and comments must end with a semicolon;
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
insert into book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b1', 'DB archive', 'Ullman', 59.0, 2, 2, 0);
insert into book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b2', 'DB concepts', 'Abraham', 59.0, 0, 0,0 );
insert into book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b3', 'C++ Primer', 'Stanley', 78.6, 0, 0, 0);
insert into book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b4', 'Redis design and archive', 'HUANG JIANHONG', 79.0, 0, 0,0);
insert into book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b5', 'Creature', 'John', 114514.00, 0, 0,0);
insert into book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b6', 'Shiji', 'SIMA QIAN', 220.2, 0, 0,0);
insert into book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b7', 'Oracle programming', 'Thomas', 43.1, 0, 0,0);
insert into book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b8', 'Distributed systems', 'Shao Peiying', 30.0, 0, 0,0);
insert into book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b9', 'Oracle management', 'Zhang Lijie', 51.9, 0, 0,0);
insert into book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b10', 'mathematical logic', 'Wang Fangting', 22.0, 0, 0,0);
insert into book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b11', 'THree Body', 'Liu Cixin', 23.0, 0, 0,0);
insert into book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b12', 'Fun python', 'Luciano', 354.2, 0, 0,0);
insert into book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b13', 'Learn SQL', 'Seyed', 23.0, 0, 0,0);
insert into book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b14', 'Perl&MySQL', 'Xu Zeping', 23.0, 0, 0,0);
insert into book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b15', 'Shadows', 'John', 1919.0, 0, 0,0);
insert into book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b16', 'Taste Welcome Wine', 'WoXiuYuan', 810.0, 0, 0,0);
insert into book(ID, name, author, price, status, borrow_Times,reserve_Times) values('b17', 'Sleepy red tea', 'Tiansuo Hao2', 114.0, 0, 0,0);

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
INSERT INTO borrow(reader_ID, book_ID, borrow_Date, return_Date)VALUES('r2', 'b1', '2022-6-8', '2022-6-30');
INSERT INTO borrow(reader_ID, book_ID, borrow_Date)VALUES('r2', 'b2', '2023-6-9');
INSERT INTO borrow(reader_ID, book_ID, borrow_Date)VALUES('r6', 'b17', '2023-6-10');
-- # reserve;
INSERT INTO reserve(reader_ID, book_ID, reserve_Date)VALUES('r1', 'b2', '2023-6-12');
-- # violation;
INSERT INTO violation(reader_ID, book_ID, borrow_Date)VALUES('r1', 'b1', '2023-2-9');
