#!/usr/bin/env python
# coding=utf-8
'''
Date: 2022-01-05 22:32:50
'''

from dayu_widgets.qt import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, MPixmap, QListView, QSize
from dayu_widgets.card import MMeta
from ui.widget.component.top_select import BarTopSelect


class Task(QWidget):
    def __init__(self, parent=None):
        super(Task, self).__init__(parent)
        self.setMaximumSize(940, 700)
        self.setMinimumSize(940, 700)
        self._init_ui()

    def _init_ui(self):
        main_lay = QVBoxLayout()
        self.topbar = BarTopSelect(self)
        self.topbar.project_type.addItems([u"我的项目", u"全部项目"])
        self.topbar.bar_title.setText(u"项目列表")
        main_lay.addWidget(self.topbar)
        self.task_pm_list = QListWidget()
        self.task_pm_list.setViewMode(QListView.IconMode)
        self.task_pm_list.setSpacing(18)
        self.task_pm_list.verticalScrollBar().setSingleStep(10)
        self.task_pm_list.setResizeMode(QListView.Adjust)
        main_lay.addWidget(self.task_pm_list)
        self.setLayout(main_lay)
    
    def add_project_item(self, setting):
        project_card = MMeta()
        project_card.setup_data(setting)
        myQListWidgetItem = QListWidgetItem(self.task_pm_list)
        myQListWidgetItem.setSizeHint(QSize(204, 260))
        self.task_pm_list.addItem(myQListWidgetItem)
        self.task_pm_list.setItemWidget(myQListWidgetItem, project_card)
        return project_card


if __name__ == '__main__':
    import sys
    from strack_connect.ui import dayu_theme
    from dayu_widgets.qt import QApplication

    app = QApplication(sys.argv)
    test = Task()
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())
