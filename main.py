from typing import Type
from unittest import result
from PyQt5.QtGui import QPixmap
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

        # Устанавливаем изображение формулы
        self.ui.setupUi(self)
        pixmap = QPixmap("img/img.jpg")
        self.ui.label.setPixmap(pixmap)

        # Устанавливаем коннекты
        self.ui.k_table.currentCellChanged.connect(self.setCell_n_table)
        self.ui.n_table.currentCellChanged.connect(self.setCell_k_table)
        self.ui.addButton.clicked.connect(self.addRow)
        self.ui.removeButton.clicked.connect(self.removeRow)
        self.ui.m_spinBox.editingFinished.connect(self.enter)
        self.ui.resultButton.clicked.connect(self.solve)


    '''Изменить текущую строку таблицы k элементов, при изменении строки n элементов'''
    def setCell_k_table(self):
        curCell = self.ui.n_table.currentRow()
        self.ui.k_table.setCurrentCell(curCell, 0)


    '''Изменить текущую строку таблицы n элементов, при изменении строки k элементов'''
    def setCell_n_table(self):
        curCell = self.ui.k_table.currentRow()
        self.ui.n_table.setCurrentCell(curCell, 0)


    '''Добавить по одной строке в таблицы'''
    def addRow(self):
        lastRow = self.ui.k_table.rowCount()
        self.ui.k_table.insertRow(lastRow)
        self.ui.k_table.setItem(lastRow, 0, QtWidgets.QTableWidgetItem("1"))
        self.ui.n_table.insertRow(lastRow)
        self.ui.n_table.setItem(lastRow, 0, QtWidgets.QTableWidgetItem("0"))
        self.updateHeaders()
        self.ui.m_spinBox.setValue(self.ui.k_table.rowCount())


    '''Удалить по одной строке из таблиц'''
    def removeRow(self):
        curRow = self.ui.k_table.currentRow()
        if self.ui.k_table.rowCount() > 1:
            self.ui.k_table.removeRow(curRow)
            self.ui.n_table.removeRow(curRow)
            self.updateHeaders()
            self.ui.m_spinBox.setValue(self.ui.k_table.rowCount())


    '''Обновить заголовки строк в таблицах'''
    def updateHeaders(self):
        for i in range(self.ui.k_table.rowCount()):
            item = QtWidgets.QTableWidgetItem("k_" + str(i + 1))
            self.ui.k_table.setVerticalHeaderItem(i, item)
            item = QtWidgets.QTableWidgetItem("n_" + str(i + 1))
            self.ui.n_table.setVerticalHeaderItem(i, item)


    '''Установить m строк в таблицы'''
    def enter(self):
        m = self.ui.m_spinBox.value()
        rowAmount = self.ui.k_table.rowCount()
        if m < rowAmount:
            for i in range(rowAmount - 1, m - 1, -1):
                self.ui.k_table.setCurrentCell(i, 0)
                self.removeRow()
        elif m > rowAmount:
            for i in range(rowAmount - 1, m - 1, 1):
                self.addRow()


    '''Проверить корректность введенных данных'''
    def isInputCorrect(self, k, n, m):
        if n > k:
            QtWidgets.QMessageBox.information(self, "Ошибка", "n не может быть больше k")
            return False
        elif m > k:
            QtWidgets.QMessageBox.information(self, "Ошибка", "m не может быть больше k")
            return False
        
        k_sum = 0
        n_sum = 0
        for i in range(m):
            k_value = self.ui.k_table.item(i, 0).text()
            n_value = self.ui.n_table.item(i, 0).text()
            
            if not k_value.isnumeric():
                QtWidgets.QMessageBox.information(self, "Ошибка", "недопустимое значение k_" + str(i + 1) + " = " + k_value)
                return False
            elif not n_value.isnumeric():
                QtWidgets.QMessageBox.information(self, "Ошибка", "недопустимое значение n_" + str(i + 1) + " = " + n_value)
                return False
            elif int(n_value) > int(k_value):
                QtWidgets.QMessageBox.information(self, "Ошибка", "n_" + str(i + 1) + " не может быть больше k_" + str(i + 1))
                return False
            
            k_sum += int(k_value)
            n_sum += int(n_value)
        
        if k_sum != k:
            QtWidgets.QMessageBox.information(self, "Ошибка", "сумма k_i должна равняться k")
            return False
        elif n_sum != n:
            QtWidgets.QMessageBox.information(self, "Ошибка", "сумма n_i должна равняться n")
            return False
        return True


    '''Вычислить результирующее значение'''
    def solve(self):
        k = self.ui.k_spinBox.value()
        n = self.ui.n_spinBox.value()
        m = self.ui.m_spinBox.value()

        # Проверить введенные данные
        if not self.isInputCorrect(k, n, m):
            return
        
        # В числителе произведение всех сочетаний n_i по k_i
        numenator = 1
        for i in range(0, m):
            n_value = int(self.ui.n_table.item(i, 0).text())
            k_value = int(self.ui.k_table.item(i, 0).text())
            if n_value > 0:
                numenator *= Combinatoric.combinations_without_repeats(k_value, n_value)

        # Полученный числитель разделить на число сочетаний n по k
        result = numenator / Combinatoric.combinations_without_repeats(k, n)

        # Вывести результат в поле ответа
        str_result = "{:01.12f}".format(result)
        self.ui.P_lineEdit.setText(str_result)



# Запуск главного окна 
if __name__ == '__main__': 
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    
    sys.exit(app.exec())