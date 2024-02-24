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
        self.touch_mode = False

        self.initUI()

    def initUI(self):
        pixmap = QPixmap('./background.jpg')

        # win pos & size
        self.setGeometry(300, 300, 1229, 775)
        self.setWindowTitle('GILauncher')

        window_size = self.size()

        scaled_pixmap = pixmap.scaled(window_size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)


        # background
        background_label = QLabel(self)
        background_label.setPixmap(scaled_pixmap)
        background_label.setAlignment(Qt.AlignCenter)

        label = QLabel("原神", self)
        label.setGeometry(100, 100, 300, 200)
        label.setStyleSheet("font-size: 80pt; font-family: “Arial”,”Microsoft YaHei”,”黑体”,”宋体”,sans-serif;")

        # file chooser
        chooser = QPushButton('选择原神安装路径', self)
        chooser.clicked.connect(self.showChooser)
        chooser.setGeometry(910, 730, 200, 30)
        
        # unlockfps
        ufps_label = QLabel("解鎖刷新率上限", self)
        ufps_label.setGeometry(730, 620, 200, 20)  # 調整寬度
        ufps_label.adjustSize()
        unlockfps_box = QCheckBox('Unlock FPS', self)
        unlockfps_box.stateChanged.connect(self.unlockfps_option)
        unlockfps_box.setGeometry(840, 620, 15, 15)

        # touch mode
        touch_label = QLabel("觸摸模式", self)
        touch_label.setGeometry(730, 650, 200, 20)
        ufps_label.adjustSize()
        touch_box = QCheckBox('', self)
        touch_box.stateChanged.connect(self.touch_option)
        touch_box.setGeometry(840, 650, 200, 20)

        # game path
        self.path_label = QLabel(f"當前游戲路徑：{self.path}", self)
        self.path_label.setGeometry(600, 570, 200, 20)
        self.path_label.adjustSize()

        # game version (os/cn)
        self.ver_label = QLabel(f"當前游戲版本：{self.get_game_version()[0]}", self)
        self.ver_label.setGeometry(940, 690, 250, 20)
        self.ver_label.adjustSize()
        
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

        self.setFixedSize(self.width(), self.height())

        self.show()

    def launch_gi(self):
            print(f'原神，启动！ {self.path}')
            if not self.path is None:
                exec_cmd = f"{self.get_unlockfps_status()} \"{self.path}/{self.get_game_version()[1]}\" {self.get_touch_status()}"
                print(exec_cmd)
                os.system(exec_cmd)
            else:
                self.showDialog("Error", "请先选择游戏可执行文件")

    def showChooser(self):
        directory = QFileDialog.getExistingDirectory(self, '选择原神安装路径', '.')
        if directory:
            print(directory)
            self.path = directory
            self.config.set_config('game_path', self.path)

            # 檢查目錄中是否存在 GenshinImpact.exe 或 YuanShen.exe
            exe_files = ['GenshinImpact.exe', 'YuanShen.exe']
            exe_found = False
            for exe_file in exe_files:
                if os.path.exists(os.path.join(directory, exe_file)):
                    exe_found = True
                    break

            # 更新 path_label 的文本
            if exe_found:
                self.path_label.setText(f"當前游戲路徑：{self.path}")
            else:
                QMessageBox.critical(self, "錯誤", "找不到可执行文件")

            self.path_label.adjustSize()


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
            return "unlockfps.exe"
        else:
            return ""
        
    def touch_option(self, state):
        if state == 2:
            print("Touch Mode enabled")
            self.touch_mode = True
        else:
            self.touch_mode = False

    def get_touch_status(self):
        if self.touch_mode:
            return " use_mobile_platform -is_cloud 1 -platform_type CLOUD_THIRD_PARTY_MOBILE"
        else:
            return ""
        
    def get_game_version(self): # [version, filename]
        game_files = ['GenshinImpact.exe', 'YuanShen.exe']

        for game_file in game_files:
            if os.path.exists(os.path.join(self.path, game_file)):
                if game_file == 'GenshinImpact.exe':
                    return ['OS', game_file]
                elif game_file == 'YuanShen.exe':
                    return ['CN', game_file]

    def showDialog(self, title="Dialog", msg="Message"):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(msg)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
