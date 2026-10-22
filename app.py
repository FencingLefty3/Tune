from pathlib import Path
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QIcon
import server
import sys


class QMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tune Manager")




def onSubmit(self):

        title = self.title.toPlainText()
        media_ids = 1
        shuffle = self.shuffle.isChecked()
        type = "music"

        
        server.Create_channel(title, media_ids, shuffle, type)
        self.load_channels()

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform,)
from PySide6.QtWidgets import (QApplication, QCheckBox, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QStatusBar,  QVBoxLayout, QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(799, 595)
        MainWindow.setAutoFillBackground(True)
        self.view_media_file = QAction(MainWindow)
        self.view_media_file.setObjectName(u"view_media_file")
        self.view_media_file.setEnabled(True)
        self.create_channel_edit = QAction(MainWindow)
        self.create_channel_edit.setObjectName(u"create_channel_edit")
        self.add_media_edit = QAction(MainWindow)
        self.add_media_edit.setObjectName(u"add_media_edit")
        self.actionHi = QAction(MainWindow)
        self.actionHi.setObjectName(u"actionHi")
        self.view_channels_file = QAction(MainWindow)
        self.view_channels_file.setObjectName(u"view_channels_file")
        self.exit_file = QAction(MainWindow)
        self.exit_file.setObjectName(u"exit_file")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.title = QTextEdit(self.centralwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(480, 30, 281, 31))
        self.label_title = QLabel(self.centralwidget)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setGeometry(QRect(490, 60, 91, 16))
        self.Upload = QPushButton(self.centralwidget)
        self.Upload.setObjectName(u"Upload")
        self.Upload.setGeometry(QRect(480, 90, 281, 31))
        self.shuffle = QCheckBox(self.centralwidget)
        self.shuffle.setObjectName(u"shuffle")
        self.shuffle.setGeometry(QRect(480, 140, 141, 31))
        self.label_genre = QLabel(self.centralwidget)
        self.label_genre.setObjectName(u"label_genre")
        self.label_genre.setGeometry(QRect(630, 180, 91, 16))
        self.Genre = QTextEdit(self.centralwidget)
        self.Genre.setObjectName(u"Genre")
        self.Genre.setGeometry(QRect(620, 140, 141, 31))
        self.submit = QPushButton(self.centralwidget)
        self.submit.setObjectName(u"submit")
        self.submit.setGeometry(QRect(480, 210, 281, 31))
        self.label_ip = QLabel(self.centralwidget)
        self.label_ip.setObjectName(str(server.get_local_ipv4()))
        self.label_ip.setGeometry(QRect(480, 320, 141, 31))
        self.Port = QTextEdit(self.centralwidget)
        self.Port.setObjectName(u"Port")
        self.Port.setGeometry(QRect(620, 290, 141, 31))
        self.label_port = QLabel(self.centralwidget)
        self.label_port.setObjectName(u"label_port")
        self.label_port.setGeometry(QRect(630, 330, 91, 16))
        self.submit.clicked.connect(lambda checked: onSubmit(self))
        
        self.channelsScrollArea = QScrollArea(self.centralwidget)
        self.channelsScrollArea.setObjectName(u"channelsScrollArea")
        self.channelsScrollArea.setGeometry(QRect(0, 0, 441, 551))
        self.channelsScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 437, 547))
        self.channelsScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.host = QPushButton(self.centralwidget)
        self.channelsLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.channelsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.host.setObjectName(u"host")
        self.host.setGeometry(QRect(480, 290, 131, 31))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 799, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menuFile.addAction(self.view_media_file)
        self.menuFile.addAction(self.view_channels_file)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.exit_file)
        self.menuEdit.addAction(self.create_channel_edit)
        self.menuEdit.addAction(self.add_media_edit)
        self.menuEdit.addSeparator()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.view_media_file.setText(QCoreApplication.translate("MainWindow", u"View Media Folder", None))
#if QT_CONFIG(shortcut)
        self.view_media_file.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+O", None))
#endif // QT_CONFIG(shortcut)
        self.create_channel_edit.setText(QCoreApplication.translate("MainWindow", u"New Channel", None))
#if QT_CONFIG(shortcut)
        self.create_channel_edit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.add_media_edit.setText(QCoreApplication.translate("MainWindow", u"Add Media", None))
#if QT_CONFIG(shortcut)
        self.add_media_edit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionHi.setText(QCoreApplication.translate("MainWindow", u"Hi", None))
        self.view_channels_file.setText(QCoreApplication.translate("MainWindow", u"Channels", None))
#if QT_CONFIG(shortcut)
        self.view_channels_file.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+N", None))
#endif // QT_CONFIG(shortcut)
        self.exit_file.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.exit_file.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.title.setToolTip(QCoreApplication.translate("MainWindow", u"Test", None))
#endif // QT_CONFIG(tooltip)
        self.label_title.setText(QCoreApplication.translate("MainWindow", u"Channel Title", None))
        self.Upload.setText(QCoreApplication.translate("MainWindow", u"Upload Media", None))
        self.shuffle.setText(QCoreApplication.translate("MainWindow", u"Shuffle", None))
        self.label_genre.setText(QCoreApplication.translate("MainWindow", u"Genre", None))
        self.submit.setText(QCoreApplication.translate("MainWindow", u"Create", None))
        self.label_ip.setText(QCoreApplication.translate("MainWindow", str(server.get_local_ipv4()), None))
        self.label_port.setText(QCoreApplication.translate("MainWindow", u"Port", None))
        self.host.setText(QCoreApplication.translate("MainWindow", u"Host", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))

    
    def load_channels(self):
        while self.channelsLayout.count():
            item = self.channelsLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        for index, channel in enumerate(server.Read_chanel()):
            card = QWidget(self.scrollAreaWidgetContents)
            card.setObjectName(f"channel_{index}")
            card.setMinimumHeight(91)
            card.setStyleSheet(
                f"#{card.objectName()} {{ background-color: #757575; }}"
            )

            card_layout = QVBoxLayout(card)

    

            title_label = QLabel(
                channel.get("title", "Untitled"),
                card,
                
            )
            genre_label = QLabel(
                f"Type: {channel.get('type', 'unknown')}",
                card,
            )

            card_layout.addWidget(title_label)
            card_layout.addWidget(genre_label)
            self.channelsLayout.addWidget(card)
            title_font = QFont()
            title_font.setPointSize(20)
            title_label.setFont(title_font)

            genre_font = QFont()
            genre_font.setPointSize(10)
            genre_label.setFont(genre_font)
    def host_server(self):
        return

        


def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    icon_path = Path(__file__).resolve().parent / "icon.png"
    window.setWindowIcon(QIcon(str(icon_path)))
    ui = Ui_MainWindow()
    ui.setupUi(window)
    ui.load_channels()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
