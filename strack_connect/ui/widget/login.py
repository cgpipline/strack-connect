# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

import os
from dayu_widgets.alert import MAlert
from dayu_widgets.avatar import MAvatar
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets import dayu_theme
from dayu_widgets.qt import QWidget, QPixmap, QVBoxLayout, MPixmap, QFormLayout, Qt, QHBoxLayout, Signal
from strack_connect.ui.widget.loading import LoadingMask


class Login(QWidget, MFieldMixin):
    """Login widget class."""
    # Login signal with params  username and password.
    login = Signal(object, object, object)

    # # Error signal that can be used to present an error message.
    loginError = Signal(object, object)

    def __init__(self, parent=None, **kwargs):
        super(Login, self).__init__(parent)

        theme = kwargs.get("theme", "dark")
        dayu_theme.set_theme(theme)

        self.setWindowTitle('strack connect')

        # setting login page size 600*400
        self.setMaximumSize(560, 460)
        self.setMinimumSize(560, 460)

        # use v layout
        main_lay = QVBoxLayout()

        # login logo icon
        icon_layout = QHBoxLayout()
        logon_icon = MAvatar()

        resource_path = os.getenv('RESOUCE_PATH')

        if resource_path is not None:
            logon_icon.set_dayu_image(MPixmap(
                '{}/images/desktop_logo.png'.format(resource_path)
            ))
        else:
            logon_icon.set_dayu_image(MPixmap(
                './../resource/images/desktop_logo.png'
            ))

        logon_icon.set_dayu_size(140)

        icon_layout.addWidget(logon_icon)
        main_lay.addLayout(icon_layout)

        # login form layout
        form_lay = QFormLayout()
        form_lay.setContentsMargins(80, 0, 80, 0)

        form_lay.setLabelAlignment(Qt.AlignLeft)
        form_lay.setVerticalSpacing(16)

        self.login_url_input = MLineEdit()
        self.login_url_input.setPlaceholderText(u'请输入请求地址')

        self.login_name_input = MLineEdit()
        self.login_name_input.setPlaceholderText(u'请输入用户名')

        self.password_input = MLineEdit().password()
        self.password_input.setPlaceholderText(u'请输入密码')

        form_lay.addRow(MLabel(u'URL：').strong(), self.login_url_input)
        form_lay.addRow(MLabel(u'登录名：').strong(), self.login_name_input)
        form_lay.addRow(MLabel(u'密码：').strong(), self.password_input)

        main_lay.addLayout(form_lay)

        # login button
        button_layout = QHBoxLayout()
        login_button = MPushButton(text='登录').primary()
        login_button.clicked.connect(self.slot_handle_login)

        button_layout.addWidget(login_button)
        button_layout.setContentsMargins(80, 40, 80, 20)

        main_lay.addLayout(button_layout)

        # error message region
        error_message_layout = QHBoxLayout()
        self.register_field('msg', '')
        self.register_field('msg_type', MAlert.InfoType)
        error_label = MAlert(parent=self)
        error_label.set_closable(True)
        self.bind('msg', error_label, 'dayu_text')
        self.bind('msg_type', error_label, 'dayu_type')

        error_message_layout.addWidget(error_label)
        error_message_layout.setContentsMargins(20, 0, 20, 0)
        self.loginError.connect(self.on_set_error)

        main_lay.addLayout(error_message_layout)

        main_lay.addStretch()

        self.setLayout(main_lay)

        if parent is not None:
            self.loading_mask = LoadingMask(parent=parent)
            parent.installEventFilter(self.loading_mask)
        else:
            self.loading_mask = LoadingMask(parent=self)
            self.installEventFilter(self.loading_mask)

    def on_set_error(self, alert_text, alert_type):
        """Set the error text and disable the login widget."""
        # hide plane loading
        # self.loading_mask.hide()

        # show error tip msg
        self.set_field('msg_type', alert_type)
        self.set_field('msg', alert_text)

    def slot_handle_login(self):
        """Fetch login data from form fields and emit login event."""
        login_url = self.login_url_input.text()
        login_name = self.login_name_input.text()
        password = self.password_input.text()

        # login_name and password require
        if login_url == '' or login_name == '' or password == '':
            self.on_set_error(u'URL，请输入用户名，密码！', MAlert.WarningType)
            return
        else:
            self.on_set_error('', MAlert.InfoType)

        # show plane loading
        self.loading_mask.show_loading()

        # emit login parm
        self.login.emit(login_url, login_name, password)


if __name__ == '__main__':
    import sys
    from dayu_widgets.qt import QApplication

    app = QApplication(sys.argv)
    test = Login()
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())
