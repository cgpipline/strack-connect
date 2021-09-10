# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

from dayu_widgets.avatar import MAvatar
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.label import MLabel
from dayu_widgets.push_button import MPushButton
from dayu_widgets import dayu_theme
from dayu_widgets.message import MMessage
from dayu_widgets.qt import QWidget, QPixmap, QVBoxLayout, MPixmap, QFormLayout, Qt, QHBoxLayout


class Login(QWidget, MFieldMixin):
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
        logon_icon.set_dayu_size(180)
        logon_icon.setFixedSize(180, 120)

        icon_layout.addWidget(logon_icon)
        main_lay.addLayout(icon_layout)

        # login form layout
        form_lay = QFormLayout()
        form_lay.setContentsMargins(80, 0, 80, 0)

        form_lay.setLabelAlignment(Qt.AlignLeft)
        form_lay.setVerticalSpacing(16)

        self.login_name_input = MLineEdit()
        self.login_name_input.setPlaceholderText('请输入用户名')

        self.password_input = MLineEdit().password()
        self.password_input.setPlaceholderText('请输入密码')

        form_lay.addRow(MLabel('登录名：').strong(), self.login_name_input)
        form_lay.addRow(MLabel('密码：').strong(), self.password_input)

        main_lay.addLayout(form_lay)

        # login button
        button_layout = QHBoxLayout()
        login_button = MPushButton(text='登录').primary()
        login_button.clicked.connect(self.slot_handle_login)
        button_layout.addWidget(login_button)
        button_layout.setContentsMargins(80, 0, 80, 60)

        main_lay.addLayout(button_layout)
        self.setLayout(main_lay)

    def slot_handle_login(self):
        """Fetch login data from form fields and emit login event."""
        login_name = self.login_name_input.text()
        password = self.password_input.text()

        # 必须输入账户密码
        if login_name == '' or password == '':
            MMessage.warning('请输入用户名，密码！', parent=self, closable=True)
            return

        print("login name {}".format(login_name))
        print("password {}".format(password))


if __name__ == '__main__':
    import sys
    from dayu_widgets.qt import QApplication

    app = QApplication(sys.argv)
    test = Login()
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())
