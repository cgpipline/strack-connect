# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

# Load UI resources such as icons.

from strack_connect.config.env import Env
Env()

from .theme import MTheme
dayu_theme = MTheme('dark', primary_color=MTheme.orange)