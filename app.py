from PySide6.QtWidgets import QApplication, QWidget

import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tune Manager")


        pyside6-designer


app = QApplication(sys.argv)


window = MainWindow()
window.show()
app.exec()
