# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

from dayu_widgets.label import MLabel
from dayu_widgets.loading import MLoading
from dayu_widgets.qt import Qt, QWidget, QMainWindow, QFont, QFontMetrics, QMovie, QMoveEvent, QCloseEvent, QShowEvent, \
    QSize, QTimer, QHBoxLayout


class LoadingMask(QMainWindow):
    def __init__(self, parent=None, gif=None):
        super(LoadingMask, self).__init__(parent)

        self.label = MLabel()

        self.label = MLoading.large()

        layout = QHBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        layout.addWidget(self.label)

        self.setCentralWidget(widget)
        self.setWindowOpacity(0.8)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.hide()

    def eventFilter(self, widget, event):
        if widget == self.parent() and (type(event) in [QMoveEvent, QCloseEvent]):
            if type(event) == QCloseEvent:
                self.hide()
            else:
                self.moveWithParent()
            return True
        return super(LoadingMask, self).eventFilter(widget, event)

    def moveWithParent(self):
        if self.isVisible():
            self.move(self.parent().geometry().x(), self.parent().geometry().y())
            self.setFixedSize(QSize(self.parent().geometry().width(), self.parent().geometry().height()))

    def show_loading(self):
        self.show()
        self.moveWithParent()
