
import cv2
import sys

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QColor, QFont, QPalette
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QWidget, QVBoxLayout, QSlider, QHBoxLayout



class SingleSliderColorPicker(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        # Основной layout
        layout = QVBoxLayout()
        layout.setSpacing(15)  # 15 пикселей между всеми виджетами
        layout.setContentsMargins(10, 0, 0, 0)  # Отступы: left, top, right, bottom
        layout2 = QHBoxLayout()

        # Создаем один слайдер (вертикальный)
        self.slider = QSlider(Qt.Vertical, self)
        self.slider.setRange(0, 100)
        self.slider.valueChanged.connect(self.update_color)

        self.saturation_slider = QSlider(Qt.Vertical, self)
        self.saturation_slider.setRange(0, 100)
        self.saturation_slider.setValue(70)
        self.saturation_slider.valueChanged.connect(self.update_color)

        self.value_slider = QSlider(Qt.Vertical, self)
        self.value_slider.setRange(0, 100)
        self.value_slider.setValue(90)
        self.value_slider.valueChanged.connect(self.update_color)

        self.c_grad = f"""
                    QSlider::groove:vertical {{
                        width: 20px;
                        background: qlineargradient(x1:0, y1:1, x2:0, y2:0,  /* Перевернутый градиент (снизу вверх) */
                    stop:0 red, stop:0.17 yellow, stop:0.33 lime, 
                    stop:0.5 cyan, stop:0.67 blue, stop:0.83 magenta, stop:1 red);
                        border-radius: 10px;
                    }}
                    QSlider::handle:vertical {{
                        background: white;
                        border: 1px solid #999;
                        height: 14px;
                        margin: 0 -5px;
                        border-radius: 7px;
                    }}
                """
        self.gray = f"""
                            QSlider::groove:vertical {{
                                width: 20px;
                                background: #cccccc;
                                border-radius: 10px;
                            }}
                            QSlider::handle:vertical {{
                                background: #f0f0f0;
                                border: 1px solid #999;
                                height: 14px;
                                margin: 0 -5px;
                                border-radius: 7px;
                            }}
                        """


        # Градиентный фон для вертикального слайдера
        # self.slider.setStyleSheet("""
        #     QSlider::groove:vertical {
        #         width: 35px;  /* Ширина дорожки */
        #         background: qlineargradient(x1:0, y1:1, x2:0, y2:0,  /* Перевернутый градиент (снизу вверх) */
        #             stop:0 red, stop:0.17 yellow, stop:0.33 lime,
        #             stop:0.5 cyan, stop:0.67 blue, stop:0.83 magenta, stop:1 red);
        #         border-radius: 20px;
        #     }
        #     QSlider::handle:vertical {
        #         background: white;
        #         border: 1px solid #FFFFFF;
        #         width: 20px;
        #         height: 10px;
        #         border-radius: 10px;
        #         margin: 0 -5px;  /* Смещение ручки */
        #     }
        # """)

        self.slider.setStyleSheet(self.c_grad)

        # Область для отображения выбранного цвета
        self.color_display = QtWidgets.QFrame(self)
        self.color_display.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.color_display.setAutoFillBackground(True)


        # self.color_display.setMaximumWidth(100)

        # Метка для отображения значения цвета
        self.color_label = QtWidgets.QLabel(self)
        self.color_label.setText("Цвет")
        self.color_label.setStyleSheet("color: #734A12;")
        self.color_label.setAlignment(Qt.AlignCenter)

        layout.addSpacing(20)  # 20 пикселей между виджетами
        layout.addWidget(self.color_display, QtCore.Qt.AlignCenter)
        layout.addSpacing(15)  # 20 пикселей между виджетами
        layout.addWidget(self.color_label)
        layout.addSpacing(20)  # 20 пикселей между виджетами

        layout2.addWidget(self.slider)
        layout2.addWidget(self.saturation_slider)
        layout2.addWidget(self.value_slider)
        layout2.addLayout(layout)

        # Добавляем элементы в layout
        # layout.addWidget(self.slider)


        self.setLayout(layout2)
        self.update_color()
        # self.update_slider_styles()

    def update_slider_styles(self, base_color: QColor):
        # Слайдер насыщенности (от серого к base_color) — вертикально
        self.s_grad = f"""
            QSlider::groove:vertical {{
                width: 20px;
                background: qlineargradient(x1:0, y1:1, x2:0, y2:0,
                    stop:0 rgb(128,128,128), stop:1 {base_color.name()});
                border-radius: 10px;
            }}
            QSlider::handle:vertical {{
                background: white;
                border: 1px solid #999;
                height: 14px;
                margin: 0 -5px;
                border-radius: 7px;
            }}
        """
        self.saturation_slider.setStyleSheet(self.s_grad)

        # Слайдер яркости (от чёрного к base_color) — вертикально
        self.v_grad = f"""
            QSlider::groove:vertical {{
                width: 20px;
                background: qlineargradient(x1:0, y1:1, x2:0, y2:0,
                    stop:0 black, stop:1 {base_color.name()});
                border-radius: 10px;
            }}
            QSlider::handle:vertical {{
                background: white;
                border: 1px solid #999;
                height: 14px;
                margin: 0 -5px;
                border-radius: 7px;
            }}
        """
        self.value_slider.setStyleSheet(self.v_grad)

    def update_color(self):
        value = self.slider.value()

        # Преобразуем позицию слайдера в цвет (0-100% спектра)
        hue = self.slider.value() / 100.0
        sat = self.saturation_slider.value() / 100.0
        val = self.value_slider.value() / 100.0

        color = QColor()
        color.setHsvF(hue, sat, val)

        h = int(hue * 179)
        s = int(sat * 255)
        v = int(val * 255)
        hue_range = 15  # диапазон оттенков (можно подстроить)
        sat_range = 40
        val_range = 40

        self.lower = np.array([
            max(0, h - hue_range),
            max(0, s - sat_range),
            max(0, v - val_range)
        ])
        self.upper = np.array([
            min(179, h + hue_range),
            min(255, s + sat_range),
            min(255, v + val_range)
        ])

        # Устанавливаем цвет для отображения
        palette = self.color_display.palette()
        palette.setColor(QPalette.Window, color)
        self.color_display.setPalette(palette)

        # Отображаем значения цвета
        self.color_label.setText(
            f"HSV({int(hue * 360)}°, {int(sat * 100)}%, {int(val * 100)}%)\n"
            f"RGB({color.red()}, {color.green()}, {color.blue()})\n"
            f"HEX: {color.name()}"
        )

        self.update_slider_styles(color)

    # В классе SingleSliderColorPicker добавьте метод:
    def set_enabled(self, enabled):
        """Включает/отключает слайдер"""
        self.slider.setEnabled(enabled)

        # Опционально: изменяем стиль для визуального отключения
        if enabled:
            self.slider.setStyleSheet(self.c_grad)
            self.saturation_slider.setStyleSheet(self.s_grad)
            self.value_slider.setStyleSheet(self.v_grad)
            self.update_color()

        else:
            self.slider.setStyleSheet(self.gray)
            self.saturation_slider.setStyleSheet(self.gray)
            self.value_slider.setStyleSheet(self.gray)
            value = "#d1d1d1"
            color = QColor(value)

            palette = self.color_display.palette()
            palette.setColor(QPalette.Window, color)
            self.color_display.setPalette(palette)