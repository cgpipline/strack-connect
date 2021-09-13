# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

import os
import signal
import strack_connect.ui.application
from dayu_widgets.qt import QApplication, QCoreApplication, Qt
from dayu_widgets import dayu_theme


def main():
    # If under X11, make Xlib calls thread-safe.
    # http://stackoverflow.com/questions/31952711/threading-pyqt-crashes-with-unknown-request-in-queue-while-dequeuing
    if os.name == 'posix':
        QCoreApplication.setAttribute(Qt.AA_X11InitThreads)

    application = QApplication([])
    application.setOrganizationName('strack')
    application.setOrganizationDomain('github.com/cgpipline')
    application.setQuitOnLastWindowClosed(False)

    # Enable ctrl+c to quit application when started from command line.
    signal.signal(signal.SIGINT, lambda sig, _: application.quit())

    # Construct main connect window and apply theme.
    connect_window = strack_connect.ui.application.Application()
    dayu_theme.apply(connect_window)
    connect_window.focus()

    # Fix for Windows where font size is incorrect for some widgets. For some
    # reason, resetting the font here solves the sizing issue.
    font = application.font()
    application.setFont(font)

    return application.exec_()


if __name__ == '__main__':
    raise SystemExit(
        main()
    )
