# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

import os
import sqlite3

from strack_connect.model.session import Session, LoginThread
from strack_connect.config.log import *
from strack_connect.config.config import Config
from strack_connect.ui.widget import login as _login
from strack_connect.ui.widget import main as _main
from dayu_widgets.qt import QMainWindow, QApplication, QSystemTrayIcon, QMenu, QAction, Signal, MPixmap, MIcon
from dayu_widgets import dayu_theme


class Application(QMainWindow):
    """ Main application window for strack connect.' """

    #: Signal when login fails.
    loginMsg = Signal(object, object)

    # Login signal.
    loginSignal = Signal(object, object, object)
    loginSuccessSignal = Signal()

    @property
    def session(self):
        """Return current session."""
        return self._session

    def __init__(self, theme='dark'):
        super(Application, self).__init__()

        # reset
        self._session = None
        self._login_server_thread = None

        # load config
        config = Config()
        config.load("config.yaml")

        # init logger
        set_loggers(["connect_runtime", "api"])
        self.logoIcon = MIcon('{}/images/favicon.ico'.format(os.getenv('RESOUCE_PATH')))
        self.setObjectName('strack-connect-window')
        self.setWindowTitle('strack connect')
        self.setWindowIcon(self.logoIcon)

        self._initialiseTray(self.logoIcon)

        self.setMaximumSize(560, 460)
        self.setMinimumSize(560, 460)
        self.loginWidget = _login.Login(parent=self)
        self.loginSignal.connect(self.login_request)
        self.loginSuccessSignal.connect(self._post_login_settings)
        self.login()

    def _createTrayMenu(self):
        """Return a menu for system tray."""
        menu = QMenu(self)

        quit_action = QAction(
            'Quit', self,
            triggered=QApplication.quit
        )

        focus_action = QAction(
            'Open', self,
            triggered=self.focus
        )

        about_action = QAction(
            'About', self,
            triggered=self.show_about
        )

        menu.addAction(about_action)
        menu.addSeparator()
        menu.addAction(focus_action)
        menu.addSeparator()
        menu.addAction(quit_action)

        return menu

    def _initialiseTray(self, icon):
        '''Initialise and add application icon to system tray.'''
        self.trayMenu = self._createTrayMenu()
        self.tray = QSystemTrayIcon(self)

        self.tray.setContextMenu(
            self.trayMenu
        )
        self.tray.setIcon(icon)

    def show_about(self):
        """Display window with about information."""
        print("about")

    def _post_login_settings(self):
        if self.tray:
            self.tray.show()

        self.setMinimumSize(1140, 700)
        self.mainWidget = _main.Main(parent=self)
        self.setCentralWidget(self.mainWidget)
        self.focus()
        self._save_user_settings()

    def _save_user_settings(self):
        user_setting_path = "{}/strack-connect/user_setting.db".format(os.environ.get("temp"))
        if not os.path.exists(os.path.dirname(user_setting_path)):
            os.makedirs(os.path.dirname(user_setting_path))
        status = {True: 1, False: 0}
        auto_login_check = self.loginWidget.auto_login_check.isChecked()
        remember_password = self.loginWidget.remember_password_check.isChecked()
        if remember_password:
            conn = sqlite3.connect(user_setting_path)
            c = conn.cursor()
            create_table_sql = """create table if not exists login_user
            (id integer primary key autoincrement,
            user_name varchar(20),
            url text not NULL,
            password text not NULL,
            is_autologin integer not NULL,
            is_remember integer not NULL)
            """
            c.execute(create_table_sql)
            conn.commit()
            login_user_data = c.execute("SELECT id from login_user")
            if len(list(login_user_data)) == 1:
                c.execute("UPDATE login_user set user_name='{}',"
                          " url='{}',password='{}', is_remember={}, is_autologin={} where id=1".format(
                    self.loginWidget.login_name_input.text(), self.loginWidget.login_url_input.text(),
                    self.loginWidget.password_input.text(), status[remember_password], status[auto_login_check]
                ))
            else:
                save_info_sql = """insert into login_user (user_name, url, password, is_remember, is_autologin)
                VALUES ('{}','{}', '{}', {}, {})
                """.format(self.loginWidget.login_name_input.text(), self.loginWidget.login_url_input.text(),
                           self.loginWidget.password_input.text(), status[remember_password], status[auto_login_check])
                c.execute(save_info_sql)
            conn.commit()
            conn.close()

    def login(self):
        """Login using stored credentials or ask user for them."""
        self.loginWidget.login.connect(self.login_request)
        self.show_login_widget()

    def login_request(self, url, username, password):

        # If there is an existing server thread running we need to stop it.
        if self._login_server_thread:
            self._login_server_thread.quit()
            self._login_server_thread = None

        # get token by QThread
        if url is not None and username is not None and password is not None:
            self._login_server_thread = LoginThread()
            self._login_server_thread.loginMsg.connect(self.loginMsg)
            self._login_server_thread.loginSuccessSignal.connect(self.loginSuccessSignal)
            self._login_server_thread.start(url, username, password)
            return

    def show_login_widget(self):
        """Show the login widget."""
        self.setCentralWidget(self.loginWidget)
        self.loginMsg.connect(self.loginWidget.loginMsg.emit)
        self.loginWidget.setFocus()

    def focus(self):
        """Focus and bring the window to top."""
        self.activateWindow()
        self.show()
        self.raise_()


if __name__ == '__main__':
    import sys
    from dayu_widgets.qt import QApplication

    app = QApplication(sys.argv)

    try:
        test = Application()
        dayu_theme.apply(test)
        test.focus()
        # raise StrackError("test error")
        sys.exit(app.exec_())
    except Exception as e:
        print(e.args)
