# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

from dayu_widgets.alert import MAlert
from dayu_widgets.avatar import MAvatar
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets import dayu_theme
from dayu_widgets.qt import QWidget, QPixmap, QVBoxLayout, MPixmap, QFormLayout, Qt, QHBoxLayout, Signal


class Login(QWidget, MFieldMixin):
    """Login widget class."""
    # Login signal with params  username and password.
    login = Signal(object, object)

    # # Error signal that can be used to present an error message.
    loginError = Signal(object)

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setWindowTitle('strack connect')

        # setting login page size 600*400
        self.setMaximumSize(560, 400)
        self.setMinimumSize(560, 400)

        # use v layout
        main_lay = QVBoxLayout()

        # login logo icon
        icon_layout = QHBoxLayout()
        logon_icon = MAvatar()

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

        self.login_name_input = MLineEdit()
        self.login_name_input.setPlaceholderText(u'请输入用户名')

        self.password_input = MLineEdit().password()
        self.password_input.setPlaceholderText(u'请输入密码')

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

    def on_set_error(self, alert_text, alert_type):
        """Set the error text and disable the login widget."""
        self.set_field('msg_type', alert_type)
        self.set_field('msg', alert_text)

    def slot_handle_login(self):
        """Fetch login data from form fields and emit login event."""
        login_name = self.login_name_input.text()
        password = self.password_input.text()

        # login_name and password require
        if login_name == '' or password == '':
            self.on_set_error(u'请输入用户名，密码！', MAlert.WarningType)
            return

        self.login.emit(login_name, password)


if __name__ == '__main__':
    import sys
    from dayu_widgets.qt import QApplication

    app = QApplication(sys.argv)
    test = Login()
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())