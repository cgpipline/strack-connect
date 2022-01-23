#!/usr/bin/env python
# coding=utf-8
from dayu_widgets.qt import QWidget, QHBoxLayout, Qt
from dayu_widgets.label import MLabel
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.tool_button import MToolButton


class BarTopSelect(QWidget):
    def __init__(self, parent=None):
        super(BarTopSelect, self).__init__(parent)
        self.top_main_lay = QHBoxLayout()
        self._init_ui()
        self.setLayout(self.top_main_lay)
    
    def _init_ui(self):
        self.project_type = MComboBox()
        self.project_type.setMaximumSize(300, 60)
        self.top_main_lay.addWidget(self.project_type)
        self.bar_title = MLabel(u"名称").h4()
        self.bar_title.setAlignment(Qt.AlignCenter)
        self.top_main_lay.addWidget(self.bar_title)

        self.search_text = MLineEdit()
        self.search_text.search()
        self.search_text.setPlaceholderText("输入搜索名称")
        self.search_text.setMaximumSize(200, 60)
        self.search_text.set_prefix_widget(MToolButton().svg('search_line.svg').icon_only())
        self.top_main_lay.addWidget(self.search_text)
