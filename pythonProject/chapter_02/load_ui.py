from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

# UI 파일 경로
ui_file_path = "TestProgramUI.ui"  # 여기에 ui 파일 경로를 입력하세요

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # loadUi 함수로 UI 파일 불러오기
        uic.loadUi(ui_file_path, self)

        # UI 초기화 후 원하는 기능 추가
        self.pushButton.clicked.connect(self.print_function)

    def print_function(self):
        self.lineEdit.setText("안녕하세요!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()  # UI 창을 띄우기
    sys.exit(app.exec_())
