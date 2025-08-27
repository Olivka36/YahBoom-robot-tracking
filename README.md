# YahBoom-robot-tracking
Object tracking by robot based on YahBoom using segmentation method

## Отслеживание объектов мобильным колесным роботом на базе Raspberry Pi 4 и платы расширения YahBoom

В качестве вычислительного модуля используется микроконтроллер Raspberry Pi 4 Model B, обладающий достаточной производительностью для обработки видеоданных и выполнения алгоритмов компьютерного зрения. Дополнительно применяется плата расширения YahBoom, обеспечивающая подключение периферийных устройств, включая моторы типа TT, модули управления питанием, а также датчики и камеры. Для реализации функции отслеживания объектов используется видеокамера Logitech, подключаемая к Raspberry Pi через порт USB.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)  ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)  ![PyQt](https://img.shields.io/badge/PyQt-41CD52?style=for-the-badge&logo=qt&logoColor=white)  ![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white)  ![VNC](https://img.shields.io/badge/VNC-2C3E50?style=for-the-badge&logo=realvnc&logoColor=white)  ![PID Control](https://img.shields.io/badge/PID--Controller-FF6F00?style=for-the-badge&logo=mathworks&logoColor=white)  

### 🚀 Функционал программы:
:arrow_right: Камера, подключённая к микрокомпьютеру, передаёт видеопоток
:arrow_right: Видеопоток в реальном времени обрабатывается с помощью библиотеки OpenCV
