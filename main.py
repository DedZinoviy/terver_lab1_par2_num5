from typing import Type
from unittest import result
from PyQt5 import QtWidgets
from ui import Ui_MainWindow
import sys
from combinatoric import Combinatoric

class mywindow(QtWidgets.QMainWindow):

    '''Конструктор главного окна'''
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.m_spinBox.editingFinished.connect(self.enter)
        self.ui.resultButton.clicked.connect(self.solve)

    def enter(self):
        m = self.ui.m_spinBox.value()
        self.ui.n_table.setRowCount(m)
        self.ui.k_table.setRowCount(m)
        for i in range(m):
            n_item = QtWidgets.QTableWidgetItem("n_" + str(i + 1))
            self.ui.n_table.setVerticalHeaderItem(i, n_item)
            self.ui.n_table.setItem(i, 0, QtWidgets.QTableWidgetItem("0"))
            k_item = QtWidgets.QTableWidgetItem("k_" + str(i + 1))
            self.ui.k_table.setVerticalHeaderItem(i, k_item)
            self.ui.k_table.setItem(i, 0, QtWidgets.QTableWidgetItem("0"))


    def solve(self):
        k = self.ui.k_spinBox.value()
        n = self.ui.n_spinBox.value()
        m = self.ui.m_spinBox.value()
        if n > k:
            QtWidgets.QMessageBox.information(self, "Ошибка", "n не может быть больше k")
            return
        elif m > k:
            QtWidgets.QMessageBox.information(self, "Ошибка", "m не может быть больше k")
            return
        
        k_sum = 0
        n_sum = 0
        for i in range(m):
            k_value = self.ui.k_table.item(i, 0).text()
            n_value = self.ui.n_table.item(i, 0).text()
            if not k_value.isnumeric():
                QtWidgets.QMessageBox.information(self, "Ошибка", k_value + " не является числом")
                return
            elif int(k_value) <= 0:
                QtWidgets.QMessageBox.information(self, "Ошибка", "недопустимое значение k_" + str(i) + " = " + k_value)
                return
            elif not n_value.isnumeric():
                QtWidgets.QMessageBox.information(self, "Ошибка", n_value + " не является числом")
                return
            
            k_sum += int(k_value)
            n_sum += int(n_value)
        
        if k_sum != k:
            QtWidgets.QMessageBox.information(self, "Ошибка", "сумма k_i должна равняться k")
            return
        elif n_sum != n:
            QtWidgets.QMessageBox.information(self, "Ошибка", "сумма n_i должна равняться n")
            return
        
        numenator = 1
        for i in range(0, m):
            n_value = int(self.ui.n_table.item(i, 0).text())
            k_value = int(self.ui.k_table.item(i, 0).text())
            
            if n_value > k_value:
                QtWidgets.QMessageBox.information(self, "Ошибка", "n_i не может быть больше k_i")
                return
            
            if n_value > 0:
                numenator *= Combinatoric.combinations_without_repeats(k_value, n_value)
        result = numenator / Combinatoric.combinations_without_repeats(k, n)
        result = round(result, 2)
        self.ui.P_lineEdit.setText(str(result))



# Запуск главного окна 
if __name__ == '__main__': 
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    
    sys.exit(app.exec())