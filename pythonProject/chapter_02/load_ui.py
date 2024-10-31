from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtUiTools
import sys

# UI 파일 경로
ui_file_path = "test_ui.ui"  # 여기에 ui 파일 경로를 입력하세요

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # UI 파일을 불러오기
        loader = QtUiTools.QUiLoader()
        ui_file = open(ui_file_path, "r", encoding="utf-8")
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # UI 초기화 후 원하는 기능 추가
        # 예: self.ui.button.clicked.connect(self.some_function)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.ui.show()  # UI 창을 띄우기
    sys.exit(app.exec_())
