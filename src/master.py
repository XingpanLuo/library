import sys
import time
import os
import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QGroupBox,
                             QToolButton, QSplitter, QVBoxLayout, QHBoxLayout,
                             QLabel, QTableWidget, QTableWidgetItem,
                             QAbstractItemView, QLineEdit, QFileDialog,
                             QMessageBox, QComboBox)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

try:
    import database
    import book_information
    import reader_information
    import reader
except:
    from src import database
    from src import book_information
    from src import reader_information


class AdministratorPage(QWidget):

    def __init__(self, info):
        super().__init__()
        self.info = info
        self.focus = 0
        self.initUI()

    def initUI(self):
        # 标题栏
        self.titleBar = QWidget()
        self.titleBar.setFixedSize(1250, 50)
        self.setTitleBar()

        # 分割
        self.body = QSplitter()
        self.setLeftMunu()
        self.content = None
        self.setContent()

        self.bodyLayout = QGridLayout()
        self.bodyLayout.addWidget(self.titleBar, 0, 0, 1, 7)
        self.bodyLayout.addWidget(self.body, 1, 0, 7, 7)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.bodyLayout)
        self.setFixedSize(1280, 720)
        self.setMyStyle()

    # 设置标题栏
    def setTitleBar(self):
        self.title = QLabel()
        self.title.setText('图书馆管理系统--管理员')
        self.title.setFixedHeight(30)

        self.account = QToolButton()
        self.account.setText(self.info['ID'])
        self.account.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.account.setFixedHeight(20)
        self.account.setEnabled(False)

        self.out = QToolButton()
        self.out.setText('退出')
        self.out.setFixedHeight(30)

        titleLayout = QHBoxLayout()
        titleLayout.addSpacing(100)
        titleLayout.addWidget(self.title)
        titleLayout.addWidget(self.account)
        titleLayout.addWidget(self.out)
        self.titleBar.setLayout(titleLayout)

    # 左侧菜单栏
    def setLeftMunu(self):
        # 书籍管理
        self.bookManage = QToolButton()
        self.bookManage.setText('图书管理')
        self.bookManage.setFixedSize(160, 50)
        self.bookManage.setIconSize(QSize(30, 30))
        self.bookManage.clicked.connect(
            lambda: self.switch(0, self.bookManage))
        self.bookManage.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # 读者管理
        self.userManage = QToolButton()
        self.userManage.setText('读者管理')
        self.userManage.setFixedSize(160, 50)
        self.userManage.setIconSize(QSize(30, 30))
        self.userManage.clicked.connect(
            lambda: self.switch(1, self.userManage))
        self.userManage.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # 预约信息
        self.reserveManage = QToolButton()
        self.reserveManage.setText('预约信息')
        self.reserveManage.setFixedSize(160, 50)
        self.reserveManage.setIconSize(QSize(30, 30))
        self.reserveManage.clicked.connect(lambda: self.switch(2, self.reserveManage))
        self.reserveManage.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.borrowManage = QToolButton()
        self.borrowManage.setText('借阅信息')
        self.borrowManage.setFixedSize(160, 50)
        self.borrowManage.setIconSize(QSize(30, 30))
        self.borrowManage.clicked.connect(
            lambda: self.switch(3, self.borrowManage))
        self.borrowManage.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # 违期信息
        self.violationManage = QToolButton()
        self.violationManage.setText('违期信息')
        self.violationManage.setFixedSize(160, 50)
        self.violationManage.setIconSize(QSize(30, 30))
        self.violationManage.clicked.connect(
            lambda: self.switch(4, self.borrowManage))
        self.borrowManage.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.btnList = [
            self.bookManage, self.userManage, self.reserveManage, self.borrowManage, self.violationManage
        ]

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.bookManage)
        self.layout.addWidget(self.userManage)
        self.layout.addWidget(self.reserveManage)
        self.layout.addWidget(self.borrowManage)
        self.layout.addWidget(self.violationManage)
        self.layout.addStretch()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.menu = QGroupBox()
        self.menu.setFixedSize(160, 500)
        self.menu.setLayout(self.layout)
        self.menu.setContentsMargins(0, 0, 0, 0)
        self.body.addWidget(self.menu)

    def switch(self, index, btn):
        self.focus = index
        self.setContent()

    # 设置右侧信息页
    def setContent(self):
        if self.content is not None:
            self.content.deleteLater()
        if self.focus == 0:
            self.content = BookManage()
        elif self.focus == 1:
            self.content = ReaderManage()
        elif self.focus == 2:
            self.content = ReserveManage()
        elif self.focus == 3:
            self.content = BorrowManage()
        else:
            self.content = ViolationManage()
        self.body.addWidget(self.content)

    def setMyStyle(self):
        pass


class BookManage(QGroupBox):

    def __init__(self):
        super().__init__()
        self.book_list = []
        self.body = QVBoxLayout()
        self.table = None
        self.setTitleBar()
        self.setSearchBar()
        self.searchFunction()

        self.setLayout(self.body)
        self.initUI()

    # 标题栏
    def setTitleBar(self):
        pass

    # 设置搜索框
    def setSearchBar(self):
        self.selectBox = QComboBox()
        self.selectBox.addItems(['书号', '作者', '书名'])
        self.selectBox.setFixedHeight(30)
        self.searchTitle = QLabel()
        self.searchTitle.setText('搜索书籍')
        self.searchInput = QLineEdit()
        self.searchInput.setText('')
        self.searchInput.setClearButtonEnabled(True)
        self.searchInput.setFixedSize(400, 40)
        self.searchButton = QToolButton()
        self.searchButton.setFixedSize(100, 40)
        self.searchButton.setText('搜索')
        self.searchButton.clicked.connect(self.searchFunction)
        self.addNewBookButton = QToolButton()
        self.addNewBookButton.setFixedSize(170, 40)
        self.addNewBookButton.setText('新增书籍')
        self.addNewBookButton.clicked.connect(self.addNewBookFunction)
        searchLayout = QHBoxLayout()
        searchLayout.addStretch()
        searchLayout.addWidget(self.selectBox)
        searchLayout.addWidget(self.searchTitle)
        searchLayout.addWidget(self.searchInput)
        searchLayout.addWidget(self.searchButton)
        searchLayout.addWidget(self.addNewBookButton)
        searchLayout.addStretch()
        self.searchWidget = QWidget()
        self.searchWidget.setLayout(searchLayout)
        self.body.addWidget(self.searchWidget)

    # 搜索方法
    def searchFunction(self):
        convert = {'书号': 'ID', '作者': 'AUTHOR', '书名': 'NAME'}
        self.book_list = database.search_book(self.searchInput.text(), convert[self.selectBox.currentText()])
        if self.book_list == []:
            print('未找到')
        if self.table is not None:
            self.table.deleteLater()
        self.setTable()

    # 设置表格
    def setTable(self):
        self.table = QTableWidget(1, 8)
        self.table.setContentsMargins(10, 10, 10, 10)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(7, 85)

        self.table.setItem(0, 0, QTableWidgetItem('书号'))
        self.table.setItem(0, 1, QTableWidgetItem('书名'))
        self.table.setItem(0, 2, QTableWidgetItem('作者'))
        self.table.setItem(0, 3, QTableWidgetItem('价格'))
        self.table.setItem(0, 4, QTableWidgetItem('状态'))
        self.table.setItem(0, 5, QTableWidgetItem('借阅数'))
        self.table.setItem(0, 6, QTableWidgetItem('预约数'))
        self.table.setItem(0, 7, QTableWidgetItem('管理'))
        for i in range(8):
            self.table.item(0, i).setTextAlignment(Qt.AlignCenter)
            self.table.item(0, i).setFont(QFont('微软雅黑', 15))

        # 显示借阅详情
        for i in self.book_list:
            self.insertRow(i)
        self.body.addWidget(self.table)

    # 插入行
    def insertRow(self, val: list):
        print(val)
        itemBID = QTableWidgetItem(val[0])
        itemBID.setTextAlignment(Qt.AlignCenter)

        itemBorrowTime = QTableWidgetItem('《' + val[1] + '》')
        itemBorrowTime.setTextAlignment(Qt.AlignCenter)

        itemAUTHOR = QTableWidgetItem(val[2])
        itemAUTHOR.setTextAlignment(Qt.AlignCenter)

        itemPRICE = QTableWidgetItem(str(val[3]))
        itemPRICE.setTextAlignment(Qt.AlignCenter)

        itemSTATUS = QTableWidgetItem(str(val[4]))
        itemSTATUS.setTextAlignment(Qt.AlignCenter)

        itemSUM = QTableWidgetItem(str(val[5]))
        itemSUM.setTextAlignment(Qt.AlignCenter)

        itemRESERVE = QTableWidgetItem(str(val[6]))
        itemRESERVE.setTextAlignment(Qt.AlignCenter)

        itemModify = QToolButton(self.table)
        itemModify.setFixedSize(75, 25)
        itemModify.setText('修改')
        itemModify.clicked.connect(lambda: self.updateBookFunction(val[0]))
        itemDelete = QToolButton(self.table)
        itemDelete.setFixedSize(75, 25)
        itemDelete.setText('删除')
        itemDelete.clicked.connect(lambda: self.deleteBookFunction(val[0]))

        itemLayout = QHBoxLayout()
        itemLayout.setContentsMargins(0, 0, 0, 0)
        itemLayout.addWidget(itemModify)
        itemLayout.addWidget(itemDelete)
        itemWidget = QWidget()
        itemWidget.setLayout(itemLayout)

        self.table.insertRow(1)
        self.table.setItem(1, 0, itemBID)
        self.table.setItem(1, 1, itemBorrowTime)
        self.table.setItem(1, 2, itemAUTHOR)
        self.table.setItem(1, 3, itemPRICE)
        self.table.setItem(1, 4, itemSTATUS)
        self.table.setItem(1, 5, itemSUM)
        self.table.setItem(1, 6, itemRESERVE)

        self.table.setCellWidget(1, 7, itemWidget)

    def updateBookFunction(self, ID: str):
        book_info = database.get_book_info(ID)
        if book_info is None:
            return
        self.updateBookDialog = book_information.BookInfo(book_info)
        self.updateBookDialog.after_close.connect(self.updateBook)
        self.updateBookDialog.show()

    def updateBook(self, book_info: dict):
        ans = database.update_book(book_info)
        if ans:
            self.searchFunction()

    def addNewBookFunction(self):
        self.newBookDialog = book_information.BookInfo()
        self.newBookDialog.show()
        self.newBookDialog.after_close.connect(self.addNewBook)

    def addNewBook(self, book_info: dict):
        ans = database.new_book(book_info)
        if ans:
            self.searchFunction()
        else:
            self.errorBox('新增书籍失败!书籍ID已存在')

    def deleteBookFunction(self, BID: str):
        msgBox = QMessageBox(QMessageBox.Warning, "警告!", '您将会永久删除这本书以及相关信息!',
                             QMessageBox.NoButton, self)
        msgBox.addButton("确认", QMessageBox.AcceptRole)
        msgBox.addButton("取消", QMessageBox.RejectRole)
        if msgBox.exec_() == QMessageBox.AcceptRole:
            ans = database.delete_book(BID)
            if ans[0]:
                self.searchFunction()
            else:
                self.errorBox(ans[1])

    def initUI(self):
        self.setFixedSize(1100, 600)

    def errorBox(self, mes: str):
        msgBox = QMessageBox(
            QMessageBox.Warning,
            "警告!",
            mes,
            QMessageBox.NoButton,
            self
        )
        msgBox.addButton("确认", QMessageBox.AcceptRole)
        msgBox.exec_()


class ReaderManage(QWidget):

    def __init__(self):
        super().__init__()
        self.book_list = []
        self.body = QVBoxLayout()
        self.table = None
        self.setTitleBar()
        self.setSearchBar()
        self.searchFunction()

        self.setLayout(self.body)
        self.initUI()

    # 标题栏
    def setTitleBar(self):
        pass

    # 设置搜索框
    def setSearchBar(self):
        self.searchTitle = QLabel()
        self.searchTitle.setText('搜索读者')
        self.searchInput = QLineEdit()
        self.searchInput.setText('ID/姓名')
        self.searchInput.setClearButtonEnabled(True)
        self.searchInput.setFixedSize(400, 40)
        self.searchButton = QToolButton()
        self.searchButton.setFixedSize(100, 40)
        self.searchButton.setText('搜索')
        self.searchButton.clicked.connect(self.searchFunction)

        searchLayout = QHBoxLayout()
        searchLayout.addStretch()
        searchLayout.addWidget(self.searchTitle)
        searchLayout.addWidget(self.searchInput)
        searchLayout.addWidget(self.searchButton)
        searchLayout.addStretch()

        self.searchWidget = QWidget()
        self.searchWidget.setLayout(searchLayout)
        self.body.addWidget(self.searchWidget)

    # 搜索方法
    def searchFunction(self):
        self.stu_list = database.search_reader(self.searchInput.text())
        if self.stu_list == []:
            print('未找到')
        if self.table is not None:
            self.table.deleteLater()
        self.setTable()

    # 设置表格
    def setTable(self):
        self.table = QTableWidget(1, 6)
        self.table.setContentsMargins(10, 10, 10, 10)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)

        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 175)
        self.table.setColumnWidth(4, 175)
        self.table.setColumnWidth(5, 170)

        self.table.setItem(0, 0, QTableWidgetItem('学号'))
        self.table.setItem(0, 1, QTableWidgetItem('姓名'))
        self.table.setItem(0, 2, QTableWidgetItem('邮箱'))
        self.table.setItem(0, 3, QTableWidgetItem('操作'))

        for i in range(4):
            self.table.item(0, i).setTextAlignment(Qt.AlignCenter)
            self.table.item(0, i).setFont(QFont('微软雅黑', 15))

        # 显示借阅详情
        for i in self.stu_list:
            self.insertRow(i)
        self.body.addWidget(self.table)

    # 插入行
    def insertRow(self, val: list):
        itemRID = QTableWidgetItem(val[0])
        itemRID.setTextAlignment(Qt.AlignCenter)

        itemBorrowTime = QTableWidgetItem(val[1])
        itemBorrowTime.setTextAlignment(Qt.AlignCenter)

        itemEMAIL = QTableWidgetItem(val[2])
        itemEMAIL.setTextAlignment(Qt.AlignCenter)

        itemModify = QToolButton(self.table)
        itemModify.setFixedSize(85, 25)
        itemModify.setText('修改')
        itemModify.clicked.connect(lambda: self.updatereaderFunction(val[0]))

        itemDelete = QToolButton(self.table)
        itemDelete.setFixedSize(85, 25)
        itemDelete.setText('删除')
        itemDelete.clicked.connect(lambda: self.deletereaderFunction(val[0]))

        itemLayout = QHBoxLayout()
        itemLayout.setContentsMargins(0, 0, 0, 0)
        itemLayout.addWidget(itemModify)
        itemLayout.addWidget(itemDelete)
        itemWidget = QWidget()
        itemWidget.setLayout(itemLayout)

        self.table.insertRow(1)
        self.table.setItem(1, 0, itemRID)
        self.table.setItem(1, 1, itemBorrowTime)
        self.table.setItem(1, 2, itemEMAIL)
        self.table.setCellWidget(1, 3, itemWidget)

    def updatereaderFunction(self, ID: str):
        print(ID)
        stu_info = database.get_reader_info(ID)
        # print(stu_info)

        if stu_info is None:
            return
        self.updatereaderDialog = reader_information.readerInfo(stu_info)
        # 这里将关闭窗口时的信息传递到updatereader中
        self.updatereaderDialog.after_close.connect(self.updatereader)
        self.updatereaderDialog.show()

    def updatereader(self, stu_info: dict):
        print(stu_info)
        update_state = 'PWD' in stu_info.keys()
        print(update_state)
        if database.update_reader(stu_info, update_state) is True:
            msgBox = QMessageBox(QMessageBox.Information, "成功", '更新信息成功',
                                 QMessageBox.NoButton, self)
            msgBox.addButton("确认", QMessageBox.AcceptRole)
            msgBox.exec_()
        else:
            msgBox = QMessageBox(QMessageBox.Warning, "错误", '更新信息失败',
                                 QMessageBox.NoButton, self)
            msgBox.addButton("确认", QMessageBox.AcceptRole)
            msgBox.exec_()
        # 修改后刷新界面
        self.searchFunction()

    def deletereaderFunction(self, rid: str):
        msgBox = QMessageBox(QMessageBox.Warning, "警告!", '您将会永久删除此读者以及相关信息!',
                             QMessageBox.NoButton, self)
        msgBox.addButton("确认", QMessageBox.AcceptRole)
        msgBox.addButton("取消", QMessageBox.RejectRole)
        if msgBox.exec_() == QMessageBox.AcceptRole:
            res = database.delete_reader(rid)
            if res is True:
                msgBox = QMessageBox(QMessageBox.Information, "成功", '已删除读者',
                                     QMessageBox.NoButton, self)
                msgBox.addButton("确认", QMessageBox.AcceptRole)
                msgBox.exec_()
            else:
                msgBox = QMessageBox(QMessageBox.Warning, "错误", '删除读者失败，请检查读者是否有未归还的图书',
                                     QMessageBox.NoButton, self)
                msgBox.addButton("确认", QMessageBox.AcceptRole)
                msgBox.exec_()
            self.searchFunction()

    def initUI(self):
        self.setFixedSize(900, 600)


class BorrowManage(QWidget):

    def __init__(self):
        super().__init__()
        self.body = QVBoxLayout()
        self.borrow_list = []
        self.table = None
        # self.setTitleBar()
        self.setSearchBar()
        self.searchFunction()

        self.setLayout(self.body)
        self.initUI()

    # 标题栏
    def setTitleBar(self):
        self.title = QLabel()
        self.title.setText('借阅信息管理')
        self.title.setFixedHeight(25)
        titleLayout = QHBoxLayout()
        titleLayout.addSpacing(50)
        titleLayout.addWidget(self.title)
        self.titleBar = QWidget()
        self.titleBar.setFixedSize(900, 50)
        self.titleBar.setLayout(titleLayout)
        self.body.addWidget(self.titleBar)

    # 设置搜索框
    def setSearchBar(self):
        self.searchTitle = QLabel()
        self.searchTitle.setText('搜索')
        self.searchInput = QLineEdit()
        self.searchInput.setText('ID')
        self.searchInput.setClearButtonEnabled(True)
        self.searchInput.setFixedSize(450, 40)
        self.searchreaderButton = QToolButton()
        self.searchreaderButton.setFixedSize(170, 40)
        self.searchreaderButton.setText('搜索学号')
        self.searchreaderButton.clicked.connect(
            lambda: self.searchFunction('SID'))

        self.searchBookButton = QToolButton()
        self.searchBookButton.setFixedSize(170, 40)
        self.searchBookButton.setText('搜索书号')
        self.searchBookButton.clicked.connect(lambda: self.searchFunction())

        searchLayout = QHBoxLayout()
        searchLayout.addStretch()
        searchLayout.addWidget(self.searchTitle)
        searchLayout.addWidget(self.searchInput)
        searchLayout.addWidget(self.searchreaderButton)
        searchLayout.addWidget(self.searchBookButton)
        searchLayout.addStretch()

        self.searchWidget = QWidget()
        self.searchWidget.setLayout(searchLayout)
        self.body.addWidget(self.searchWidget)

    # 搜索方法
    def searchFunction(self, e: str = 'BID'):
        # 搜索书号
        if e == 'BID':
            self.borrow_list = database.get_borrow_list(
                self.searchInput.text(), True)
        else:
            # 搜索学号
            self.borrow_list = database.get_borrow_list(
                self.searchInput.text())
            self.SID = self.searchInput.text()
        if self.borrow_list == []:
            print('未找到')
            msgbox = QMessageBox()
            msgbox.setText("未找到")
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.exec()
        if self.table is not None:
            self.table.deleteLater()
        self.setTable()

    # 设置表格
    def setTable(self, val: dict = None):
        self.table = QTableWidget(1, 7)
        self.table.setContentsMargins(10, 10, 10, 10)
        self.table.setFixedHeight(500)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setColumnWidth(1, 170)
        self.table.setColumnWidth(2, 170)
        self.table.setColumnWidth(3, 170)
        self.table.setColumnWidth(4, 170)
        self.table.setColumnWidth(5, 170)

        self.table.setItem(0, 0, QTableWidgetItem('读者号'))
        self.table.setItem(0, 1, QTableWidgetItem('读者姓名'))
        self.table.setItem(0, 2, QTableWidgetItem('书号'))
        self.table.setItem(0, 3, QTableWidgetItem('书名'))
        self.table.setItem(0, 4, QTableWidgetItem('借阅日期'))
        self.table.setItem(0, 5, QTableWidgetItem('归还日期'))
        self.table.setItem(0, 6, QTableWidgetItem('归还'))
        for i in range(7):
            self.table.item(0, i).setTextAlignment(Qt.AlignCenter)
            self.table.item(0, i).setFont(QFont('微软雅黑', 15))
        for i in self.borrow_list:
            self.insertRow(i)

        self.body.addWidget(self.table)

    # 插入行
    def insertRow(self, val: list):
        print(val)
        itemRID = QTableWidgetItem(val[0])
        itemRID.setTextAlignment(Qt.AlignCenter)
        itemRName = QTableWidgetItem(val[1])
        itemRName.setTextAlignment(Qt.AlignCenter)
        itemBID = QTableWidgetItem(val[2])
        itemBID.setTextAlignment(Qt.AlignCenter)
        itemBName = QTableWidgetItem(val[3])
        itemBName.setTextAlignment(Qt.AlignCenter)
        try:
            itemBorrowTime = QTableWidgetItem(val[4].strftime('%Y-%m-%d'))
        except:
            itemBorrowTime = QTableWidgetItem('NULL')
        itemBorrowTime.setTextAlignment(Qt.AlignCenter)
        try:
            itemReturnTime = QTableWidgetItem(val[5].strftime('%Y-%m-%d'))
        except:
            itemReturnTime = QTableWidgetItem('NULL')
        itemReturnTime.setTextAlignment(Qt.AlignCenter)

        itemLayout = QHBoxLayout()
        itemLayout.setContentsMargins(0, 0, 0, 0)
        itemWidget = QWidget()
        itemWidget.setLayout(itemLayout)

        self.table.insertRow(1)
        self.table.setItem(1, 0, itemRID)
        self.table.setItem(1, 1, itemRName)
        self.table.setItem(1, 2, itemBID)
        self.table.setItem(1, 3, itemBName)
        self.table.setItem(1, 4, itemBorrowTime)
        self.table.setItem(1, 5, itemReturnTime)
        self.table.setCellWidget(1, 4, itemWidget)
        print(val[5])
        if val[5] == None:
            itemBorrow = QToolButton(self.table)
            itemBorrow.setFixedSize(75, 25)
            itemBorrow.setText("归还")
            itemBorrow.clicked.connect(lambda: self.returnBook(val[0], val[2], 0))
            itemLayout = QHBoxLayout()
            itemLayout.setContentsMargins(0, 0, 0, 0)
            itemLayout.addWidget(itemBorrow)
            itemWidget = QWidget()
            itemWidget.setLayout(itemLayout)
            self.table.setCellWidget(1, 6, itemWidget)


    def returnBook(self, SID: str, BID: str, isPunished: int):
        if isPunished > 0:
            database.pay(BID, SID, isPunished)
        # print(SID)
        # print(BID)
        database.return_book(BID, SID)
        # 刷新表格
        self.searchFunction('BID')

    def initUI(self):
        self.setFixedSize(1000, 600)


class ReserveManage(QWidget):

    def __init__(self):
        super().__init__()
        self.body = QVBoxLayout()
        self.reserve_list = []
        self.table = None
        # self.setTitleBar()
        self.setSearchBar()
        self.searchFunction()

        self.setLayout(self.body)
        self.initUI()

    # 标题栏
    def setTitleBar(self):
        self.title = QLabel()
        self.title.setText('预约信息管理')
        self.title.setFixedHeight(25)
        titleLayout = QHBoxLayout()
        titleLayout.addSpacing(50)
        titleLayout.addWidget(self.title)
        self.titleBar = QWidget()
        self.titleBar.setFixedSize(900, 50)
        self.titleBar.setLayout(titleLayout)
        self.body.addWidget(self.titleBar)

    # 设置搜索框
    def setSearchBar(self):
        self.searchTitle = QLabel()
        self.searchTitle.setText('搜索')
        self.searchInput = QLineEdit()
        self.searchInput.setText('ID')
        self.searchInput.setClearButtonEnabled(True)
        self.searchInput.setFixedSize(450, 40)
        self.searchreaderButton = QToolButton()
        self.searchreaderButton.setFixedSize(170, 40)
        self.searchreaderButton.setText('搜索学号')
        self.searchreaderButton.clicked.connect(
            lambda: self.searchFunction('SID'))

        self.searchBookButton = QToolButton()
        self.searchBookButton.setFixedSize(170, 40)
        self.searchBookButton.setText('搜索书号')
        self.searchBookButton.clicked.connect(lambda: self.searchFunction())

        searchLayout = QHBoxLayout()
        searchLayout.addStretch()
        searchLayout.addWidget(self.searchTitle)
        searchLayout.addWidget(self.searchInput)
        searchLayout.addWidget(self.searchreaderButton)
        searchLayout.addWidget(self.searchBookButton)
        searchLayout.addStretch()

        self.searchWidget = QWidget()
        self.searchWidget.setLayout(searchLayout)
        self.body.addWidget(self.searchWidget)

    # 搜索方法
    def searchFunction(self, e: str = 'BID'):
        # 搜索书号
        if e == 'BID':
            self.reserve_list = database.get_reserve_list(
                self.searchInput.text(), True)
        else:
            # 搜索学号
            self.reserve_list = database.get_reserve_list(
                self.searchInput.text())
            self.SID = self.searchInput.text()
        if self.reserve_list == []:
            print('未找到')
        if self.table is not None:
            self.table.deleteLater()
        self.setTable()

    # 设置表格
    def setTable(self, val: dict = None):
        self.table = QTableWidget(1, 7)
        self.table.setContentsMargins(10, 10, 10, 10)
        self.table.setFixedHeight(500)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setColumnWidth(1, 170)
        self.table.setColumnWidth(2, 170)
        self.table.setColumnWidth(3, 170)
        self.table.setColumnWidth(4, 170)
        self.table.setColumnWidth(5, 170)

        self.table.setItem(0, 0, QTableWidgetItem('读者号'))
        self.table.setItem(0, 1, QTableWidgetItem('读者姓名'))
        self.table.setItem(0, 2, QTableWidgetItem('书号'))
        self.table.setItem(0, 3, QTableWidgetItem('书名'))
        self.table.setItem(0, 4, QTableWidgetItem('预约日期'))
        self.table.setItem(0, 5, QTableWidgetItem('取书日期'))
        for i in range(6):
            self.table.item(0, i).setTextAlignment(Qt.AlignCenter)
            self.table.item(0, i).setFont(QFont('微软雅黑', 15))
        for i in self.reserve_list:
            self.insertRow(i)

        self.body.addWidget(self.table)

    # 插入行
    def insertRow(self, val: list):
        print(val)
        itemRID = QTableWidgetItem(val[0])
        itemRID.setTextAlignment(Qt.AlignCenter)
        itemRName = QTableWidgetItem(val[1])
        itemRName.setTextAlignment(Qt.AlignCenter)
        itemBID = QTableWidgetItem(val[2])
        itemBID.setTextAlignment(Qt.AlignCenter)
        itemBName = QTableWidgetItem(val[3])
        itemBName.setTextAlignment(Qt.AlignCenter)
        try:
            itemBorrowTime = QTableWidgetItem(val[4].strftime('%Y-%m-%d'))
        except:
            itemBorrowTime = QTableWidgetItem('NULL')
        itemBorrowTime.setTextAlignment(Qt.AlignCenter)
        try:
            itemReturnTime = QTableWidgetItem(val[5].strftime('%Y-%m-%d'))
        except:
            itemReturnTime = QTableWidgetItem('NULL')
        itemReturnTime.setTextAlignment(Qt.AlignCenter)

        itemLayout = QHBoxLayout()
        itemLayout.setContentsMargins(0, 0, 0, 0)
        itemWidget = QWidget()
        itemWidget.setLayout(itemLayout)

        self.table.insertRow(1)
        self.table.setItem(1, 0, itemRID)
        self.table.setItem(1, 1, itemRName)
        self.table.setItem(1, 2, itemBID)
        self.table.setItem(1, 3, itemBName)
        self.table.setItem(1, 4, itemBorrowTime)
        self.table.setItem(1, 5, itemReturnTime)
        self.table.setCellWidget(1, 4, itemWidget)

    def retrurnBook(self, SID: str, BID: str, isPunished: int):
        if isPunished > 0:
            database.pay(BID, SID, isPunished)
        ans = database.return_book(BID, SID)
        # 刷新表格
        if ans:
            self.searchFunction('BID')

    def initUI(self):
        self.setFixedSize(1000, 600)


class ViolationManage(QWidget):

    def __init__(self):
        super().__init__()
        self.body = QVBoxLayout()
        self.reserve_list = []
        self.table = None
        # self.setTitleBar()
        self.setSearchBar()
        self.searchFunction()

        self.setLayout(self.body)
        self.initUI()

    # 标题栏
    def setTitleBar(self):
        self.title = QLabel()
        self.title.setText('预约信息管理')
        self.title.setFixedHeight(25)
        titleLayout = QHBoxLayout()
        titleLayout.addSpacing(50)
        titleLayout.addWidget(self.title)
        self.titleBar = QWidget()
        self.titleBar.setFixedSize(900, 50)
        self.titleBar.setLayout(titleLayout)
        self.body.addWidget(self.titleBar)

    # 设置搜索框
    def setSearchBar(self):
        self.searchTitle = QLabel()
        self.searchTitle.setText('搜索')
        self.searchInput = QLineEdit()
        self.searchInput.setText('ID')
        self.searchInput.setClearButtonEnabled(True)
        self.searchInput.setFixedSize(450, 40)
        self.searchreaderButton = QToolButton()
        self.searchreaderButton.setFixedSize(170, 40)
        self.searchreaderButton.setText('搜索学号')
        self.searchreaderButton.clicked.connect(
            lambda: self.searchFunction('SID'))

        self.searchBookButton = QToolButton()
        self.searchBookButton.setFixedSize(170, 40)
        self.searchBookButton.setText('搜索书号')
        self.searchBookButton.clicked.connect(lambda: self.searchFunction())

        searchLayout = QHBoxLayout()
        searchLayout.addStretch()
        searchLayout.addWidget(self.searchTitle)
        searchLayout.addWidget(self.searchInput)
        searchLayout.addWidget(self.searchreaderButton)
        searchLayout.addWidget(self.searchBookButton)
        searchLayout.addStretch()

        self.searchWidget = QWidget()
        self.searchWidget.setLayout(searchLayout)
        self.body.addWidget(self.searchWidget)

    # 搜索方法
    def searchFunction(self, e: str = 'BID'):
        # 搜索书号
        if e == 'BID':
            self.reserve_list = database.get_reserve_list(
                self.searchInput.text(), True)
        else:
            # 搜索学号
            self.reserve_list = database.get_reserve_list(
                self.searchInput.text())
            self.SID = self.searchInput.text()
        if self.reserve_list == []:
            print('未找到')
        if self.table is not None:
            self.table.deleteLater()
        self.setTable()

    # 设置表格
    def setTable(self, val: dict = None):
        self.table = QTableWidget(1, 7)
        self.table.setContentsMargins(10, 10, 10, 10)
        self.table.setFixedHeight(500)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setColumnWidth(1, 170)
        self.table.setColumnWidth(2, 170)
        self.table.setColumnWidth(3, 170)
        self.table.setColumnWidth(4, 170)
        self.table.setColumnWidth(5, 170)

        self.table.setItem(0, 0, QTableWidgetItem('读者号'))
        self.table.setItem(0, 1, QTableWidgetItem('读者姓名'))
        self.table.setItem(0, 2, QTableWidgetItem('书号'))
        self.table.setItem(0, 3, QTableWidgetItem('书名'))
        self.table.setItem(0, 4, QTableWidgetItem('预约日期'))
        for i in range(5):
            self.table.item(0, i).setTextAlignment(Qt.AlignCenter)
            self.table.item(0, i).setFont(QFont('微软雅黑', 15))
        for i in self.reserve_list:
            self.insertRow(i)

        self.body.addWidget(self.table)

    # 插入行
    def insertRow(self, val: list):
        print(val)
        itemRID = QTableWidgetItem(val[0])
        itemRID.setTextAlignment(Qt.AlignCenter)
        itemRName = QTableWidgetItem(val[1])
        itemRName.setTextAlignment(Qt.AlignCenter)
        itemBID = QTableWidgetItem(val[2])
        itemBID.setTextAlignment(Qt.AlignCenter)
        itemBName = QTableWidgetItem(val[3])
        itemBName.setTextAlignment(Qt.AlignCenter)
        try:
            itemBorrowTime = QTableWidgetItem(val[4].strftime('%Y-%m-%d'))
        except:
            itemBorrowTime = QTableWidgetItem('NULL')
        itemBorrowTime.setTextAlignment(Qt.AlignCenter)

        itemLayout = QHBoxLayout()
        itemLayout.setContentsMargins(0, 0, 0, 0)
        itemWidget = QWidget()
        itemWidget.setLayout(itemLayout)

        self.table.insertRow(1)
        self.table.setItem(1, 0, itemRID)
        self.table.setItem(1, 1, itemRName)
        self.table.setItem(1, 2, itemBID)
        self.table.setItem(1, 3, itemBName)
        self.table.setItem(1, 4, itemBorrowTime)
        self.table.setCellWidget(1, 4, itemWidget)

    def retrurnBook(self, SID: str, BID: str, isPunished: int):
        if isPunished > 0:
            database.pay(BID, SID, isPunished)
        ans = database.return_book(BID, SID)
        # 刷新表格
        if ans:
            self.searchFunction('BID')

    def initUI(self):
        self.setFixedSize(1000, 600)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    user_message = {'class': 'master', 'ID': 'master'}
    ex = AdministratorPage(user_message)
    ex.show()
    sys.exit(app.exec_())
