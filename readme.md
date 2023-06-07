# 配置

`python -m pip install --upgrade pip`
`pip3 intall PyQt5`
`pip3 install pymysql`

## mysql

确定安装mysql，并将*/mysql8/bin加入环境变量。启动mysql `mysql -uroot -pustc` ustc是密码.启动一次就可以 `quit`退出。

## 修改database.py中的config

```python
config = {
    "host": '127.0.0.1',
    "user": 'root',
    "pwd": 'ustc',
    "port": 3306,
    "db": 'library'
}
```

一般修改密码pwd就行。mysql端口默认是3306

表：
reader: ID:char(8),name:varchar(10),email:varchar(30),pwd:char(64),headshot:varchar(255)

master: ID:char(8),name:varchar(10),email:varchar(30),pwd:char(64),headshot:varchar(255)

book: ID:char(8),name:varchar(10),author:varchar(10),price:float,status:int,borrow_Times:int,reserve_Times:int

borrow: book_ID:char(8),reader_ID:char(8),borrow_Date:date,return_Date:date

reserve: book_ID:char(8),reader_ID:char(8),reserve_Date:date,take_Date:date

violation: reader_ID:char(8),book_ID(8),borrow_Date:date
