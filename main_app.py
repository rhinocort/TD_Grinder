from window_app import *
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyApp()
    window.setWindowTitle('TD-GRINDER v.01')
    window.show()
    sys.exit(app.exec_())
