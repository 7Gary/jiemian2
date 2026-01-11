# peifang.py - 完整修改代码（操作列改为彩色可点击文字，非按钮形式）
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import logo_rc
# from add import AddDialog  # [已移除] 不再直接调用弹窗，改为信号通知 Main
import json
import os



class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self, text, color, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            color: {color};
            font-family: 宋体;
            font-size: 16pt;
            font-weight: bold;
        """)
        self.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class PeifangWindow(QtWidgets.QMainWindow):
    JSON_PATH = "recipes.json"
    
    # [新增] 信号：请求切换到创建配方页面
    go_create_recipe = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.all_recipes = []
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._combo_aligned = False
        self.align_combo_boxes()

        self.ui.pushButton.clicked.connect(self.filter_recipes)

        if hasattr(self.ui, 'frame'):
             # 尝试移除子页面自带的顶部导航条，由 main.py 统一管理
            self.ui.frame.hide()

        # 隐藏原 UI 中用于模拟表格的控件

        for widget_name in ["textBrowser_2", "textBrowser_3", "textBrowser_4",
                            "textBrowser_5", "textBrowser_6", "textBrowser_7",
                            "label_10", "label_22", "label_23", "label_24",
                            "label_25", "label_26"]:
            widget = getattr(self.ui, widget_name, None)
            if widget is not None:
                widget.hide()

        # 创建真实表格
        self.table = QtWidgets.QTableWidget(self.ui.centralwidget)
        self.table.setGeometry(QtCore.QRect(70, 110, 1460, 600))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["名称", "品类", "幅宽", "颜色", "克重", "操作"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setStyleSheet("""
        /* ===== 内容区：关闭 hover / selected ===== */
        QTableWidget::item:hover {
            background: transparent;
        }
        QTableWidget::item:selected {
            background: transparent;
        }

        /* ===== 表头：关闭 hover / pressed ===== */
        QHeaderView::section {
            background-color: rgb(240, 240, 240);   /* 表头底色，可按需改 */
            color: black;
            border: 1px solid rgb(200, 200, 200);
        }

        QHeaderView::section:hover {
            background-color: rgb(240, 240, 240);
        }

        QHeaderView::section:pressed {
            background-color: rgb(240, 240, 240);
        }
        """)

        font = QtGui.QFont("宋体", 14)
        self.table.setFont(font)
        self.table.horizontalHeader().setFont(font)
        self.table.horizontalHeader().setFixedHeight(45)

        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 400)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 300)

        self.load_recipes()

        # 连接“创建配方”按钮：改为发射信号通知 Main 切换页面
        self.ui.pushButton_2.clicked.connect(lambda: self.go_create_recipe.emit())

    def load_recipes(self):

        if not os.path.exists(self.JSON_PATH):
            return

        with open(self.JSON_PATH, "r", encoding="utf-8") as f:
            try:
                self.all_recipes = json.load(f)
            except json.JSONDecodeError:
                self.all_recipes = []

        self.init_filter_boxes()
        self.refresh_table(self.all_recipes)

    def save_recipes(self):
        recipes = []
        for row in range(self.table.rowCount()):
            recipes.append({
                "name": self.table.item(row, 0).text() if self.table.item(row, 0) else "",
                "category": self.table.item(row, 1).text() if self.table.item(row, 1) else "",
                "width": self.table.item(row, 2).text() if self.table.item(row, 2) else "",
                "color": self.table.item(row, 3).text() if self.table.item(row, 3) else "",
                "gram": self.table.item(row, 4).text() if self.table.item(row, 4) else "",
            })
        with open(self.JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(recipes, f, ensure_ascii=False, indent=2)
# def open_add_dialog(self):
    #     add_dialog = AddDialog(self)
    #     add_dialog.recipe_saved.connect(self.on_recipe_saved)
    #     add_dialog.exec_()

    # 供外部调用（From Main）：当 AddPage 保存成功时调用
    def on_recipe_saved(self, data):
        self.all_recipes.append(data)

        self.all_recipes.append(data)
        self.save_recipes()
        self.init_filter_boxes()
        self.refresh_table(self.all_recipes)

    def on_delete_clicked(self):
        label = self.sender()
        if not label:
            return

        cell_widget = label.parent()
        if not cell_widget:
            return

        index = self.table.indexAt(cell_widget.pos())
        if not index.isValid():
            return

        row = index.row()
        self.delete_row(row)

    def delete_row(self, row):

        name = self.table.item(row, 0).text()
        self.all_recipes = [
            r for r in self.all_recipes
            if r.get("name") != name
        ]

        self.save_recipes()
        self.init_filter_boxes()
        self.refresh_table(self.all_recipes)

    def init_filter_boxes(self):
        # 清空
        self.ui.comboBox.clear()
        self.ui.comboBox_2.clear()
        self.ui.comboBox_3.clear()
        self.ui.comboBox_4.clear()

        # 全部选项
        self.ui.comboBox.addItem("全部")
        self.ui.comboBox_2.addItem("全部")
        self.ui.comboBox_3.addItem("全部")
        self.ui.comboBox_4.addItem("全部")

        categories = set()
        widths = set()
        colors = set()
        grams = set()

        for r in self.all_recipes:
            categories.add(r.get("category", ""))
            widths.add(r.get("width", ""))
            colors.add(r.get("color", ""))
            grams.add(r.get("gram", ""))

        self.ui.comboBox.addItems(sorted(categories))
        self.ui.comboBox_2.addItems(sorted(widths))
        self.ui.comboBox_3.addItems(sorted(colors))
        self.ui.comboBox_4.addItems(sorted(grams))

    def align_combo_boxes(self):
        if self._combo_aligned:
            return

        combo_font = QtGui.QFont("宋体", 16)
        combo_height = 24
        combo_width = 195

        for cb in (self.ui.comboBox, self.ui.comboBox_2, self.ui.comboBox_3, self.ui.comboBox_4):
            cb.setFont(combo_font)
            cb.setFixedHeight(combo_height)
            cb.setFixedWidth(combo_width)

        self._combo_aligned = True

    def refresh_table(self, data_list):
        self.table.setRowCount(0)
        for data in data_list:
            self.add_row_to_table(data)

    def create_center_item(self, text):
        item = QtWidgets.QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def filter_recipes(self):
        category = self.ui.comboBox.currentText()
        width = self.ui.comboBox_2.currentText()
        color = self.ui.comboBox_3.currentText()
        gram = self.ui.comboBox_4.currentText()

        result = []

        for r in self.all_recipes:
            if category != "全部" and r.get("category") != category:
                continue
            if width != "全部" and r.get("width") != width:
                continue
            if color != "全部" and r.get("color") != color:
                continue
            if gram != "全部" and r.get("gram") != gram:
                continue
            result.append(r)

        self.refresh_table(result)

    def add_row_to_table(self, data):
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, self.create_center_item(data.get("name", "")))
        self.table.setItem(row, 1, self.create_center_item(data.get("category", "")))
        self.table.setItem(row, 2, self.create_center_item(data.get("width", "")))
        self.table.setItem(row, 3, self.create_center_item(data.get("color", "")))
        self.table.setItem(row, 4, self.create_center_item(data.get("gram", "")))

        # 操作列：4个彩色可点击文字（非按钮）
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(55, 5, 55, 5)
        layout.setSpacing(22)  # 文字间距
        # 关键：整体居中
        layout.setAlignment(QtCore.Qt.AlignCenter)

        label_zhijian = ClickableLabel("质检", "rgb(0, 85, 255)")
        label_xunlian = ClickableLabel("训练", "rgb(0, 85, 255)")
        label_bianji = ClickableLabel("编辑", "rgb(0, 85, 255)")
        label_shanchu = ClickableLabel("删除", "rgb(0, 85, 255)")

        layout.addWidget(label_zhijian)
        layout.addWidget(label_xunlian)
        layout.addWidget(label_bianji)
        layout.addWidget(label_shanchu)

        widget.setLayout(layout)

        self.table.setCellWidget(row, 5, widget)

        # 点击事件
        label_shanchu.clicked.connect(self.on_delete_clicked)
        label_zhijian.clicked.connect(lambda: print(f"质检 第 {row+1} 行"))
        label_xunlian.clicked.connect(lambda: print(f"训练 第 {row+1} 行"))
        label_bianji.clicked.connect(lambda: print(f"编辑 第 {row+1} 行"))


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1590, 633)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1591, 51))
        self.frame.setStyleSheet("background-color: rgb(227, 227, 227);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(10, 0, 71, 51))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap(":/new/prefix1/images/logo.png"))
        self.label_6.setObjectName("label_6")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(90, 10, 151, 31))
        self.label.setStyleSheet("font: 18pt \"宋体\";")
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(660, 10, 61, 31))
        self.label_3.setStyleSheet("font: 22pt \"宋体\";")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(780, 10, 61, 31))
        self.label_4.setStyleSheet("font: 22pt \"宋体\";")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(900, 10, 61, 31))
        self.label_5.setStyleSheet("font: 22pt \"宋体\";")
        self.label_5.setObjectName("label_5")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setGeometry(QtCore.QRect(1520, 10, 51, 31))
        self.label_7.setStyleSheet("font: 18pt \"宋体\";")
        self.label_7.setObjectName("label_7")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setEnabled(True)
        self.label_2.setGeometry(QtCore.QRect(540, 10, 61, 31))
        self.label_2.setStyleSheet("font: 22pt \"宋体\";")
        self.label_2.setObjectName("label_2")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(70, 70, 41, 21))
        self.label_8.setStyleSheet("font: 16pt \"宋体\";")
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(330, 70, 41, 21))
        self.label_9.setStyleSheet("font: 16pt \"宋体\";")
        self.label_9.setObjectName("label_9")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(590, 70, 41, 21))
        self.label_11.setStyleSheet("font: 16pt \"宋体\";")
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(850, 70, 41, 21))
        self.label_12.setStyleSheet("font: 16pt \"宋体\";")
        self.label_12.setObjectName("label_12")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(120, 70, 181, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(380, 70, 181, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(640, 70, 181, 22))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_4 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_4.setGeometry(QtCore.QRect(900, 70, 181, 22))
        self.comboBox_4.setObjectName("comboBox_4")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(25, 51, 1541, 691))
        self.textBrowser.setStyleSheet("border-color: rgb(193, 193, 193);")
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(70, 110, 291, 41))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(170, 120, 41, 21))
        self.label_10.setStyleSheet("font: 16pt \"宋体\";")
        self.label_10.setObjectName("label_10")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_3.setGeometry(QtCore.QRect(355, 110, 211, 41))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        self.label_22.setGeometry(QtCore.QRect(440, 120, 41, 21))
        self.label_22.setStyleSheet("font: 16pt \"宋体\";")
        self.label_22.setObjectName("label_22")
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_4.setGeometry(QtCore.QRect(560, 110, 121, 41))
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        self.label_23.setGeometry(QtCore.QRect(600, 120, 41, 21))
        self.label_23.setStyleSheet("font: 16pt \"宋体\";")
        self.label_23.setObjectName("label_23")
        self.textBrowser_5 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_5.setGeometry(QtCore.QRect(680, 110, 161, 41))
        self.textBrowser_5.setObjectName("textBrowser_5")
        self.label_24 = QtWidgets.QLabel(self.centralwidget)
        self.label_24.setGeometry(QtCore.QRect(740, 120, 41, 21))
        self.label_24.setStyleSheet("font: 16pt \"宋体\";")
        self.label_24.setObjectName("label_24")
        self.textBrowser_6 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_6.setGeometry(QtCore.QRect(840, 110, 101, 41))
        self.textBrowser_6.setObjectName("textBrowser_6")
        self.label_25 = QtWidgets.QLabel(self.centralwidget)
        self.label_25.setGeometry(QtCore.QRect(870, 120, 41, 21))
        self.label_25.setStyleSheet("font: 16pt \"宋体\";")
        self.label_25.setObjectName("label_25")
        self.textBrowser_7 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_7.setGeometry(QtCore.QRect(940, 110, 591, 41))
        self.textBrowser_7.setObjectName("textBrowser_7")
        self.label_26 = QtWidgets.QLabel(self.centralwidget)
        self.label_26.setGeometry(QtCore.QRect(1220, 120, 41, 21))
        self.label_26.setStyleSheet("font: 16pt \"宋体\";")
        self.label_26.setObjectName("label_26")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1320, 70, 91, 31))
        self.pushButton.setStyleSheet(
            "background-color: rgb(0, 85, 255);"
            "color: white;"
            "font: 14pt \"宋体\";"
        )

        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1440, 70, 91, 31))
        self.pushButton_2.setStyleSheet(
            "background-color: rgb(0, 85, 255);"
            "color: white;"
            "font: 14pt \"宋体\";"
        )

        self.pushButton_2.setObjectName("pushButton_2")

        self.textBrowser.raise_()
        self.frame.raise_()
        self.label_8.raise_()
        self.label_9.raise_()
        self.label_11.raise_()
        self.label_12.raise_()
        self.comboBox.raise_()
        self.comboBox_2.raise_()
        self.comboBox_3.raise_()
        self.comboBox_4.raise_()
        self.textBrowser_2.raise_()
        self.label_10.raise_()
        self.textBrowser_3.raise_()
        self.label_22.raise_()
        self.textBrowser_4.raise_()
        self.label_23.raise_()
        self.textBrowser_5.raise_()
        self.label_24.raise_()
        self.textBrowser_6.raise_()
        self.label_25.raise_()
        self.textBrowser_7.raise_()
        self.label_26.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "AI智能验布机"))
        self.label_3.setText(_translate("MainWindow", "配方"))
        self.label_4.setText(_translate("MainWindow", "历史"))
        self.label_5.setText(_translate("MainWindow", "配置"))
        self.label_7.setText(_translate("MainWindow", "退出"))
        self.label_2.setText(_translate("MainWindow", "质检"))
        self.label_8.setText(_translate("MainWindow", "品类"))
        self.label_9.setText(_translate("MainWindow", "幅度"))
        self.label_11.setText(_translate("MainWindow", "颜色"))
        self.label_12.setText(_translate("MainWindow", "克重"))
        self.label_10.setText(_translate("MainWindow", "名称"))
        self.label_22.setText(_translate("MainWindow", "品类"))
        self.label_23.setText(_translate("MainWindow", "幅宽"))
        self.label_24.setText(_translate("MainWindow", "颜色"))
        self.label_25.setText(_translate("MainWindow", "克重"))
        self.label_26.setText(_translate("MainWindow", "操作"))
        self.pushButton.setText(_translate("MainWindow", "查 询"))
        self.pushButton_2.setText(_translate("MainWindow", "创建配方"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = PeifangWindow()
    window.show()
    sys.exit(app.exec_())