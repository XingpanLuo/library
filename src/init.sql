-- # 此处仅用于初始化数据，且注释必须用分号结尾;
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
INSERT INTO book(
		ID,
		name,
		author,
		price,
		status,
		borrow_Times,
		reserve_Times
	)
VALUES('b1', '数据库系统实现', 'Ullman', 59.0, 1, 4, 1);
INSERT INTO book(
		ID,
		name,
		author,
		price,
		status,
		borrow_Times,
		reserve_Times
	)
VALUES('b2', '数据结构', 'MAL', 70.0, 2, 7, 9);
INSERT INTO book(
		ID,
		name,
		author,
		price,
		status,
		borrow_Times,
		reserve_Times
	)
VALUES('b3', '组成原理', 'zxh', 68.0, 0, 5, 2);
-- # reader;
INSERT INTO reader(ID, name, email, pwd, headshot)
VALUES(
		'r1',
		'lihua',
		'a@qq.com',
		'r1',
		'./headshot/r1.png'
	);
INSERT INTO reader(ID, name, email, pwd, headshot)
VALUES(
		'r2',
		'lilin',
		'b@ustc.edu.cn',
		'password',
		'./headshot/r1.png'
	);
-- # borrow;
INSERT INTO borrow(reader_ID, book_ID, borrow_Date)
VALUES('r1', 'b1', '2023-5-8');
INSERT INTO borrow(reader_ID, book_ID, borrow_Date, return_Date)
VALUES('r2', 'b1', '2023-7-8', '2023-9-30');
-- # reserve;
INSERT INTO reserve(reader_ID, book_ID, reserve_Date, take_Date)
VALUES('r2', 'b1', '2023-4-8', '2023-6-9');
INSERT INTO reserve(reader_ID, book_ID, reserve_Date)
VALUES('r1', 'b2', '2023-5-7');
-- # violation;
INSERT INTO violation(reader_ID, book_ID, borrow_Date)
VALUES('r1', 'b1', '2023-2-9');
