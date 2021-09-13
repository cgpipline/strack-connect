# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

from strack_connect.config.strack_error import StrackError
from strack_connect.config.env import Env
from strack_connect.config.log import *
from strack_connect.config.config import Config
from strack_connect.ui.widget import login as _login
from dayu_widgets.qt import QMainWindow, Signal
from dayu_widgets import dayu_theme


class Application(QMainWindow):
    """ Main application window for strack connect.' """

    #: Signal when login fails.
    loginError = Signal(object)

    # Login signal.
    loginSignal = Signal(object, object, object)
    loginSuccessSignal = Signal()

    @property
    def session(self):
        """Return current session."""
        return self._session

    def __init__(self, theme='dark'):
        super(Application, self).__init__()

        # reset session
        self._session = None

        # load env
        Env()

        # load config
        config = Config()
        config.load("config.yaml")

        # init logger
        set_logger(["connect_runtime", "api"])

        self.loginWidget = _login.Login(theme=theme)
        self.login()

    def login(self):
        """Login using stored credentials or ask user for them."""
        self.show_login_widget()

    def show_login_widget(self):
        """Show the login widget."""
        self.setCentralWidget(self.loginWidget)
        self.loginError.connect(self.loginWidget.loginError.emit)
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
