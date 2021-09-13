# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

import traceback
from strack_connect.config.log import *
from strack_api.strack import Strack
from dayu_widgets.qt import QThread, Signal
from dayu_widgets.alert import MAlert
import threading


class LoginThread(QThread):
    """Session api by thread"""
    # Login Msg signal.
    loginMsg = Signal(object, object)
    url = ""
    username = ""
    password = ""

    def start(self, url, username, password):
        """Start thread."""
        self.url = url
        self.username = username
        self.password = password
        super(LoginThread, self).start()

    def _handle_login(self):
        """Login to server with *api_user* and *api_key*."""
        session = Session()

        res = session.get_token(self.url, self.username, self.password)
        if not res['code']:
            self.loginMsg.emit(res['msg'], MAlert.ErrorType)
        else:
            self.loginMsg.emit(res['msg'], MAlert.SuccessType)
            self.loginSuccessSignal.emit()

    def run(self):
        """Listen for events."""
        self._handle_login()


class Session(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Session, "_instance"):
            with Session._instance_lock:
                if not hasattr(Session, "_instance"):
                    Session._instance = object.__new__(cls)
        return Session._instance

    @staticmethod
    def get_token(url, username, password):
        logger = get_logger("api")
        try:
            strack = Strack(url, username, password)
            user_filters = [['id', 'is', strack.user_id]]
            user = strack.find('user', user_filters)
            print(user)
            if not user:
                raise RuntimeError('Cannot find user named %s.' % username)
            return {
                'code': True,
                'msg': u"登录成功，正在跳转……"
            }
        except Exception as err:
            logger.error("login failed. Please check login info.")
            logger.error(err)
            logger.error(traceback.format_exc())
            return {
                'code': False,
                'msg': u"登录失败. %s." % err.args
            }
