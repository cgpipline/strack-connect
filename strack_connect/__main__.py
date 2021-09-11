# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

import logging
from strack_connect.config.env import *  # setup environment
import strack_connect.ui.application

# set Logger
logger = logging.getLogger("strack_connect")
logger.setLevel(logging.DEBUG)


def main():
    print("main")


if __name__ == '__main__':
    raise SystemExit(
        main()
    )
