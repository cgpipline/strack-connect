# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

import os
import importlib
import codecs
from dayu_widgets.qt import QWidget, QHBoxLayout, QStackedWidget


class Main(QWidget):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.setWindowTitle('main')

        # setting login page size 1140*700
        self.setMaximumSize(1140, 700)
        self.setMinimumSize(1140, 700)

        self._init_ui()

    def _init_ui(self):
        main_lay = QHBoxLayout()
        self.stacked_widget = QStackedWidget()

        # load menu widget
        left_menu = self.get_widget_by_name('left_menu')

        if left_menu.get('cls') is not None:
            left_menu_widget = left_menu.get('cls')()
            left_menu_widget.setProperty('code', left_menu.get('code'))
            main_lay.addWidget(left_menu_widget)
            main_lay.setStretchFactor(left_menu_widget, 1)

        # load project list
        project_list = self.get_widget_by_name('project_list')

        if project_list.get('cls') is not None:
            project_list_widget = project_list.get('cls')()
            project_list_widget.setProperty('code', project_list.get('code'))
            main_lay.addWidget(project_list_widget)
            main_lay.setStretchFactor(project_list_widget, 1)

        # main_lay.addStretch()
        main_lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_lay)

    @staticmethod
    def get_widget_by_name(name=None):
        widget = {
            'name': '',
            'cls': None,
            'code': '',
        }
        if name is not None:
            dir = os.path.dirname(__file__)
            module_name = 'strack_connect.ui.widget.{component}'.format(component=name)
            class_name = ''.join(map(lambda x: x.title(), name.split('_')))
            module = importlib.import_module(module_name, class_name)
            if hasattr(module, class_name):
                with codecs.open(os.path.join(dir, "%s.py" % name), encoding='utf-8') as f:
                    widget['name'] = name
                    widget['cls'] = getattr(module, class_name)
                    widget['code'] = f.readlines()

        return widget


if __name__ == '__main__':
    import sys
    from strack_connect.ui import dayu_theme
    from dayu_widgets.qt import QApplication

    app = QApplication(sys.argv)
    test = Main()
    dayu_theme.apply(test)

    test.show()
    sys.exit(app.exec_())
