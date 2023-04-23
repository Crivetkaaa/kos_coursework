from main_win import *
from database import DB
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 

import sys


class Interface(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.accept_product = []
        DB.create_table()
        self.update_table()
        self.ui.pushButton.clicked.connect(self.create_report)
        self.ui.pushButton_2.clicked.connect(self.generation_report)

    def else_info(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("TypeError")
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def generation_report(self):
        if len(self.accept_product) > 0:
            text = "SELECT * FROM users WHERE"
            count = 0
            print(self.accept_product)
            for name in self.accept_product:
                if count == 0:
                    text += f" product_name='{name}'"
                    count += 1
                else:
                    text += f" OR product_name='{name}'"
           
            print(text)
            data = DB.execute_res(text=text)
            self.generate_table(data, cheker=True)
        else:
            self.else_info(text='Добавте продукты для отчёта.')        

    def create_num(self, len):
        num = [i for i in range(0, len)]
        return num
    
    def update_combobox(self, data):
        self.ui.comboBox.clear()
        for item in data:
            if item[0] not in self.accept_product:
                self.ui.comboBox.addItem(item[0])

    def update_table(self):
        data = DB.execute_res(text="SELECT * FROM users")
        self.update_combobox(data)
        self.generate_table(data)

    def generate_table(self, data, cheker=False):
        num = self.create_num(len(data))
        
        self.ui.tableWidget.setRowCount(num[-1]+1)
        endd = 0
        end_price = 0
        for i in range(0, len(data)):
            product_name = QtWidgets.QTableWidgetItem(str(data[i][0]))
            product_price = QtWidgets.QTableWidgetItem(str(data[i][1]))
            product_count = QtWidgets.QTableWidgetItem(str(data[i][2]))
            price = data[i][2]*data[i][1]
            end_price += price
            product_prices = QtWidgets.QTableWidgetItem(str(price))
            
            self.ui.tableWidget.setItem(i, 0, product_name)
            self.ui.tableWidget.setItem(i, 1, product_price)
            self.ui.tableWidget.setItem(i, 2, product_count)
            self.ui.tableWidget.setItem(i, 3, product_prices)
            endd = i
        if cheker:
            self.ui.tableWidget.setRowCount(num[-1]+2)

            end = QtWidgets.QTableWidgetItem("Итого:")
            end_prices  = QtWidgets.QTableWidgetItem(str(end_price))
            self.ui.tableWidget.setItem(endd+1, 0, end)
            self.ui.tableWidget.setItem(endd+1, 3, end_prices)
            

    def create_report(self):
        product = self.ui.comboBox.currentText()
        self.accept_product.append(product)
        data = DB.execute_res(text="SELECT * FROM users")
        self.update_combobox(data)
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    mywin = Interface()
    mywin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()