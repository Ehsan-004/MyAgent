from PyQt6.QtWidgets import QApplication
import sys
from ui.app import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    file_indexes = dict()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
