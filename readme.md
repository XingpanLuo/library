
# 配置
`python -m pip install --upgrade pip`
`pip3 intall PyQt5`
`pip3 install pymysql`

# 确定安装mysql，并将*/mysql8/bin加入环境变量。启动mysql `mysql -uroot -pustc` ustc是密码.启动一次就可以 `quit`退出。
# 修改database.py中的config
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
