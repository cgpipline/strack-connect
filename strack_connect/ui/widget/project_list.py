# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

from dayu_widgets.qt import QWidget, QHBoxLayout


class ProjectList(QWidget):
    def __init__(self, parent=None):
        super(ProjectList, self).__init__(parent)

        self.setWindowTitle('project list')

        # setting login page size 700*600
        self.setMaximumSize(940, 700)
        self.setMinimumSize(940, 700)

        self._init_ui()

    def _init_ui(self):
        print('project')


if __name__ == '__main__':
    import sys
    from strack_connect.ui import dayu_theme
    from dayu_widgets.qt import QApplication

    app = QApplication(sys.argv)
    test = ProjectList()
    dayu_theme.apply(test)

    test.show()
    sys.exit(app.exec_())
