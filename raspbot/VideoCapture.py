import cv2
import sys
import YB_Pcb_Car  #Import Yahboom car library
import time

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QColor, QFont, QPalette
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QWidget, QVBoxLayout, QSlider, QHBoxLayout

from SingleSliderColorPicker import SingleSliderColorPicker

left = 0 
right = 0

class VideoCapture(QtCore.QObject):
    """Класс для захвата видео с камеры"""
    new_frame = QtCore.pyqtSignal(QtGui.QImage)
    object_coords = QtCore.pyqtSignal(int, int)  # Сигнал с координатами объекта
    binary_frame = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, picker: SingleSliderColorPicker = None):
        super().__init__()
        self.camera = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(15)  # ~30 FPS
        self.picker = picker
        self.speed_left = 0
        self.speed_right = 0
        self.Car = YB_Pcb_Car.YB_Pcb_Car()

    def update_frame(self):
        self.iSee = False
        ret, self.frame = self.camera.read()
        if ret:
            frame = cv2.flip(self.frame, 1)
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.new_frame.emit(qt_image)
            self.process_camera(frame, self.picker.lower, self.picker.upper)
        else:
            # Создаем белое изображение с текстом
            w, h = 640, 480  # Размеры по умолчанию
            white_image = QtGui.QImage(w, h, QtGui.QImage.Format_RGB888)
            white_image.fill(QtGui.QColor(255, 255, 255))  # Белый фон

            # Настраиваем painter для рисования текста
            painter = QtGui.QPainter(white_image)
            painter.setPen(QtGui.QColor(0, 0, 0))  # Черный текст
            font = QtGui.QFont()
            font.setPointSize(20)
            painter.setFont(font)

            # Вычисляем позицию текста по центру
            text = "Ожидается подключение"
            text_rect = painter.fontMetrics().boundingRect(text)
            x = (w - text_rect.width()) // 2
            y = (h + text_rect.height()) // 2

            painter.drawText(x, y, text)
            painter.end()

            self.new_frame.emit(white_image)

    def process_camera(self, frame, lower, upper):
        global left, right
        height, width = frame.shape[0:2]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        binary = cv2.inRange(hsv, lowerb=lower, upperb=upper)

        # Конвертируем бинарное изображение в RGB (для отображения)
        binary_rgb = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)

        # Создаем QImage из бинарного изображения
        h, w, ch = binary_rgb.shape
        bytes_per_line = ch * w
        binary_qt_image = QImage(binary_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

        self.binary_frame.emit(binary_qt_image)

        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cx, cy = -1, -1  # Инициализируем недопустимыми координатами

        if len(contours) > 0:
            maxc = max(contours, key=cv2.contourArea)
            moments = cv2.moments(maxc)

            if moments["m00"] > 20:
                cx = int(moments["m10"] / moments["m00"])
                cy = int(moments["m01"] / moments["m00"])

                self.iSee = True
                controlX = 4 * (cx - width / 4) / width  # находим отклонение найденного объекта от центра кадра и
                # нормализуем его (приводим к диапазону [-1; 1])
                if controlX < 0:
                    left = int(abs(60*controlX))
                    right = 60
                else:
                    right = int(abs(60*controlX))
                    left = 60
                print(left, right)
        if self.iSee:
            self.Car.Control_Car(left, right)
        else:
            self.Car.Car_Stop()

        # Отправляем координаты
        if cx >= 0 and cy >= 0:
            self.object_coords.emit(cx, cy)


    def __del__(self):
            """Деструктор - освобождаем ресурсы"""
            if hasattr(self, 'timer'):
                self.timer.stop()
            if hasattr(self, 'camera') and self.camera.isOpened():
                self.camera.release()
