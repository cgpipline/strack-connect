# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

import os
import sys
import inspect

if sys.platform == "darwin":
    platform_name = "mac"
elif sys.platform == "win32":
    platform_name = "windows"
elif "linux" in sys.platform:
    platform_name = "linux"
else:
    platform_name = ""

if not hasattr(sys.modules[__name__], '__file__'):
    __file__ = inspect.getfile(inspect.currentframe())
else:
    __file__ = sys.modules[__name__].__file__

# get strack connect root path
CONFIG_PATH = os.path.dirname(__file__)
ROOT_PATH = os.path.dirname(CONFIG_PATH)
RUNTIME_PATH = os.path.join(ROOT_PATH, 'runtime')

# append to environment variable
os.environ['ROOT_PATH'] = ROOT_PATH
os.environ['CONFIG_PATH'] = CONFIG_PATH
os.environ['RUNTIME_PATH'] = RUNTIME_PATH
