import sys

import sqlite3
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel


class Calc(QWidget):
    def __init__(self):
        super(Calc, self).__init__()
        uic.loadUi('calc_window.ui', self)

        self.con = sqlite3.connect('curr.db')
        self.cur = self.con.cursor()

        self.input_type.addItems(['Доллар', 'Евро', 'Рубль', 'ШвейцарскийФранк', 'ФунтСтерлингов'])
        self.output_type.addItems(['Доллар', 'Евро', 'Рубль', 'ШвейцарскийФранк', 'ФунтСтерлингов'])

        self.input_year.addItems([str(item[0]) for item in self.cur.execute("SELECT year FROM currency").fetchall()])
        self.output_year.addItems([str(item[0]) for item in self.cur.execute("SELECT year FROM currency").fetchall()])

        self.count_btn.clicked.connect(self.convert)

    def convert(self):
        input_val = self.cur.execute(f'''SELECT {self.input_type.currentText()}
                    FROM {'currency'} WHERE year = {self.input_year.currentText()}''').fetchall()[0][0]

        input_val = input_val.replace(',', '.')
        input_val = float(self.input_value.text()) * float(input_val)

        output_val = self.cur.execute(f'''SELECT {self.output_type.currentText()} 
                    FROM {'currency'} WHERE year = {self.output_year.currentText()}''').fetchall()[0][0]

        output_val = output_val.replace(',', '.')
        output = input_val / float(output_val)

        self.output_value.setText(f'{output:.2f}')


class Info:
    def __init__(self, currency, year, month):
        self.con = sqlite3.connect('curr.db')
        self.cur = self.con.cursor()
        self.currency = currency
        self.year = year
        self.month = month

    def return_value(self):
        result = self.cur.execute(f"SELECT {self.month} FROM {self.currency} WHERE year = {self.year}").fetchall()[0][0]
        result = float(result.replace(',', '.'))

        return result


class Curr(QWidget):
    def __init__(self):
        super(Curr, self).__init__()
        uic.loadUi('currency.ui', self)
        self.val_1.clicked.connect(self.dollar_call)
        self.val_2.clicked.connect(self.euro_call)
        self.val_3.clicked.connect(self.gpb_call)
        self.val_4.clicked.connect(self.chf_call)

    def dollar_call(self):
        self.dol = Dollar()
        self.dol.show()

    def euro_call(self):
        self.eur = Euro()
        self.eur.show()

    def gpb_call(self):
        self.gpb = Gpb()
        self.gpb.show()

    def chf_call(self):
        self.chf = Chf()
        self.chf.show()


class Dollar(QWidget):
    def __init__(self):
        super(Dollar, self).__init__()
        uic.loadUi('dollar.ui', self)
        label = QLabel(self)
        pixmap = QPixmap('Доллар.PNG')
        label.setPixmap(pixmap)
        label.move(10, 10)
        label.resize(855, 527)


class Euro(QWidget):
    def __init__(self):
        super(Euro, self).__init__()
        uic.loadUi('euro.ui', self)
        label = QLabel(self)
        pixmap = QPixmap('Евро.PNG')
        label.setPixmap(pixmap)
        label.move(10, 10)
        label.resize(855, 527)


class Rub(QWidget):
    def __init__(self):
        super(Rub, self).__init__()


class Gpb(QWidget):
    def __init__(self):
        super(Gpb, self).__init__()
        uic.loadUi('gpb.ui', self)
        label = QLabel(self)
        pixmap = QPixmap('Фунт стерлингов.PNG')
        label.setPixmap(pixmap)
        label.move(10, 10)
        label.resize(855, 527)


class Chf(QWidget):
    def __init__(self):
        super(Chf, self).__init__()
        uic.loadUi('chf.ui', self)
        label = QLabel(self)
        pixmap = QPixmap('Швейцарский франк.PNG')
        label.setPixmap(pixmap)
        label.move(10, 10)
        label.resize(855, 527)


class SearchWidget(QWidget):
    def __init__(self):
        super(SearchWidget, self).__init__()
        uic.loadUi('search.ui', self)

        self.con = sqlite3.connect('curr.db')
        self.cur = self.con.cursor()
        self.curr_box.addItems(['Доллар', 'Евро', 'Рубль', 'Швейцарский франк', 'Фунт стерлингов'])
        self.year.addItems([str(item[0]) for item in self.cur.execute("SELECT year FROM gpb_info").fetchall()])
        self.month.addItems(['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август',
                             'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'])
        self.search_btn_2.clicked.connect(self.search_func)

    def search_func(self):
        if self.curr_box.currentText() == 'Доллар':
            info = Info('dollar_info', self.year.currentText(), self.month.currentText()).return_value()
            self.text.setText(f'Доллар, {self.month.currentText()} {self.year.currentText()}: {info:.2f}')
        if self.curr_box.currentText() == 'Евро':
            info = Info('euro_info', self.year.currentText(), self.month.currentText()).return_value()
            self.text.setText(f'Евро, {self.month.currentText()} {self.year.currentText()}: {info:.2f}')
        if self.curr_box.currentText() == 'Рубль':
            info = Info('rub_info', self.year.currentText(), self.month.currentText()).return_value()
            self.text.setText(f'Рубль, {self.month.currentText()} {self.year.currentText()}: {info:.2f}')
        if self.curr_box.currentText() == 'Фунт стерлингов':
            info = Info('gpb_info', self.year.currentText(), self.month.currentText()).return_value()
            self.text.setText(f'Фунт стерлингов, {self.month.currentText()} {self.year.currentText()}: {info:.2f}')
        if self.curr_box.currentText() == 'Швейцарский франк':
            info = Info('chf_info', self.year.currentText(), self.month.currentText()).return_value()
            self.text.setText(f'Швейцарский франк, {self.month.currentText()} {self.year.currentText()}: {info:.2f}')


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('project.ui', self)
        self.calc_btn.clicked.connect(self.calc_window)
        self.currency_btn.clicked.connect(self.currency_call)
        self.search_btn.clicked.connect(self.search_call)

    def currency_call(self):
        self.curr = Curr()
        self.curr.show()

    def calc_window(self):
        self.calc = Calc()
        self.calc.show()

    def search_call(self):
        self.search_ = SearchWidget()
        self.search_.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
