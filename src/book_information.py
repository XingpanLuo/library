import sys
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QLabel, QLineEdit, QToolButton, QGroupBox, QMessageBox)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon

KEY_LIST = ['ID', 'NAME', 'AUTHOR',
            'PRICE', 'BORROW_TIMES','RESERVE_TIMES','STATUS']


class BookInfo(QGroupBox):
    '''
    编辑书本信息的界面
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
    after_close = pyqtSignal(dict)

    def __init__(self, book_msg: dict = None):
        super().__init__()
        if book_msg is not None:
            self.book_msg = book_msg
        else:
            self.book_msg = {
                'ID': '图书ID',
                'NAME': '书名',
                'AUTHOR': '作者',
                'PRICE': '价格',
                'BORROW_TIMES': '借阅次数',
                'RESERVE_TIMES': '预约次数',
                'STATUS': '价格'
            }

        self.title = QLabel()
        self.title.setText('编辑书籍信息')

        self.bid=QLabel()
        self.bid.setText('书号')
        
        self.bname=QLabel()
        self.bname.setText('书名')
        
        self.bauthor=QLabel()
        self.bauthor.setText('作者')
        
        self.bprice=QLabel()
        self.bprice.setText('价格')
        # 书号输入框
        self.BIDInput = QLineEdit()
        self.BIDInput.setFixedSize(400, 40)
        self.BIDInput.setText(self.book_msg['ID'])
        self.BIDInput.initText = '图书ID'
        self.BIDInput.mousePRICEEvent = lambda x: self.inputClick(self.BIDInput)

        if self.BIDInput.text() != self.BIDInput.initText:
            self.BIDInput.setEnabled(False)
        # 书名输入框
        self.BNAMEInput = QLineEdit()
        self.BNAMEInput.setFixedSize(400, 40)
        self.BNAMEInput.setText(self.book_msg['NAME'])
        self.BNAMEInput.initText = '请输入书名'
        self.BNAMEInput.mousePRICEEvent = lambda x: self.inputClick(self.BNAMEInput)

        # 作者
        self.AUTHORInput = QLineEdit()
        self.AUTHORInput.setFixedSize(400, 40)
        self.AUTHORInput.setText(self.book_msg['AUTHOR'])
        self.AUTHORInput.initText = '请输入作者'
        self.AUTHORInput.mousePRICEEvent = lambda x: self.inputClick(self.AUTHORInput)

        # 价格
        self.PRICEInput = QLineEdit()
        self.PRICEInput.setFixedSize(400, 40)
        self.PRICEInput.setText(str(self.book_msg['PRICE']))
        self.PRICEInput.initText = '请输入价格'
        self.PRICEInput.mousePRICEEvent = lambda x: self.inputClick(self.PRICEInput)

        # 提交
        self.submit = QToolButton()
        self.submit.setText('提交')
        self.submit.setFixedSize(400, 40)
        self.submit.clicked.connect(self.submitFunction)

        # 退出
        self.back = QToolButton()
        self.back.setText('退出')
        self.back.setFixedSize(400, 40)
        self.back.clicked.connect(self.close)

        self.btnList = [
            self.BIDInput,
            self.BNAMEInput,
            self.AUTHORInput,
            self.PRICEInput
        ]
        self.lableList=[
            self.bid,
            self.bname,
            self.bauthor,
            self.bprice
        ]
        self.bodyLayout = QVBoxLayout()
        self.bodyLayout.addWidget(self.title)
        for i in range(0,len(self.btnList)):
            self.bodyLayout.addWidget(self.lableList[i])
            self.bodyLayout.addWidget(self.btnList[i])
        self.bodyLayout.addWidget(self.submit)
        self.bodyLayout.addWidget(self.back)

        self.setLayout(self.bodyLayout)
        self.initUI()

    def inputClick(self, e):
        for item in self.btnList:
            if item.text() == '':
                item.setText(item.initText)
        if e.text() == e.initText:
            e.setText('')

    def submitFunction(self):
        for btn, key in zip(self.btnList, KEY_LIST):
            if btn.text() == btn.initText:
                self.book_msg[key] = '0'
            else:
                self.book_msg[key] = btn.text()
        self.close()
        self.after_close.emit(self.book_msg)

    def initUI(self):
        self.setFixedSize(422, 550)
        self.setWindowTitle('修改书籍')
    
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



if __name__ == '__main__':
    book_msg = {
                'ID': '4',
                'NAME': 'Java',
                'AUTHOR': 'kak',
                'PRICE': '15',
                'BORROWS_TIMES': '0',
                'RESERVE_TIMES': '0',
                'STATUS': '0'
            }
    app = QApplication(sys.argv)
    ex = BookInfo(book_msg)
    ex.show()
    sys.exit(app.exec_())
