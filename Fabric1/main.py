# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget

import os
import io
import logo_rc
import switch_off_rc
import switch_on_rc
import requests
from PIL import Image

# ===== API 配置（通过 MobaXterm SSH 隧道）=====
API_URL = "http://localhost:5000/detect"
DETECT_TIMEOUT = 10  # 秒


class Ui_zhijian(object):
    def setupUi(self, zhijian):
        zhijian.setObjectName("zhijian")
        zhijian.resize(1691, 669)
        self.textBrowser = QtWidgets.QTextBrowser(zhijian)
        self.textBrowser.setGeometry(QtCore.QRect(50, 50, 1551, 611))
        self.textBrowser.setStyleSheet("border-color: rgb(193, 193, 193);")
        self.textBrowser.setObjectName("textBrowser")
        self.frame = QtWidgets.QFrame(zhijian)
        self.frame.setGeometry(QtCore.QRect(30, 0, 1591, 51))
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
        self.label.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.label_7.raise_()
        self.label_2.raise_()
        self.label_6.raise_()
        self.textBrowser_2 = QtWidgets.QTextBrowser(zhijian)
        self.textBrowser_2.setGeometry(QtCore.QRect(60, 170, 401, 481))
        self.textBrowser_2.setStyleSheet("background-color: rgb(242, 242, 242);")
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.frame_2 = QtWidgets.QFrame(zhijian)
        self.frame_2.setGeometry(QtCore.QRect(60, 60, 1531, 101))
        self.frame_2.setStyleSheet("background-color: rgb(242, 242, 242);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setGeometry(QtCore.QRect(420, 20, 51, 21))
        self.label_8.setStyleSheet("font: 16pt \"宋体\";")
        self.label_8.setObjectName("label_8")
        self.label_11 = QtWidgets.QLabel(self.frame_2)
        self.label_11.setGeometry(QtCore.QRect(420, 60, 51, 21))
        self.label_11.setStyleSheet("font: 16pt \"宋体\";")
        self.label_11.setObjectName("label_11")
        self.label_9 = QtWidgets.QLabel(self.frame_2)
        self.label_9.setGeometry(QtCore.QRect(680, 20, 51, 21))
        self.label_9.setStyleSheet("font: 16pt \"宋体\";")
        self.label_9.setObjectName("label_9")
        self.label_12 = QtWidgets.QLabel(self.frame_2)
        self.label_12.setGeometry(QtCore.QRect(680, 60, 51, 21))
        self.label_12.setStyleSheet("font: 16pt \"宋体\";")
        self.label_12.setObjectName("label_12")
        self.label_10 = QtWidgets.QLabel(self.frame_2)
        self.label_10.setGeometry(QtCore.QRect(1100, 10, 91, 21))
        self.label_10.setStyleSheet("font: 16pt \"宋体\";")
        self.label_10.setObjectName("label_10")
        self.label_13 = QtWidgets.QLabel(self.frame_2)
        self.label_13.setGeometry(QtCore.QRect(1210, 10, 81, 81))
        self.label_13.setStyleSheet("font: 16pt \"宋体\";\n"
                                    "background-color: rgb(70, 177, 225);")
        self.label_13.setObjectName("label_13")
        self.label_15 = QtWidgets.QLabel(self.frame_2)
        self.label_15.setGeometry(QtCore.QRect(1320, 10, 81, 81))
        self.label_15.setStyleSheet("font: 16pt \"宋体\";\n"
                                    "background-color: rgb(70, 177, 225);")
        self.label_15.setObjectName("label_15")
        self.label_14 = QtWidgets.QLabel(self.frame_2)
        self.label_14.setGeometry(QtCore.QRect(1430, 10, 81, 81))
        self.label_14.setStyleSheet("font: 16pt \"宋体\";\n"
                                    "background-color: rgb(70, 177, 225);")
        self.label_14.setObjectName("label_14")
        self.label_18 = QtWidgets.QLabel(self.frame_2)
        self.label_18.setGeometry(QtCore.QRect(1110, 40, 71, 51))
        self.label_18.setText("")
        self.label_18.setPixmap(QtGui.QPixmap(":/new/prefix1/images/switch_on.png"))
        self.label_18.setObjectName("label_18")
        self.label_18.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.imageLabel = QtWidgets.QLabel(zhijian)
        self.imageLabel.setGeometry(QtCore.QRect(470, 170, 1121, 410))
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel.setStyleSheet("background-color: #F2F2F2;")
        self.imageLabel.setObjectName("imageLabel")

        self.label_16 = QtWidgets.QLabel(zhijian)
        self.label_16.setGeometry(QtCore.QRect(870, 590, 121, 41))
        self.label_16.setStyleSheet("font: 16pt \"宋体\";\n"
                                    "background-color: rgb(255, 0, 0);")
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(zhijian)
        self.label_17.setGeometry(QtCore.QRect(1070, 590, 121, 41))
        self.label_17.setStyleSheet("font: 16pt \"宋体\";\n"
                                    "background-color: rgb(0, 176, 80);")
        self.label_17.setObjectName("label_17")

        self.retranslateUi(zhijian)
        QtCore.QMetaObject.connectSlotsByName(zhijian)

    def retranslateUi(self, zhijian):
        _translate = QtCore.QCoreApplication.translate
        zhijian.setWindowTitle(_translate("zhijian", "Form"))
        self.label.setText(_translate("zhijian", "AI智能验布机"))
        self.label_3.setText(_translate("zhijian", "配方"))
        self.label_4.setText(_translate("zhijian", "历史"))
        self.label_5.setText(_translate("zhijian", "配置"))
        self.label_7.setText(_translate("zhijian", "退出"))
        self.label_2.setText(_translate("zhijian", "质检"))
        self.label_8.setText(_translate("zhijian", "品类："))
        self.label_11.setText(_translate("zhijian", "颜色："))
        self.label_9.setText(_translate("zhijian", "幅宽："))
        self.label_12.setText(_translate("zhijian", "克重："))
        self.label_10.setText(_translate("zhijian", "缺陷停机"))
        self.label_13.setText(_translate("zhijian",
                                         "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">开始/</span></p><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">停止</span></p></body></html>"))
        self.label_15.setText(_translate("zhijian",
                                         "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">下一卷</span></p></body></html>"))
        self.label_14.setText(_translate("zhijian",
                                         "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">换配方</span></p></body></html>"))
        self.label_16.setText(_translate("zhijian",
                                         "<html><head/><body><p align=\"center\"><span style=\" color:#ffffff;\">是缺陷</span></p></body></html>"))
        self.label_17.setText(_translate("zhijian",
                                         "<html><head/><body><p align=\"center\"><span style=\" color:#ffffff;\">不是缺陷</span></p></body></html>"))


class DetectThread(QThread):
    # 子线程绝对不要传 QPixmap，改为传 bytes（线程安全）
    finished = pyqtSignal(bytes, float, bool, str)

    def __init__(self, img_path):
        super().__init__()
        self.img_path = img_path

    def run(self):
        score = 0.0
        is_defect = False
        png_bytes = b""
        err_msg = ""

        try:
            # 读原图 -> PNG bytes（用于 fallback 显示）
            pil_img = Image.open(self.img_path).convert("RGB")
            fallback_buf = io.BytesIO()
            pil_img.save(fallback_buf, format="PNG")
            fallback_buf.seek(0)
            png_bytes = fallback_buf.getvalue()

            # 发给服务端
            files = {"image": ("temp.png", io.BytesIO(png_bytes), "image/png")}
            response = requests.post(API_URL, files=files, timeout=DETECT_TIMEOUT)

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text[:200]}")

            data = response.json()

            if not data.get("ok", False):
                raise Exception(str(data.get("error", "unknown error")))

            # ===== 正确：使用归一化分数 =====
            score = float(data.get("score", 0.0))  # ✅ normalized score (0~1)
            is_defect = bool(data.get("is_defect", False))

            # ===== 可选：仅用于调试 =====
            raw_score = float(data.get("raw_score", -1.0))





        except Exception as e:
            err_msg = str(e)

        self.finished.emit(png_bytes, score, is_defect, err_msg)


class ZhijianWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_zhijian()
        self.ui.setupUi(self)

        self.defect_stop_on = True
        self.update_switch()
        self.ui.label_18.mousePressEvent = self.toggle_switch

        self.running = False
        self.ui.label_13.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ui.label_13.mousePressEvent = self.toggle_run
        self.update_run_button()

        # ===== 改这里：你的图片文件夹路径（模拟实时采集源）=====
        self.image_dir = (r"D:\Downloads\patchcore-inspection-main\datasets\mvtec_anomaly_detection\mvtec_anomaly_detection\nuser3\train\good"
                          r"")

        self.image_list = []
        self.image_index = 0
        self.total_images = 0

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.show_next_image)

        self.current_thread = None
        self.detect_busy = False

    def load_images(self):
        if not os.path.exists(self.image_dir):
            print("目录不存在:", self.image_dir)
            return

        self.image_list = [
            os.path.join(self.image_dir, f)
            for f in os.listdir(self.image_dir)
            if f.lower().endswith((".jpg", ".png", ".bmp"))
        ]
        self.image_list.sort()
        self.total_images = len(self.image_list)
        self.image_index = 0
        print(f"加载 {self.total_images} 张图像（模拟一卷布料）")

        self.ui.textBrowser_2.clear()
        self.ui.textBrowser_2.append(f"新一卷开始，共 {self.total_images} 张图像\n")

    def show_next_image(self):
        if not self.running or not self.image_list:
            return

        if self.detect_busy:
            return

        if self.image_index >= self.total_images:
            self.image_index = 0
            self.ui.textBrowser_2.append("一卷检测完成，循环继续...\n")

        img_path = self.image_list[self.image_index]
        print(f"采集并检测第 {self.image_index + 1}/{self.total_images} 张: {os.path.basename(img_path)}")

        self.detect_busy = True

        self.current_thread = DetectThread(img_path)
        self.current_thread.finished.connect(self.on_detect_finished)
        self.current_thread.finished.connect(self.current_thread.deleteLater)
        self.current_thread.start()

        self.image_index += 1

    def on_detect_finished(self, png_bytes: bytes, score: float, is_defect: bool, err_msg: str):
        # 无论成功失败，都要释放 busy（否则会“卡死不动”）
        self.detect_busy = False

        if err_msg:
            print("检测异常:", err_msg)
            self.ui.textBrowser_2.append(f"检测异常: {err_msg}\n")

        # 主线程把 bytes 转成 QPixmap（线程安全）
        pix = QPixmap()
        if png_bytes:
            pix.loadFromData(png_bytes)

        if pix.isNull():
            return

        label_size = self.ui.imageLabel.size()
        scaled = pix.scaled(label_size, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        x = (scaled.width() - label_size.width()) // 2
        y = (scaled.height() - label_size.height()) // 2
        cropped = scaled.copy(x, y, label_size.width(), label_size.height())
        self.ui.imageLabel.setPixmap(cropped)

        self.ui.textBrowser_2.append(
            f"第 {self.image_index}/{self.total_images} 张\n"
            f"异常分值: {score:.3f}\n"
            f"结果: {'***缺陷***' if is_defect else '正常'}\n"
            f"{'-'*20}\n"
        )
        self.ui.textBrowser_2.moveCursor(QtGui.QTextCursor.End)

        base_red = "font: 16pt \"宋体\"; background-color: rgb(255, 0, 0); color: white;"
        base_green = "font: 16pt \"宋体\"; background-color: rgb(0, 176, 80); color: white;"
        if is_defect:
            self.ui.label_16.setStyleSheet(base_red.replace("16pt", "22pt"))
            self.ui.label_17.setStyleSheet(base_green)
        else:
            self.ui.label_16.setStyleSheet(base_red)
            self.ui.label_17.setStyleSheet(base_green.replace("16pt", "22pt"))

        if is_defect and self.defect_stop_on:
            self.running = False
            self.timer.stop()
            self.update_run_button()
            self.ui.textBrowser_2.append("*** 检测到缺陷，自动停机 ***\n")
            print("缺陷停机触发")

    def toggle_switch(self, event):
        self.defect_stop_on = not self.defect_stop_on
        self.update_switch()

    def toggle_run(self, event):
        self.running = not self.running
        self.update_run_button()

        if self.running:
            if not self.image_list:
                self.load_images()
            self.timer.start()
            self.ui.textBrowser_2.append("=== 开始实时检测 ===\n")
        else:
            self.timer.stop()
            self.ui.textBrowser_2.append("=== 停止检测 ===\n")

    def update_run_button(self):
        if self.running:
            self.ui.label_13.setStyleSheet("font: 16pt \"宋体\"; background-color: #177DA9;")
            self.ui.label_13.setText("<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">运行中</span></p></body></html>")
        else:
            self.ui.label_13.setStyleSheet("font: 16pt \"宋体\"; background-color: rgb(70, 177, 225);")
            self.ui.label_13.setText("<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">开始/</span></p><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">停止</span></p></body></html>")

    def update_switch(self):
        if self.defect_stop_on:
            self.ui.label_18.setPixmap(QtGui.QPixmap(":/new/prefix1/images/switch_on.png"))
        else:
            self.ui.label_18.setPixmap(QtGui.QPixmap(":/new/prefix1/images/switch_off.png"))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = ZhijianWindow()
    w.show()
    sys.exit(app.exec_())
