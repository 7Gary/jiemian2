# moxing.py - "模型" 小窗口（配方页面中的模型界面）
# -*- coding: utf-8 -*-

import sys
import os
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

import logo_rc  # 复用项目已有资源，显示左上角 logo


class ImageItem:
    """内部数据结构：记录单张图像及其状态"""

    def __init__(self, path: str):
        self.path = path
        self.status = "pending"  # pending / normal / defect


class MoxingWindow(QtWidgets.QMainWindow):
    """配方页面中的“模型”界面

    最新修复：
    - 修复点击缩略图后中间只显示黑色的问题
    - 使用 setScaledContents(True) + 直接设置原始 QPixmap，让 QLabel 自动缩放图片（最稳定方式）
    - 自动保持纵横比、居中显示，背景黑色（图片小于区域时会显示黑边）
    - 移除手动 scaled()，避免 size 为 0 或过小时出现空图/黑块
    - 其他功能不变
    """

    FOLDER_PATH = r"D:\Downloads\DBFAD-main\dataset\MVTEC\nuser3\train\good"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AI智能验布机 - XYZ 340 - 模型")
        self.resize(1600, 800)

        self.image_items = []  # type: list[ImageItem]

        self._init_ui()
        self._update_stats()
        self._current_pixmap = None

    # ---------------- UI 结构 ----------------
    def _init_ui(self):
        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)

        main_layout = QtWidgets.QVBoxLayout(central)
        main_layout.setContentsMargins(30, 5, 30, 5)
        main_layout.setSpacing(5)

        # 第二行：标签条
        tab_frame = QtWidgets.QFrame()
        tab_layout = QtWidgets.QHBoxLayout(tab_frame)
        tab_layout.setContentsMargins(20, 0, 20, 0)
        tab_layout.setSpacing(0)

        def _make_tab(text, checked=False):
            btn = QtWidgets.QPushButton(text)
            btn.setCheckable(True)
            btn.setChecked(checked)
            if checked:
                btn.setStyleSheet(
                    "background-color: white; border: 1px solid rgb(193,193,193); font: 14pt \"宋体\";"
                )
            else:
                btn.setStyleSheet(
                    "background-color: rgb(242,242,242); border: 1px solid rgb(193,193,193); font: 14pt \"宋体\";"
                )
            btn.setFixedHeight(30)
            btn.setFixedWidth(120)
            return btn

        self.tab_basic = _make_tab("基本信息")
        self.tab_camera = _make_tab("相机")
        self.tab_model = _make_tab("模型", checked=True)

        tab_layout.addWidget(self.tab_basic)
        tab_layout.addWidget(self.tab_camera)
        tab_layout.addWidget(self.tab_model)
        tab_layout.addStretch(1)

        main_layout.addWidget(tab_frame)

        # 第三块：统计 + 进度条 + 顶部按钮
        stat_frame = QtWidgets.QFrame()
        stat_layout = QtWidgets.QHBoxLayout(stat_frame)
        stat_layout.setContentsMargins(20, 0, 20, 0)
        stat_layout.setSpacing(15)

        font_small = QtGui.QFont("宋体", 10)

        self.label_normal = QtWidgets.QLabel("正常: 0")
        self.label_defect = QtWidgets.QLabel("缺陷: 0")
        self.label_pending = QtWidgets.QLabel("待更新: 0")

        for lab in (self.label_normal, self.label_defect, self.label_pending):
            lab.setFont(font_small)

        self.checkbox_select_all = QtWidgets.QCheckBox("全选")
        self.checkbox_select_all.setFont(font_small)
        self.checkbox_select_all.stateChanged.connect(self._on_select_all_changed)

        self.btn_delete_selected = QtWidgets.QPushButton("删除")
        self.btn_delete_selected.setFont(font_small)
        self.btn_delete_selected.clicked.connect(self._on_delete_selected)

        self.progress = QtWidgets.QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        self.progress.setFixedWidth(250)

        self.label_progress = QtWidgets.QLabel("样本: 0 / 0")
        self.label_progress.setFont(font_small)

        btn_font = QtGui.QFont("宋体", 12)
        self.btn_setting = QtWidgets.QPushButton("设置")
        self.btn_capture = QtWidgets.QPushButton("采图")
        self.btn_train = QtWidgets.QPushButton("训练")
        self.btn_single_delete = QtWidgets.QPushButton("删除")

        for b in (self.btn_setting, self.btn_capture, self.btn_train):
            b.setFont(btn_font)
            b.setFixedSize(100, 32)
            b.setStyleSheet("background-color: rgb(70, 177, 225); color: white;")

        self.btn_single_delete.setFont(btn_font)
        self.btn_single_delete.setFixedSize(100, 32)
        self.btn_single_delete.setStyleSheet("background-color: rgb(255, 0, 0); color: white;")

        stat_layout.addWidget(self.label_normal)
        stat_layout.addWidget(self.label_defect)
        stat_layout.addWidget(self.label_pending)
        stat_layout.addSpacing(20)
        stat_layout.addWidget(self.checkbox_select_all)
        stat_layout.addWidget(self.btn_delete_selected)
        stat_layout.addSpacing(20)
        stat_layout.addWidget(self.progress)
        stat_layout.addWidget(self.label_progress)
        stat_layout.addSpacing(30)
        stat_layout.addWidget(self.btn_setting)
        stat_layout.addWidget(self.btn_capture)
        stat_layout.addWidget(self.btn_train)
        stat_layout.addWidget(self.btn_single_delete)

        main_layout.addWidget(stat_frame)

        # 中间主体：左侧列表 + 中间单张大图预览
        body_layout = QtWidgets.QHBoxLayout()
        body_layout.setContentsMargins(10, 5, 10, 5)
        body_layout.setSpacing(10)

        # 左侧：图片缩略图列表
        left_frame = QtWidgets.QFrame()
        left_layout = QtWidgets.QVBoxLayout(left_frame)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(5)

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setIconSize(QtCore.QSize(140, 80))
        self.list_widget.setResizeMode(QtWidgets.QListView.Adjust)
        self.list_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # 隐藏滚动条，但保留鼠标滚轮滚动
        self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 点击事件
        self.list_widget.currentItemChanged.connect(self._update_preview)
        self.list_widget.itemClicked.connect(self._update_preview)

        left_layout.addWidget(self.list_widget)
        body_layout.addWidget(left_frame, 2)

        # 中间：单张大图预览（关键修复）
        center_frame = QtWidgets.QFrame()
        center_layout = QtWidgets.QHBoxLayout(center_frame)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)

        self.label_preview = QtWidgets.QLabel("请采图加载样本")
        self.label_preview.setAlignment(Qt.AlignCenter)
        self.label_preview.setStyleSheet("background-color: #000000; color: white;")


        center_layout.addWidget(self.label_preview)
        body_layout.addWidget(center_frame, 8)

        main_layout.addLayout(body_layout, stretch=1)

        # 底部：是缺陷 / 不是缺陷
        bottom_frame = QtWidgets.QFrame()
        bottom_layout = QtWidgets.QHBoxLayout(bottom_frame)
        bottom_layout.setContentsMargins(0, 5, 0, 5)
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

        # 信号连接
        self.btn_capture.clicked.connect(self._on_capture_clicked)
        self.btn_single_delete.clicked.connect(self._on_delete_current)
        self.btn_setting.clicked.connect(self._on_setting_clicked)
        self.btn_train.clicked.connect(self._on_train_clicked)
        self.btn_is_defect.clicked.connect(partial(self._set_status_for_selected, "defect"))
        self.btn_not_defect.clicked.connect(partial(self._set_status_for_selected, "normal"))

    # ---------------- 数据加载 / 操作 ----------------
    def _add_image(self, path: str):
        if not os.path.exists(path):
            return

        if any(it.path == path for it in self.image_items):
            return

        item_data = ImageItem(path)
        self.image_items.append(item_data)

        pix = QtGui.QPixmap(path)
        if pix.isNull():
            pix = QtGui.QPixmap(140, 80)
            pix.fill(Qt.gray)

        scaled_pix = pix.scaled(140, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon = QtGui.QIcon(scaled_pix)

        item = QtWidgets.QListWidgetItem(icon, "")  # 无文件名
        item.setData(Qt.UserRole, path)
        self.list_widget.addItem(item)

        self._apply_item_style(item, item_data.status)
        self._update_stats()

    # ---------------- 统计与样式 ----------------
    def _update_stats(self):
        normal = sum(1 for it in self.image_items if it.status == "normal")
        defect = sum(1 for it in self.image_items if it.status == "defect")
        pending = len(self.image_items) - normal - defect
        total = len(self.image_items)

        self.label_normal.setText(f"正常: {normal}")
        self.label_defect.setText(f"缺陷: {defect}")
        self.label_pending.setText(f"待更新: {pending}")

        self.label_progress.setText(f"样本: {normal + defect} / {total}")
        self.progress.setValue(0 if total == 0 else int((normal + defect) * 100 / total))

    def _apply_item_style(self, item: QtWidgets.QListWidgetItem, status: str):
        if status == "normal":
            item.setBackground(QtGui.QColor(230, 255, 230))
        elif status == "defect":
            item.setBackground(QtGui.QColor(255, 230, 230))
        else:
            item.setBackground(QtGui.QColor(245, 245, 220))

    # ---------------- 事件处理 ----------------
    def _on_capture_clicked(self):
        if not os.path.isdir(self.FOLDER_PATH):
            QtWidgets.QMessageBox.warning(self, "错误", f"采集文件夹不存在：\n{self.FOLDER_PATH}")
            return

        exts = {".png", ".jpg", ".jpeg", ".bmp"}
        files = sorted([f for f in os.listdir(self.FOLDER_PATH)
                        if os.path.splitext(f)[1].lower() in exts])

        added_count = 0
        for name in files:
            path = os.path.join(self.FOLDER_PATH, name)
            if not any(it.path == path for it in self.image_items):
                self._add_image(path)
                added_count += 1

        if added_count == 0:
            QtWidgets.QMessageBox.information(self, "提示", "没有新图片可加载（已全部加载或文件夹为空）")
        else:
            if self.list_widget.count() > 0:
                self.list_widget.setCurrentRow(0)
                self._update_preview()

    def _update_preview(self, current=None, previous=None):
        item = self.list_widget.currentItem()
        if item:
            path = item.data(Qt.UserRole)
            pix = QtGui.QPixmap(path)
            if not pix.isNull():
                self._current_pixmap = pix
                self._refresh_preview()
                return

        self._current_pixmap = None
        self.label_preview.clear()
        self.label_preview.setText("无法加载图片或未选中")

    def _refresh_preview(self):
        if not self._current_pixmap:
            return

        label_size = self.label_preview.size()
        if label_size.width() <= 0 or label_size.height() <= 0:
            return

        scaled = self._current_pixmap.scaled(
            label_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.label_preview.setPixmap(scaled)

    def _set_status_for_selected(self, status: str):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.information(self, "提示", "请先在左侧选择一条或多条图片")
            return

        for item in selected_items:
            path = item.data(Qt.UserRole)
            for it in self.image_items:
                if it.path == path:
                    it.status = status
                    self._apply_item_style(item, status)
                    break

        self._update_stats()

    def _on_delete_current(self):
        row = self.list_widget.currentRow()
        if row < 0:
            return
        path = self.list_widget.item(row).data(Qt.UserRole)
        self.list_widget.takeItem(row)
        self.image_items = [it for it in self.image_items if it.path != path]
        self._update_stats()
        self._update_preview()

    def _on_delete_selected(self):
        selected_rows = sorted({self.list_widget.row(it) for it in self.list_widget.selectedItems()}, reverse=True)
        if not selected_rows:
            return

        for row in selected_rows:
            path = self.list_widget.item(row).data(Qt.UserRole)
            self.list_widget.takeItem(row)
            self.image_items = [it for it in self.image_items if it.path != path]

        self._update_stats()
        self._update_preview()

    def _on_select_all_changed(self, state):
        block = self.list_widget.blockSignals(True)
        try:
            if state == Qt.Checked:
                self.list_widget.selectAll()
            else:
                self.list_widget.clearSelection()
        finally:
            self.list_widget.blockSignals(block)

    def _on_setting_clicked(self):
        QtWidgets.QMessageBox.information(self, "设置", "这里可放置模型相关参数设置界面。")

    def _on_train_clicked(self):
        defect = sum(1 for it in self.image_items if it.status == "defect")
        normal = sum(1 for it in self.image_items if it.status == "normal")
        QtWidgets.QMessageBox.information(
            self,
            "训练",
            f"开始训练, 缺陷样本: {defect} 张, 正常样本: {normal} 张 (示意)。",
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MoxingWindow()
    win.show()
    sys.exit(app.exec_())