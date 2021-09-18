# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

from dayu_widgets.label import MLabel
from dayu_widgets.qt import QWidget, QVBoxLayout


class Setting(QWidget):
    def __init__(self, parent=None):
        super(Setting, self).__init__(parent)

        self.setWindowTitle('setting')

        # setting login page size 700*600
        self.setMaximumSize(940, 700)
        self.setMinimumSize(940, 700)

        self._init_ui()

    def _init_ui(self):
        main_lay = QVBoxLayout()
        main_lay.addWidget(MLabel('setting').h1().strong())
        self.setLayout(main_lay)


if __name__ == '__main__':
    import sys
    from strack_connect.ui import dayu_theme
    from dayu_widgets.qt import QApplication

    app = QApplication(sys.argv)
    test = Setting()
    dayu_theme.apply(test)

    test.show()
    sys.exit(app.exec_())
