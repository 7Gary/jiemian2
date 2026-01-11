# xiangqing.py - 历史详情 "布料详情" 界面
# -*- coding: utf-8 -*-

import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

import logo_rc  # 复用项目已有资源，显示左上角 logo


class DefectMapWidget(QtWidgets.QWidget):
    """左侧缺陷分布示意区域（画纵向刻度和红色编号）"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(360)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        rect = self.rect()
        painter.fillRect(rect, QtGui.QColor(247, 247, 247))

        # 左侧纵向刻度数字（模拟 135,130,...,85）
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = QtGui.QFont("宋体", 9)
        painter.setFont(font)

        top_margin = 40
        bottom_margin = 40
        h = rect.height() - top_margin - bottom_margin
        values = [135, 130, 125, 120, 115, 110, 105, 100, 95, 90, 85]
        for i, v in enumerate(values):
            y = top_margin + h * i / (len(values) - 1)
            painter.drawText(5, int(y + 4), str(v))

        # 顶部横向小刻度（1~12）
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        header_values = list(range(1, 13))
        left_offset = 40
        right_offset = 30
        w = rect.width() - left_offset - right_offset
        for i, v in enumerate(header_values):
            x = left_offset + w * i / (len(header_values) - 1)
            painter.drawText(int(x - 3), 25, str(v))

        # 几个红色编号点（示意缺陷位置）
        painter.setPen(QtGui.QPen(QtGui.QColor(220, 0, 0)))
        painter.setFont(QtGui.QFont("宋体", 12, QtGui.QFont.Bold))

        # 大致对应截图里的 1/2/3/4 位置
        points = [
            (70, rect.height() - 80, "1"),
            (140, rect.height() - 150, "2"),
            (240, rect.height() - 210, "3"),
            (190, rect.height() - 260, "4"),
        ]
        for x, y, t in points:
            painter.drawText(int(x), int(y), t)


class XiangqingWindow(QtWidgets.QMainWindow):
    """历史详情：单卷布料的缺陷分布 + 大图预览"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AI智能验布机 - XYZ 340 - 历史详情")
        self.resize(1220, 680)

        self._init_ui()

    def _init_ui(self):
        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)

        main_layout = QtWidgets.QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # [修改] 移除子页面自带顶部，由 main.py 统一管理
        # header_frame = QtWidgets.QFrame() ...
        # main_layout.addWidget(header_frame)

        # 第二行：编号、品类、幅宽、颜色、克重、长度、时间、质检员
        info_frame = QtWidgets.QFrame()
        info_frame.setMinimumHeight(40)
        info_frame.setMaximumHeight(40)
        info_layout = QtWidgets.QHBoxLayout(info_frame)
        info_layout.setContentsMargins(15, 5, 15, 5)
        info_layout.setSpacing(20)

        font_info = QtGui.QFont("宋体", 10)

        def add_pair(label_text, value_text):
            l = QtWidgets.QLabel(label_text)
            l.setFont(font_info)
            v = QtWidgets.QLabel(value_text)
            v.setFont(font_info)
            info_layout.addWidget(l)
            info_layout.addWidget(v)
            return v

        self.label_id = add_pair("编号:", "202508080001")
        self.label_category = add_pair("品类:", "再生春亚纺")
        self.label_width = add_pair("幅宽:", "2300~2600")
        self.label_color = add_pair("颜色:", "米白")
        self.label_gram = add_pair("克重:", "85")
        self.label_length = add_pair("长度:", "288.88")
        self.label_time = add_pair("时间:", "2025-08-08 08:08:08")
        self.label_operator = add_pair("质检员:", "王富贵")

        info_layout.addStretch(1)

        main_layout.addWidget(info_frame)

        # 中间主体：左侧缺陷分布 + 右侧大图
        body_frame = QtWidgets.QFrame()
        body_layout = QtWidgets.QHBoxLayout(body_frame)
        body_layout.setContentsMargins(5, 5, 5, 5)
        body_layout.setSpacing(10)

        self.defect_widget = DefectMapWidget(body_frame)
        body_layout.addWidget(self.defect_widget, 1)

        # 中间的左右切换箭头（简单用 "<" 和 ">" 按钮表示）
        self.btn_prev = QtWidgets.QToolButton(body_frame)
        self.btn_prev.setText("<")
        self.btn_prev.setFixedWidth(24)
        body_layout.addWidget(self.btn_prev, 0, Qt.AlignVCenter)

        # 大图区域
        self.image_label = QtWidgets.QLabel(body_frame)
        self.image_label.setMinimumSize(700, 450)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #F2F2F2;")
        body_layout.addWidget(self.image_label, 4)

        self.btn_next = QtWidgets.QToolButton(body_frame)
        self.btn_next.setText(">")
        self.btn_next.setFixedWidth(24)
        body_layout.addWidget(self.btn_next, 0, Qt.AlignVCenter)

        main_layout.addWidget(body_frame, 1)

        # 底部：是缺陷 / 不是缺陷
        bottom_frame = QtWidgets.QFrame()
        bottom_layout = QtWidgets.QHBoxLayout(bottom_frame)
        bottom_layout.setContentsMargins(0, 10, 0, 10)
        bottom_layout.setSpacing(40)

        self.btn_is_defect = QtWidgets.QPushButton("是缺陷")
        self.btn_not_defect = QtWidgets.QPushButton("不是缺陷")

        self.btn_is_defect.setFont(QtGui.QFont("宋体", 14))
        self.btn_not_defect.setFont(QtGui.QFont("宋体", 14))

        self.btn_is_defect.setStyleSheet("background-color: rgb(255, 0, 0); color: white;")
        self.btn_not_defect.setStyleSheet("background-color: rgb(0, 176, 80); color: white;")

        self.btn_is_defect.setFixedSize(160, 50)
        self.btn_not_defect.setFixedSize(160, 50)

        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.btn_is_defect)
        bottom_layout.addWidget(self.btn_not_defect)
        bottom_layout.addStretch(1)

        main_layout.addWidget(bottom_frame)

        # 加载默认大图（如 1.png），如果不存在则显示灰底
        self._load_default_image()

    def _load_default_image(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(base_dir, "1.png"),
            os.path.join(base_dir, "2.png"),
            os.path.join(base_dir, "images", "1.png"),
            os.path.join(base_dir, "images", "2.png"),
        ]
        pix = QtGui.QPixmap()
        for p in candidates:
            if os.path.exists(p):
                pix = QtGui.QPixmap(p)
                if not pix.isNull():
                    break
        if pix.isNull():
            # 没有图片时，仅保持灰色背景
            self.image_label.setText("")
            return
        scaled = pix.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # 窗口尺寸变化时，重新调整大图缩放
        if self.image_label.pixmap() is not None:
            pix = self.image_label.pixmap()
            if pix is not None and not pix.isNull():
                original = pix
                scaled = original.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled)

    def load_data(self, record):
        """接收 main.py 传来的字典数据，填入界面"""
        if not record:
            return
        
        # 使用安全的 getattr 或 get 方法，防止 key 不存在报错
        # 注意：这里假设 _init_ui 里已经创建了这些 self.label_xxx
        if hasattr(self, 'label_id'): self.label_id.setText(str(record.get('id', '')))
        if hasattr(self, 'label_category'): self.label_category.setText(str(record.get('category', '')))
        if hasattr(self, 'label_width'): self.label_width.setText(str(record.get('width', '')))
        if hasattr(self, 'label_color'): self.label_color.setText(str(record.get('color', '')))
        if hasattr(self, 'label_gram'): self.label_gram.setText(str(record.get('gram', '')))
        if hasattr(self, 'label_length'): self.label_length.setText(str(record.get('length', '')))
        if hasattr(self, 'label_time'): self.label_time.setText(str(record.get('time', '')))
        if hasattr(self, 'label_operator'): self.label_operator.setText(str(record.get('operator', '')))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = XiangqingWindow()
    win.show()
    sys.exit(app.exec_())
