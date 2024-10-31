from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtUiTools, QtCore
import sys

# UI 파일 경로
ui_file_path = "test_ui.ui"  # 여기에 ui 파일 경로를 입력하세요


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # QFile로 UI 파일 열기
        ui_file = QtCore.QFile(ui_file_path)
        ui_file.open(QtCore.QFile.ReadOnly)

        # QUiLoader로 UI 파일 로드
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file, self)

        # QFile 닫기
        ui_file.close()

        # UI 표시
        self.ui.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
