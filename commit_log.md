# 提交说明

## 提交1 by xyp

1. 你这都没有 student 表还到处 student，我直接全替换成 reader
2. `database.py` 的 `remove_blank` 可以用 strip 方法替代。
3. 代码使用sql语句有一堆大小写问题，我基本上能改的都给改了。
4. 我的 pylint 可能不太一样，我全都重新格式化了，Markdown 也修改了一些 lint 报错。
5. database.py 的 334 行可能因为查询不到产生 NoneType，这里做了 catch 修改。
6. 同一文件 323 行的 sql 语句应该有小的引号。
7. import 未引用的我都删了（因为我这边 pylint 到处报错）
8. reader 的 lilin 我改成了 lihua

## 提交2 by xyp

1. 修改 `main_widget.py` 的 90 行增加了 reader 内容。
2. 修改 database 211,972,980 行数据错误。
3. 修改 main_widget.py

## 提交3 by xyp

1. 修改 database.py 的 search_book 逻辑

（有事暂时离开，先只提交一点）

## 提交4 by xyp

1. database.py 判断 master 逻辑错误

## 提交5 by xyp

1. 完成 reader.py 的前两个 UI 编写

## 提交6 by xyp

1. 完成读者全部 UI
2. 修复 database.py 的 update_reader 的 bug

## 提交7 by zcm

1. 新建数据库的逻辑更新
2. 更改database.py 中的一些sql语句使其符合本项目数据库设计（但不多）

## 提交8 by zcm

1. database，py的update_reader新增参数state，为1则更新密码，为0则不更新
2. 由1，更新reader.py中修改个人信息的相关部分

## 提交9 by zcm

1. 管理员界面的学生信息更新功能完成

## 借阅逻辑

1. 对某本书借书的条件：

   - 读者没有违期
   - 书籍处于状态0（在馆可借）或状态3（在馆被预约）且预约人为本人

   对应动作为：

   - 添加借书记录，如果书是状态3则删除预约记录
   - 对状态0，修改状态为1（借出无预约）
   - 对状态3，如果没有其他预约，那么修改状态为1（借出无预约）；如果有其他预约，修改状态为2（借出有预约）

2. 对某本书可预约的条件：

   - 读者没有违期
   - 书籍当前没有被读者借阅
   - 书籍状态为1（借出无预约）或状态2/3（有预约）

   对应动作为：

   - 添加预约记录
   - 对状态1，修改书的状态为2
   - 对状态2/3，书的状态不变

3. 对某本书可还书的条件：

   - 书籍被读者借阅

   对应动作为：

   - 修改借阅记录
   - 书状态1变0，2变3
   - 如有违期则要求缴纳罚款
