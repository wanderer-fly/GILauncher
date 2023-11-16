import os
import sys
import config

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QLabel, QComboBox, QCheckBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Launcher(QWidget):
    def __init__(self):
        super().__init__()

        self.config = config.Config()
        self.path = self.config.read_config()['game_path']

        self.unlockfps_status = self.config.read_config()['unlockfps']
        # self.exec_cmd = f"prime-run wine {self.get_unlockfps_status()} {self.path}"

        self.initUI()

    def initUI(self):
        pixmap = QPixmap('./background.jpg')

        # win pos & size
        self.setGeometry(300, 300, 1229, 775)
        self.setWindowTitle('GILauncher')

        window_size = self.size()

        scaled_pixmap = pixmap.scaled(window_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)


        # 创建背景标签
        background_label = QLabel(self)
        background_label.setPixmap(scaled_pixmap)
        background_label.setAlignment(Qt.AlignCenter)

        label = QLabel("原神", self)
        label.setGeometry(100, 100, 300, 200)
        label.setStyleSheet("font-size: 100pt; font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;")

        # file chooser
        chooser = QPushButton('选择原神安装路径', self)
        chooser.clicked.connect(self.showChooser)
        
        # unlockfps
        unlockfps_box = QCheckBox('Unlock FPS', self)
        unlockfps_box.stateChanged.connect(self.unlockfps_option)
        unlockfps_box.setGeometry(0, 50, 15, 15)
        

        # launch game
        launch_game = QPushButton('Launch', self)
        launch_game.clicked.connect(self.launch_gi)
        launch_game.setStyleSheet("""
                                    background: #b3b300;
                                    color: #5d3703;
                                    font-size: 22pt;
                                    border-radius: 2px;
                                    font-family: 'Courier New', Courier, monospace;
                                  """)
        launch_game.setGeometry(890, 600, 250, 80)

        # self.setLayout(box)
        self.setFixedSize(self.width(), self.height())

        self.show()

    def launch_gi(self):
            print(f'原神，启动！ {self.path}')
            if not self.path is None:
                exec_cmd = f"prime-run wine {self.get_unlockfps_status()} {self.path}"
                # os.system(f'prime-run wine "{self.path}"')
                print(exec_cmd)
                os.system(exec_cmd)
            else:
                self.showDialog("Error", "请先选择游戏可执行文件")

    def showChooser(self):
        fname = QFileDialog.getOpenFileName(self, '选择原神可执行程式', '.', 'Executable Files (*.exe);;All Files (*)')

        if fname[0]:
            print(fname[0])
            self.path = fname[0]
            self.config.set_config('game_path', self.path)

    def unlockfps_option(self, state):
        if state == 2:
            print("Unlockfps on")
            self.unlockfps_status = True
        else:
            print("Unlockfps off")
            self.unlockfps_status = False

    def get_unlockfps_status(self):
        print(self.unlockfps_status)
        if self.unlockfps_status:
            return "./unlockfps.exe"
        else:
            return ""

    def showDialog(self, title="Dialog", msg="Message"):
        msg_box = QMessageBox()

        msg_box.setWindowTitle(title)
        msg_box.setText(msg)
        msg_box.setIcon(QMessageBox.Information)

        msg_box.setStandardButtons(QMessageBox.Ok)
