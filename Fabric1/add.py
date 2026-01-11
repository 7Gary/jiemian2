# add.py - 修改后完整代码（支持点击“保存”收集输入并通过信号返回数据）
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal

class Ui_add(object):
    # === 你的原始 setupUi 和 retranslateUi 保持完全不变 ===
    def setupUi(self, add):
        add.setObjectName("add")
        add.resize(1597, 658)
        self.frame = QtWidgets.QFrame(add)
        self.frame.setGeometry(QtCore.QRect(-10, 0, 1591, 51))
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
        self.label_10 = QtWidgets.QLabel(add)
        self.label_10.setGeometry(QtCore.QRect(40, 80, 91, 21))
        self.label_10.setStyleSheet("font: 16pt \"宋体\";")
        self.label_10.setObjectName("label_10")
        self.label_23 = QtWidgets.QLabel(add)
        self.label_23.setGeometry(QtCore.QRect(300, 80, 41, 21))
        self.label_23.setStyleSheet("font: 16pt \"宋体\";")
        self.label_23.setObjectName("label_23")
        self.label_13 = QtWidgets.QLabel(add)
        self.label_13.setGeometry(QtCore.QRect(180, 80, 41, 21))
        self.label_13.setStyleSheet("font: 16pt \"宋体\";")
        self.label_13.setObjectName("label_13")
        self.label_11 = QtWidgets.QLabel(add)
        self.label_11.setGeometry(QtCore.QRect(61, 161, 84, 21))
        self.label_11.setStyleSheet("font: 16pt \"宋体\";")
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(add)
        self.label_12.setGeometry(QtCore.QRect(60, 222, 81, 24))
        self.label_12.setStyleSheet("font: 16pt \"宋体\";")
        self.label_12.setObjectName("label_12")
        self.label_14 = QtWidgets.QLabel(add)
        self.label_14.setGeometry(QtCore.QRect(61, 345, 81, 24))
        self.label_14.setStyleSheet("font: 16pt \"宋体\";")
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(add)
        self.label_15.setGeometry(QtCore.QRect(61, 284, 81, 24))
        self.label_15.setStyleSheet("font: 16pt \"宋体\";")
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(add)
        self.label_16.setGeometry(QtCore.QRect(490, 540, 81, 24))
        self.label_16.setStyleSheet("font: 16pt \"宋体\";\n"
"background-color: rgb(255, 0, 0);")
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(add)
        self.label_17.setGeometry(QtCore.QRect(700, 540, 81, 24))
        self.label_17.setStyleSheet("font: 16pt \"宋体\";\n"
"background-color: rgb(188, 188, 188);")
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(add)
        self.label_18.setGeometry(QtCore.QRect(920, 540, 81, 24))
        self.label_18.setStyleSheet("font: 16pt \"宋体\";\n"
"background-color: rgb(188, 188, 188);")
        self.label_18.setObjectName("label_18")
        self.textBrowser = QtWidgets.QTextBrowser(add)
        self.textBrowser.setGeometry(QtCore.QRect(20, 110, 1541, 411))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_4 = QtWidgets.QTextBrowser(add)
        self.textBrowser_4.setGeometry(QtCore.QRect(260, 70, 121, 41))
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.textBrowser_2 = QtWidgets.QTextBrowser(add)
        self.textBrowser_2.setGeometry(QtCore.QRect(20, 70, 121, 41))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.textBrowser_3 = QtWidgets.QTextBrowser(add)
        self.textBrowser_3.setGeometry(QtCore.QRect(140, 70, 121, 41))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.textBrowser_6 = QtWidgets.QTextBrowser(add)
        self.textBrowser_6.setGeometry(QtCore.QRect(160, 150, 731, 41))
        self.textBrowser_6.setObjectName("textBrowser_6")
        self.textBrowser_7 = QtWidgets.QTextBrowser(add)
        self.textBrowser_7.setGeometry(QtCore.QRect(160, 210, 731, 41))
        self.textBrowser_7.setObjectName("textBrowser_7")
        self.textBrowser_8 = QtWidgets.QTextBrowser(add)
        self.textBrowser_8.setGeometry(QtCore.QRect(160, 270, 731, 41))
        self.textBrowser_8.setObjectName("textBrowser_8")
        self.textBrowser_9 = QtWidgets.QTextBrowser(add)
        self.textBrowser_9.setGeometry(QtCore.QRect(160, 340, 731, 41))
        self.textBrowser_9.setObjectName("textBrowser_9")
        self.textBrowser.raise_()
        self.textBrowser_3.raise_()
        self.textBrowser_2.raise_()
        self.textBrowser_4.raise_()
        self.frame.raise_()
        self.label_10.raise_()
        self.label_23.raise_()
        self.label_13.raise_()
        self.label_11.raise_()
        self.label_12.raise_()
        self.label_14.raise_()
        self.label_15.raise_()
        self.label_16.raise_()
        self.label_17.raise_()
        self.label_18.raise_()
        self.textBrowser_6.raise_()
        self.textBrowser_7.raise_()
        self.textBrowser_8.raise_()
        self.textBrowser_9.raise_()

        self.retranslateUi(add)
        QtCore.QMetaObject.connectSlotsByName(add)

    def retranslateUi(self, add):
        _translate = QtCore.QCoreApplication.translate
        add.setWindowTitle(_translate("add", "Dialog"))
        self.label.setText(_translate("add", "AI智能验布机"))
        self.label_3.setText(_translate("add", "配方"))
        self.label_4.setText(_translate("add", "历史"))
        self.label_5.setText(_translate("add", "配置"))
        self.label_7.setText(_translate("add", "退出"))
        self.label_2.setText(_translate("add", "质检"))
        self.label_10.setText(_translate("add", "基本信息"))
        self.label_23.setText(_translate("add", "模型"))
        self.label_13.setText(_translate("add", "相机"))
        self.label_11.setText(_translate("add", "配方名称"))
        self.label_12.setText(_translate("add", "<html><head/><body><p align=\"center\">品 类</p></body></html>"))
        self.label_14.setText(_translate("add", "<html><head/><body><p align=\"center\">幅 宽</p></body></html>"))
        self.label_15.setText(_translate("add", "<html><head/><body><p align=\"center\">颜 色</p></body></html>"))
        self.label_16.setText(_translate("add", "<html><head/><body><p align=\"center\">删 除</p></body></html>"))
        self.label_17.setText(_translate("add", "<html><head/><body><p align=\"center\">取 消</p></body></html>"))
        self.label_18.setText(_translate("add", "<html><head/><body><p align=\"center\">保 存</p></body></html>"))


# ==================== 包装类：实现按钮逻辑 + 保存信号 ====================
# [修改] 继承自 QWidget，不再是 QDialog (为了嵌入 MainStack)
class AddPage(QtWidgets.QWidget):
    recipe_saved = pyqtSignal(dict)  # 保存时发射配方数据
    cancel_signal = pyqtSignal()     # 取消时发射信号
    go_model_signal = pyqtSignal()   # [新增] 跳转到模型页面的信号

    def replace_textbrowser_with_lineedit(self, tb: QtWidgets.QTextBrowser):
        parent = tb.parent()


        line = QtWidgets.QLineEdit(parent)
        line.setGeometry(tb.geometry())  # 完全复用原位置
        line.setFont(QtGui.QFont("宋体", 16))
        line.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        line.setStyleSheet("""
        QLineEdit {
            border: 1px solid rgb(200, 200, 200);
            border-radius: 3px;
            padding-left: 6px;
            background: white;
        }

        QLineEdit:focus {
            border: 1px solid rgb(200, 200, 200);  
            outline: none;
        }
        """)

        tb.hide()  # 隐藏原 QTextBrowser
        tb.deleteLater()

        return line

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_add()
        self.ui.setupUi(self)

        # [新增] 隐藏自带的顶部 Frame，使用 Main 的统一导航
        if hasattr(self.ui, 'frame'):
            self.ui.frame.hide()

        # ===== 用 QLineEdit 替换 QTextBrowser（表单输入专用）=====
        self.name_edit = self.replace_textbrowser_with_lineedit(self.ui.textBrowser_6)
        self.category_edit = self.replace_textbrowser_with_lineedit(self.ui.textBrowser_7)
        self.color_edit = self.replace_textbrowser_with_lineedit(self.ui.textBrowser_8)
        self.width_edit = self.replace_textbrowser_with_lineedit(self.ui.textBrowser_9)

        # 让三个标签像按钮
        cursor = QtGui.QCursor(Qt.PointingHandCursor)
        self.ui.label_16.setCursor(cursor)  # 删除
        self.ui.label_17.setCursor(cursor)  # 取消
        self.ui.label_18.setCursor(cursor)  # 保存
        
        # [新增] 让上方三个词（包括“模型”）也支持点击
        self.ui.label_10.setCursor(cursor) # 基本信息
        self.ui.label_13.setCursor(cursor) # 相机
        self.ui.label_23.setCursor(cursor) # 模型

        # 绑定“模型”跳转
        self.ui.label_23.mousePressEvent = lambda event: self.go_model_signal.emit()

        # 取消：不再 reject()，而是发射取消信号
        self.ui.label_17.mousePressEvent = lambda event: self.cancel_signal.emit()

        # 保存：收集数据，发射信号
        self.ui.label_18.mousePressEvent = lambda event: self.save_recipe()

        # 删除：清空输入（可选）
        self.ui.label_16.mousePressEvent = lambda event: self.clear_inputs()


    def clear_inputs(self):
        self.name_edit.clear()
        self.category_edit.clear()
        self.color_edit.clear()
        self.width_edit.clear()

    def save_recipe(self):
        name = self.name_edit.text().strip()
        category = self.category_edit.text().strip()
        width = self.width_edit.text().strip()
        color = self.color_edit.text().strip()
        gram = "85, 95"

        data = {
            "name": name,
            "category": category,
            "width": width,
            "color": color,
            "gram": gram
        }

        self.recipe_saved.emit(data)
        # 不需要关闭窗口了，直接发信号

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = AddPage()
    dialog.show()
    sys.exit(app.exec_())
    dialog = AddDialog()
    dialog.show()
    sys.exit(app.exec_())