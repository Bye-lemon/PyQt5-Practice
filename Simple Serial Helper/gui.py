from PyQt5.QtWidgets import QApplication
from UI import GUI, Backend

from sys import argv
import qtmodern.styles
import qtmodern.windows

if __name__ == "__main__":
    app = QApplication(argv)
    qtmodern.styles.dark(app)
    gui = GUI()
    modern = qtmodern.windows.ModernWindow(gui)
    backend = Backend()
    backend.update_date.connect(gui.update_gui)
    backend.start()
    modern.show()
    app.exec_()

