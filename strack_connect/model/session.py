# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

import traceback
from strack_connect.config.log import *
from strack_api.strack import Strack
import threading


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
                'msg': ""
            }
        except Exception as err:
            logger.error("login failed. Please check login info.")
            logger.error(err)
            logger.error(traceback.format_exc())
            return {
                'code': False,
                'msg': "login failed. %s." % err.args
            }
