import pickle
# import face_recognition

import cv2
import sys

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QColor, QFont, QPalette
# from PyQt5.QtGui.QIcon import pixmap
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QWidget, QVBoxLayout, QSlider, QHBoxLayout

from SingleSliderColorPicker import SingleSliderColorPicker
from VideoCapture import VideoCapture


class Shadow(QGraphicsDropShadowEffect):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBlurRadius(20)
        self.setXOffset(6)
        self.setYOffset(7)
        self.setColor(QColor("#79A0C1"))


class MW(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_camera()
        self.btn_face = True
        self.btn_object = True
        self.btn_line = True

    def setup_ui(self):
        self.setObjectName("MainWindow")
        self.resize(1260, 787)
        self.setMinimumSize(QtCore.QSize(1120, 700))
        self.setMaximumSize(QtCore.QSize(1680, 1050))

        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Настройка градиентного фона
        color1 = QtGui.QColor("#79A0C1")
        color2 = QtGui.QColor("#E2E7EB")
        gradient = QtGui.QLinearGradient(QtCore.QPointF(0, self.height()),
                                         QtCore.QPointF(self.width(), 0))
        gradient.setColorAt(0, color1)
        gradient.setColorAt(1, color2)

        palette = self.palette()
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(gradient))
        self.setPalette(palette)

        self.flag_line = True

        self.w = self.size().width()
        self.h = self.size().height()
        n = round((self.h + self.w) / 89)

        self.f1 = QtGui.QFont()  # под кнопку
        self.f1.setFamily("Courier New")
        self.f1.setPointSize(round(n * 0.78))
        self.f1.setBold(True)
        self.f1.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 2)

        self.f2 = QtGui.QFont()  # для ip ввода
        self.f2.setFamily("Courier New")
        self.f2.setPointSize(round(n * 0.82))
        self.f2.setBold(True)

        self.f3 = QtGui.QFont()  # для ip ввода
        self.f3.setFamily("Courier New")
        self.f3.setPointSize(round(n * 0.82))
        self.f3.setBold(True)

        shadow1 = QGraphicsDropShadowEffect()
        shadow1.setBlurRadius(15)
        shadow1.setXOffset(3)
        shadow1.setYOffset(3)
        shadow1.setColor(QColor("#734A12"))  # Semi-transparent black

        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(15)
        shadow2.setXOffset(3)
        shadow2.setYOffset(3)
        shadow2.setColor(QColor("#734A12"))  # Semi-transparent black

        shadow3 = QGraphicsDropShadowEffect()
        shadow3.setBlurRadius(15)
        shadow3.setXOffset(3)
        shadow3.setYOffset(3)
        shadow3.setColor(QColor("#734A12"))  # Semi-transparent black

        shadow4 = QGraphicsDropShadowEffect()
        shadow4.setBlurRadius(15)
        shadow4.setXOffset(3)
        shadow4.setYOffset(3)
        shadow4.setColor(QColor("#734A12"))  # Semi-transparent black

        # Создаем QLabel для отображения видео
        self.video_label = QtWidgets.QLabel(self.central_widget)
        self.video_label.setGeometry(QtCore.QRect(round(self.width() * 0.01), round(self.height() * 0.01), round(self.width() * 0.78), round(self.height() * 0.8)))
        # self.video_label.setStyleSheet("background-color: #ffffff;")
        #
        # Создаем QLabel для отображения видео
        self.video_bw = QtWidgets.QLabel(self.central_widget)
        self.video_bw.setGeometry(QtCore.QRect(round(self.width() * 0.01), round(self.height() * 0.81), round(self.width() * 0.78), round(self.height() * 0.8)))
        # self.video_label.setStyleSheet("background-color: #ffffff;")

        # ID
        self.inputId = QtWidgets.QLineEdit(self.central_widget)
        self.inputId.setPlaceholderText("Введите ID-адрес Raspberry PI")
        self.inputId.setGeometry(
            QtCore.QRect(round(self.w * 0.01), round(self.h * 0.84), round(self.w * 0.78), round(self.h * 0.1)))
        self.inputId.setStyleSheet(
            "background-color: #ffffff; color: rgba(0, 0, 0, 0.6); border-radius: 16px; padding-left: 20px;")
        self.inputId.setFont(self.f2)
        self.inputId.setGraphicsEffect(Shadow())
        self.inputId.textChanged.connect(self.change_text_color)

        self.button_connection = QtWidgets.QPushButton(self.central_widget)
        self.button_connection.setFont(self.f1)
        self.button_connection.setText("Подключиться")
        self.button_connection.setGeometry(
            QtCore.QRect(round(self.w * 0.6), round(self.h * 0.847), round(self.w * 0.17), round(self.h * 0.08)))
        self.button_connection.setStyleSheet(
            "background-color: #fde869; border-radius: 12px; text-align: center; color: #734A12; border-top: 1px solid #ffffff;")
        self.button_connection.setGraphicsEffect(shadow1)
        # self.button_connection.clicked.connect(self.change_flag)

        self.line = QtWidgets.QPushButton(self.central_widget)
        self.line.setFont(self.f1)
        self.line.setGeometry(
            QtCore.QRect(round(self.w * 0.8), round(self.h * 0.1), round(self.w * 0.18), round(self.h * 0.1)))
        self.line.setText("Движение по линии")
        self.line.setStyleSheet(
            "background-color: #fde869; border-radius: 12px; text-align: center; color: #734A12; border-top: 1px solid #ffffff;")
        self.line.setGraphicsEffect(shadow2)
        self.line.clicked.connect(self.buttonLine)
        # self.line.setWordWrap(True)

        self.object = QtWidgets.QPushButton(self.central_widget)
        self.object.setFont(self.f1)
        self.object.setGeometry(
            QtCore.QRect(round(self.w * 0.8), round(self.h * 0.22), round(self.w * 0.18), round(self.h * 0.1)))
        self.object.setText("Слежение за объектом")
        self.object.setStyleSheet(
            "background-color: #fde869; border-radius: 12px; text-align: center; color: #734A12; border-top: 1px solid #ffffff;")
        self.object.setGraphicsEffect(shadow3)
        self.object.clicked.connect(self.buttonObject)

        self.stack = QtWidgets.QStackedWidget(self.central_widget)
        self.stack.setGeometry( QtCore.QRect(round(self.w * 0.8), round(self.h * 0.35), round(self.w * 0.18), round(self.h * 0.6)))

        self.picker_field = QtWidgets.QWidget()
        layout = QVBoxLayout()

        self.picker = SingleSliderColorPicker()
        self.picker.color_label.setFont(self.f2)
        # # self.picker_field.setGeometry( QtCore.QRect(round(self.w * 0.8), round(self.h * 0.35), round(self.w * 0.18), round(self.h * 0.6)))
        # self.picker.slider.setGeometry(
        #     QtCore.QRect(round(self.w * 0.8), round(self.h * 0.35), round(self.w * 0.18), round(self.h * 0.2)))
        # self.picker.color_label.setGeometry(
        #     QtCore.QRect(round(self.w * 0.8), round(self.h * 0.56), round(self.w * 0.18), round(self.h * 0.2)))
        self.picker.color_display.setGeometry(
            QtCore.QRect(round(self.w * 0.8), round(self.h * 0.77), round(self.w * 0.18), round(self.h * 0.2)))

        layout.addWidget(self.picker)
        self.picker_field.setLayout(layout)
        self.stack.addWidget(self.picker_field)

        # self.face = QtWidgets.QPushButton(self.central_widget)
        # self.face.setFont(self.f1)
        # self.face.setGeometry(
        #     QtCore.QRect(round(self.w * 0.8), round(self.h * 0.8), round(self.w * 0.18), round(self.h * 0.1)))
        # self.face.setText("Слежение за человеком")
        # self.face.setStyleSheet(
        #     "background-color: #fde869; border-radius: 12px; text-align: center; color: #734A12; border-top: 1px solid #ffffff;")
        # self.face.setGraphicsEffect(shadow4)
        # self.face.clicked.connect(self.buttonFace)

    def setup_camera(self):
        self.capture = VideoCapture(self.picker)
        self.capture.new_frame.connect(self.display_video_stream)
        self.capture.object_coords.connect(self.update_crosshair)
        self.capture.binary_frame.connect(self.display_binary_frame)

    def update_crosshair(self, x, y):
        """Обновляем позицию перекрестия"""
        self.crosshair_x = x
        self.crosshair_y = y

    # def load_encodings(self, files):
    #     all_encodings = {"names": [], "encodings": []}
    #     for file in files:
    #         data = pickle.loads(open(file, "rb").read())
    #         name = data.get("name")
    #         encodings = data.get("encodings", [])
    #
    #         if name and encodings:  # Только если есть и имя, и кодировки
    #             all_encodings["names"].extend([name] * len(encodings))  # Добавляем имя столько раз, сколько кодировок
    #             all_encodings["encodings"].extend(encodings)
    #
    #     return all_encodings

    # def detect_person_in_video(self, image):
    #     encodings_data = self.load_encodings(["Alina_encodings.pickle", "Ayta_encodings.pickle", "Julia_encodings.pickle", "Emilia_encodings.pickle",
    #          "Arina_encodings.pickle", "Dima_encodings.pickle", "Arseny_encodings.pickle"])  # Загрузка всех кодировок
    #     frame = cv2.flip(image, 1)
    #     image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #
    #     # if len(frame.shape) == 2:  # Grayscale
    #     #     image = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    #     # elif frame.shape[2] == 4:  # RGBA → RGB
    #     #     image = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)            # Определение местоположений и кодировок лиц на кадре
    #     locations = face_recognition.face_locations(image)
    #     encodings = face_recognition.face_encodings(image, locations)
    #
    #     for face_encoding, face_location in zip(encodings, locations):
    #             # Сравниваем кодировку с каждой кодировкой из данных
    #         results = face_recognition.compare_faces(encodings_data["encodings"], face_encoding)
    #         match = "Unknown"  # Начальное значение имени, если совпадений не найдено
    #
    #         if True in results:
    #                 # Получаем индексы всех совпадений и извлекаем соответствующие имена
    #             matched_indices = [i for i, is_match in enumerate(results) if is_match]
    #             matched_names = [encodings_data["names"][i] for i in matched_indices]
    #             match = ", ".join(set(matched_names))  # Объединяем все найденные имена в одну строку
    #
    #             print(f"Match found: {match}")
    #         else:
    #             print("No match found.")
    #
    #             # Рисуем рамку и имя для каждого лица
    #         left_top = (face_location[3], face_location[0])
    #         right_bottom = (face_location[1], face_location[2])
    #         color = [0, 255, 0]
    #         cv2.rectangle(image, left_top, right_bottom, color, 4)
    #
    #             # Отображаем имя
    #         cv2.putText(
    #                 image,
    #                 match,
    #                 (face_location[3] + 10, face_location[2] + 15),
    #                 cv2.FONT_HERSHEY_SIMPLEX,
    #                 1,
    #                 (255, 255, 255),
    #                 2
    #         )
    #
    #     #     # Отображаем кадр с аннотациями
    #     # cv2.imshow("Video Face Recognition", image)
    #     rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Если image в BGR
    #     h, w, ch = rgb_image.shape
    #     bytes_per_line = ch * w
    #     qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
    #     self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    # def qimage_to_numpy(self, image: QImage) -> np.ndarray:
    #     image = image.convertToFormat(QImage.Format.Format_RGB888)
    #     width = image.width()
    #     height = image.height()
    #     ptr = image.bits()
    #     ptr.setsize(image.byteCount())
    #     arr = np.array(ptr).reshape((height, width, 3))
    #     return arr

    def display_video_stream(self, image):
        orig_width, orig_height = image.width(), image.height()
        pixmap = QPixmap.fromImage(image)

        label_width = self.video_label.width()
        label_height = self.video_label.height()

        scaled = image.scaled(
            label_width, label_height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        result = QPixmap(label_width, label_height)
        result.fill(Qt.transparent)
        painter = QtGui.QPainter(result)
        x_offset = (label_width - scaled.width()) // 2
        y_offset = (label_height - scaled.height()) // 2
        painter.drawPixmap(x_offset, y_offset, QPixmap.fromImage(scaled))

        if (self.btn_line == True or self.btn_object == True):
            pen = QtGui.QPen(QtGui.QColor(0, 255, 0))
            pen.setWidth(2)
            painter.setPen(pen)
        # Перекрестие по координатам объекта
            if hasattr(self, 'crosshair_x') and hasattr(self, 'crosshair_y'):
                scale_x = scaled.width() / image.width()
                scale_y = scaled.height() / image.height()

                x = int(x_offset + self.crosshair_x * scale_x)
                y = int(y_offset + self.crosshair_y * scale_y)

                painter.drawLine(x, y_offset, x, y_offset + scaled.height())
                painter.drawLine(x_offset, y, x_offset + scaled.width(), y)

            # 💡 ДОБАВЛЯЕМ: перекрестие по центру изображения
            center_x = x_offset + scaled.width() // 2
            center_y = y_offset + scaled.height() // 2

            pen.setColor(QtGui.QColor(255, 0, 0))  # Красный для отличия
            painter.setPen(pen)

            painter.drawLine(center_x, y_offset, center_x, y_offset + scaled.height())
            painter.drawLine(x_offset, center_y, x_offset + scaled.width(), center_y)

            self.video_label.setPixmap(result)
        # elif self.btn_face == True and (self.btn_line == False or self.btn_object == False):
        #     self.detect_person_in_video(self.capture.frame)

        painter.end()



    def display_binary_frame(self, binary_image):
        label_width = self.video_bw.width()
        label_height = self.video_bw.height()
        scaled = binary_image.scaled(
            label_width, label_height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        result = QPixmap(label_width, label_height)
        result.fill(Qt.transparent)  # Прозрачный фон

        # Центрируем изображение
        painter = QtGui.QPainter(result)
        x = (label_width - scaled.width()) // 2
        y = (label_height - scaled.height()) // 2
        painter.drawPixmap(x, y, QPixmap.fromImage(scaled))
        painter.end()
        self.video_bw.setPixmap(result)

    def buttonAccess(self):
        # if self.btn_face == True and self.btn_line == False and self.btn_object == False:
        #     self.face.setStyleSheet(
        #         "background-color: #fde869; border-radius: 12px; text-align: center; color: #734A12; border-top: 1px solid #ffffff;")
        #     # self.line.setEnabled(False)
        #     self.line.setStyleSheet("background-color: #BEB26B; border-radius: 12px; text-align: center; color: #666666; border-top: 1px solid #ffffff;")
        #     # self.object.setEnabled(False)
        #     self.object.setStyleSheet("background-color: #BEB26B; border-radius: 12px; text-align: center; color: #666666; border-top: 1px solid #ffffff;")
        #     self.picker.set_enabled(False)
        #     # detect_person_in_video()

        if self.btn_line == True and self.btn_object == False:
            self.line.setStyleSheet(
                "background-color: #fde869; border-radius: 12px; text-align: center; color: #563F20; border-top: 1px solid #ffffff;")
            # self.face.setEnabled(False)
            # self.face.setStyleSheet("background-color: #BEB26B; border-radius: 12px; text-align: center; color: #666666; border-top: 1px solid #ffffff;")
            # self.object.setEnabled(False)
            self.object.setStyleSheet("background-color: #BEB26B; border-radius: 12px; text-align: center; color: #666666; border-top: 1px solid #ffffff;")
            self.picker.set_enabled(True)

        elif self.btn_object == True and self.btn_line == False:
            self.object.setStyleSheet(
                "background-color: #fde869; border-radius: 12px; text-align: center; color: #734A12; border-top: 1px solid #ffffff;")
            # self.face.setEnabled(False)
            # self.face.setStyleSheet("background-color: #BEB26B; border-radius: 12px; text-align: center; color: #666666; border-top: 1px solid #ffffff;")
            # self.line.setEnabled(False)
            self.line.setStyleSheet("background-color: #BEB26B; border-radius: 12px; text-align: center; color: #666666; border-top: 1px solid #ffffff;")
            self.picker.set_enabled(True)

    def buttonLine(self):
        self.btn_line = True
        self.btn_object = False
        self.btn_face = False
        self.buttonAccess()

    def buttonObject(self):
        self.btn_line = False
        self.btn_object = True
        self.btn_face = False
        self.buttonAccess()
    #
    # def buttonFace(self):
    #     self.btn_line = False
    #     self.btn_object = False
    #     self.btn_face = True
    #     self.buttonAccess()

    def change_text_color(self):
        # Check if text is entered
        if self.inputId.text():
            # Change color when text is entered
            self.inputId.setStyleSheet(
                "background-color: #ffffff; color: 000000; border-radius: 16px; padding-left: 20px;")
            self.f2.setBold(True)
            self.inputId.setFont(self.f2)
        else:
            # Revert color when text is cleared
            self.inputId.setStyleSheet(
                "background-color: #ffffff; color: rgba(0, 0, 0, 0.6); border-radius: 16px; padding-left: 20px;")
            self.f2.setBold(True)
            self.inputId.setFont(self.f2)

    def closeEvent(self, event):
        self.capture.__del__()
        """Обработка закрытия окна - освобождаем ресурсы камеры"""
        # Останавливаем таймер захвата видео
        if hasattr(self, 'capture') and hasattr(self.capture, 'timer'):
            self.capture.timer.stop()

        # Освобождаем камеру
        if hasattr(self, 'capture') and hasattr(self.capture, 'camera') and self.capture.camera.isOpened():
            self.capture.camera.release()

        # Принимаем событие закрытия
        event.accept()

    def resizeEvent(self, event):
        # Вызывается при изменении размера окна
        self.w = self.size().width()
        self.h = self.size().height()
        n = (self.w + self.h)/89
        self.f1.setPointSize(round(n * 0.76))
        self.f2.setPointSize(round(n * 0.8))
        self.f3.setPointSize(round(n * 0.65))

        self.video_label.setGeometry(
            QtCore.QRect(round(self.width() * 0.01), round(self.height() * 0.005), round(self.width() * 0.68), round(self.height() * 0.86)))
        self.video_bw.setGeometry(
            QtCore.QRect(round(self.width() * 0.68), round(self.height() * 0.65), round(self.width() * 0.328), round(self.height() * 0.34)))

        self.inputId.setGeometry(
            QtCore.QRect(round(self.w * 0.01), round(self.h * 0.88), round(self.w * 0.68), round(self.h * 0.08)))
        self.inputId.setFont(self.f2)
        self.button_connection.setGeometry(
            QtCore.QRect(round(self.w * 0.55), round(self.h * 0.89), round(self.w * 0.13), round(self.h * 0.06)))
        self.button_connection.setFont(self.f1)

        # self.face.setGeometry(
        #     QtCore.QRect(round(self.w * 0.72), round(self.h * 0.03), round(self.w * 0.25), round(self.h * 0.08)))
        # self.face.setFont(self.f2)
        self.line.setGeometry(
            QtCore.QRect(round(self.w * 0.72), round(self.h * 0.13), round(self.w * 0.25), round(self.h * 0.08)))
        self.line.setFont(self.f2)
        self.object.setGeometry(
            QtCore.QRect(round(self.w * 0.72), round(self.h * 0.23), round(self.w * 0.25), round(self.h * 0.08)))
        self.object.setFont(self.f2)
        self.stop.setGeometry(
            QtCore.QRect(round(self.w * 0.72), round(self.h * 0.03), round(self.w * 0.25), round(self.h * 0.08)))
        self.stop.setFont(self.f2)

        self.picker.color_label.setFont(self.f3)

        self.stack.setGeometry(
            QtCore.QRect(round(self.w * 0.71), round(self.h * 0.32), round(self.w * 0.25), round(self.h * 0.33)))



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MW()
    window.show()
    sys.exit(app.exec_())