# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

import os
import functools

from dayu_widgets.avatar import MAvatar
from dayu_widgets.label import MLabel
from dayu_widgets.menu_tab_widget import MMenuTabWidget
from dayu_widgets.divider import MDivider
from dayu_widgets.qt import QWidget, Qt, QVBoxLayout, QHBoxLayout, MPixmap, Signal


class LeftMenu(QWidget):
    # menu click signal
    menuClicked = Signal(object)

    def __init__(self, parent=None):
        super(LeftMenu, self).__init__(parent)
        self.setWindowTitle('Left main menu')
        self._init_ui()

    def _init_ui(self):
        # add QHBoxLayout for avatar
        top_lay = QHBoxLayout()
        top_lay.setContentsMargins(20, 15, 20, 15)

        avatar = MAvatar.huge(MPixmap('avatar.png'))
        top_lay.addWidget(avatar)

        # dd QVBoxLayout for userinfo
        user_info = QVBoxLayout()
        user_info.setContentsMargins(10, 0, 0, 0)
        user_info.addWidget(MLabel('weijer').h4().strong())
        user_info.addWidget(MLabel('制片人').secondary())
        top_lay.addLayout(user_info)

        # menu tool buttons
        resource_path = os.getenv('RESOUCE_PATH')

        if resource_path is not None:
            img_path = '{}/images/'.format(resource_path)
        else:
            img_path = '{}/resource/images/'.format(os.path.dirname(os.getcwd()))

        button_list = [
            {'text': u'任务', 'svg': '{}menu_task.svg'.format(img_path), 'clicked': functools.partial(self.menu_clicked)},
            {'text': u'应用', 'svg': '{}menu_launcher.svg'.format(img_path), 'clicked': functools.partial(self.menu_clicked)},
            {'text': u'Actions', 'svg': '{}menu_action.svg'.format(img_path), 'clicked': functools.partial(self.menu_clicked)},
            {'text': u'配置', 'svg': '{}menu_setting.svg'.format(img_path), 'clicked': functools.partial(self.menu_clicked)}
        ]

        menu = MMenuTabWidget(orientation=Qt.Vertical)
        for index, data_dict in enumerate(button_list):
            data_dict['clicked'] = functools.partial(self.menu_clicked, index)
            menu.add_menu(data_dict, index)

        menu.tool_button_group.set_dayu_checked(0)

        main_lay = QVBoxLayout()
        main_lay.setContentsMargins(0, 0, 0, 0)

        # add top user info layout
        main_lay.addLayout(top_lay)

        # add divider line
        main_lay.addWidget(MDivider())

        # add menu layout
        main_lay.addWidget(menu)

        main_lay.addStretch()
        self.setLayout(main_lay)

    def menu_clicked(self, index):
        # emit index
        self.menuClicked.emit(index)


if __name__ == '__main__':
    import sys
    from strack_connect.ui import dayu_theme
    from dayu_widgets.qt import QApplication

    app = QApplication(sys.argv)
    test = LeftMenu()
    dayu_theme.apply(test)

    test.show()
    sys.exit(app.exec_())
