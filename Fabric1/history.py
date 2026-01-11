# history.py - "历史"窗口
# -*- coding: utf-8 -*-

import sys
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

import logo_rc  # 使用已有的资源文件，显示左上角 logo


class ClickableLabel(QtWidgets.QLabel):
    """表格里“查看 / 删除”使用的可点击文本标签"""
    clicked = QtCore.pyqtSignal()

    def __init__(self, text, color, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            color: {color};
            font-family: 宋体;
            font-size: 12pt;
        """)
        self.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class HistoryWindow(QtWidgets.QMainWindow):
    """与截图布局基本一致的“历史”窗口"""
    
    # [新增] 信号：当点击查看时，发射该信号把记录数据传出去
    view_detail_signal = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AI智能验布机 - XYZ 340 - 历史")
        self.resize(1691, 669)

        self._init_ui()
        self._load_fake_data()  # 先放几条演示数据，后续你可改成真实数据源

    # ----------------- UI 布局 -----------------
    def _init_ui(self):
        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)

        main_layout = QtWidgets.QVBoxLayout(central)
        # 左边距改为 30，和 zhijian.ui 顶部 frame 的 x=30 对齐
        main_layout.setContentsMargins(30, 5, 30, 10)
        main_layout.setSpacing(5)

        # [修改] 移除子页面自带的顶部导航条，由 main.py 统一管理
        # 顶部灰色条代码已移除...

        # 第二行：筛选条件区域
        filter_frame = QtWidgets.QFrame()
        filter_frame.setStyleSheet("background-color: rgb(242, 242, 242);")
        filter_layout = QtWidgets.QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(30, 15, 30, 15)
        filter_layout.setSpacing(25)

        label_font = QtGui.QFont("宋体", 12)
        combo_font = QtGui.QFont("宋体", 12)

        # 品类
        self.combo_category = QtWidgets.QComboBox()
        self.combo_category.setFont(combo_font)
        self.combo_category.setFixedWidth(150)
        self.combo_category.addItems(["全部", "春亚纺", "其他布种"])

        category_label = QtWidgets.QLabel("品类")
        category_label.setFont(label_font)

        # 幅宽
        self.combo_width = QtWidgets.QComboBox()
        self.combo_width.setFont(combo_font)
        self.combo_width.setFixedWidth(150)
        self.combo_width.addItems(["全部", "2300-2600", "2600-3000"])

        width_label = QtWidgets.QLabel("幅宽")
        width_label.setFont(label_font)

        # 颜色
        self.combo_color = QtWidgets.QComboBox()
        self.combo_color.setFont(combo_font)
        self.combo_color.setFixedWidth(150)
        self.combo_color.addItems(["全部", "米白", "本白", "深色"])

        color_label = QtWidgets.QLabel("颜色")
        color_label.setFont(label_font)

        # 克重
        self.combo_gram = QtWidgets.QComboBox()
        self.combo_gram.setFont(combo_font)
        self.combo_gram.setFixedWidth(150)
        self.combo_gram.addItems(["全部", "85", "90", "100"])

        gram_label = QtWidgets.QLabel("克重")
        gram_label.setFont(label_font)

        self.btn_search = QtWidgets.QPushButton("查询")
        btn_font = QtGui.QFont("宋体", 12)
        self.btn_search.setFont(btn_font)
        self.btn_search.setFixedWidth(80)

        filter_layout.addWidget(category_label)
        filter_layout.addWidget(self.combo_category)
        filter_layout.addWidget(width_label)
        filter_layout.addWidget(self.combo_width)
        filter_layout.addWidget(color_label)
        filter_layout.addWidget(self.combo_color)
        filter_layout.addWidget(gram_label)
        filter_layout.addWidget(self.combo_gram)
        filter_layout.addStretch(1)
        filter_layout.addWidget(self.btn_search)

        main_layout.addWidget(filter_frame)

        # 第三块：历史记录表格
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "编号", "品类", "幅宽", "颜色", "克重", "长度(米)", "缺陷数", "时间", "操作员", "操作"
        ])

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        table_font = QtGui.QFont("宋体", 12)
        self.table.setFont(table_font)
        self.table.horizontalHeader().setFont(table_font)
        self.table.horizontalHeader().setFixedHeight(40)

        self.table.setColumnWidth(0, 160)  # 编号
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 100)
        self.table.setColumnWidth(6, 80)
        self.table.setColumnWidth(7, 200)
        self.table.setColumnWidth(8, 80)
        # 第 10 列操作列留给“查看 删除”

        main_layout.addWidget(self.table, stretch=1)

        # 信号连接
        self.btn_search.clicked.connect(self.on_search_clicked)
        # self.nav_exit.mousePressEvent = self._on_exit_clicked

    # ----------------- 数据与行为 -----------------
    def _load_fake_data(self):
        """先放几条演示数据，方便你看到完整界面效果。
        以后可以改成从数据库 / 文件读取。"""
        self.all_records = [
            {
                "id": "2025080808080001",
                "category": "春亚纺",
                "width": "2300",
                "color": "米白",
                "gram": "85",
                "length": "288.88",
                "defects": "9",
                "time": "2025-08-08 08:08:08",
                "operator": "王富贵",
            },
             {
                "id": "2025080808080001",
                "category": "春亚纺",
                "width": "2300",
                "color": "米白",
                "gram": "85",
                "length": "100",
                "defects": "9",
                "time": "2025-08-08 08:08:08",
                "operator": "李",
            }
        ] * 20  # 简单复制多行

        self._refresh_table(self.all_records)

    def _refresh_table(self, records):
        self.table.setRowCount(0)

        for row_idx, rec in enumerate(records):
            self.table.insertRow(row_idx)

            def _set_item(col, text):
                item = QtWidgets.QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col, item)

            _set_item(0, rec.get("id", ""))
            _set_item(1, rec.get("category", ""))
            _set_item(2, rec.get("width", ""))
            _set_item(3, rec.get("color", ""))
            _set_item(4, rec.get("gram", ""))
            _set_item(5, rec.get("length", ""))
            _set_item(6, rec.get("defects", ""))
            _set_item(7, rec.get("time", ""))
            _set_item(8, rec.get("operator", ""))

            # 操作列：查看 / 删除
            op_widget = QtWidgets.QWidget()
            h = QtWidgets.QHBoxLayout(op_widget)
            h.setContentsMargins(0, 0, 0, 0)
            h.setSpacing(10)

            view_label = ClickableLabel("查看", "#0078d7")
            delete_label = ClickableLabel("删除", "#d9534f")

            view_label.clicked.connect(partial(self.on_view_clicked, row_idx))
            delete_label.clicked.connect(partial(self.on_delete_clicked, row_idx))

            h.addStretch(1)
            h.addWidget(view_label)
            h.addWidget(delete_label)
            h.addStretch(1)

            self.table.setCellWidget(row_idx, 9, op_widget)

    # 筛选按钮：这里只是简单演示，实际可按条件过滤 self.all_records
    def on_search_clicked(self):
        # 示例：当前只是重新刷新全部记录
        self._refresh_table(self.all_records)


    def on_view_clicked(self, row):
        rec = self.all_records[row] if 0 <= row < len(self.all_records) else None
        if not rec:
            return
        
        # [新增] 这里不再弹窗，而是发射信号通知 Main 切换到详情页
        self.view_detail_signal.emit(rec)
        
        # msg = (f"编号: {rec['id']}\n品类: {rec['category']}\n幅宽: {rec['width']}\n"
        #        f"颜色: {rec['color']}\n克重: {rec['gram']}\n长度(米): {rec['length']}\n"
        #        f"缺陷数: {rec['defects']}\n时间: {rec['time']}\n操作员: {rec['operator']}")
        # QtWidgets.QMessageBox.information(self, "记录详情", msg)

    def on_delete_clicked(self, row):
        if not (0 <= row < len(self.all_records)):
            return
        reply = QtWidgets.QMessageBox.question(
            self,
            "删除确认",
            "确定要删除这一条历史记录吗？",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )
        if reply != QtWidgets.QMessageBox.Yes:
            return

        self.all_records.pop(row)
        self._refresh_table(self.all_records)

    # def _on_exit_clicked(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.close()
    #     QtWidgets.QLabel.mousePressEvent(self.nav_exit, event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = HistoryWindow()
    win.show()
    sys.exit(app.exec_())
