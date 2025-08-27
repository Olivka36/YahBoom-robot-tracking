# YahBoom-robot-tracking
Object tracking by robot based on YahBoom using segmentation method

## Отслеживание объектов мобильным колесным роботом на базе Raspberry Pi 4 и платы расширения YahBoom

В качестве вычислительного модуля используется микроконтроллер Raspberry Pi 4 Model B. Дополнительно применяется плата расширения YahBoom, обеспечивающая подключение моторов типа TT и камеры. Для реализации функции отслеживания объектов используется видеокамера Logitech, подключаемая к Raspberry Pi через порт USB.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)  ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)  ![PyQt](https://img.shields.io/badge/PyQt-41CD52?style=for-the-badge&logo=qt&logoColor=white)  ![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white)  ![VNC](https://img.shields.io/badge/VNC-2C3E50?style=for-the-badge&logo=realvnc&logoColor=white)  ![PID Control](https://img.shields.io/badge/PID--Controller-FF6F00?style=for-the-badge&logo=mathworks&logoColor=white)  

### 🚀 Принцип работы:
:one: Raspberry Pi 4 поднимает камеру, задаёт FPS (10–15), размеры кадра, пороги HSV и параметры привода    
:two: OpenCV читает очередной кадр из видеопотока    
:three: кадр переводится из RGB (в OpenCV BGR) в HSV    
:four: формируется бинарная маска inRange(HSV, low, high)    
:five: выполняются морфологические операции (opening/closing), чтобы убрать шум и заделать разрывы    
:six: функцией findContours библиотеки OpenCV выделяются контуры всех объектов на маске    
:seven: контуры фильтруются по площади и берётся подходящий (крупнейший) контур    
:eight: по моментам контура вычисляется центр масс (cx, cy) - геометрическая «середина» найденного объекта    
:nine: считается ошибка по горизонтали dx = cx − W/2, где W - ширина кадра (отклонение центра объекта от центра кадра)    
:keycap_ten: ПИД-регулятор формирует корректирующий сигнал поворота, на основе которого вычисляются скорости колёс, которые отправляются на драйверы платы YahBoom    
:arrow_right: если контуров нет (цель потеряна) — скорости обнуляются (подается стоп)

Шаги 2–10 повторяются каждый кадр.

### 🖥 Интерфейс взаимодействия:
Для взаимодействия с системой создано приложение на PyQt. Визуализация упрощает контроль работы алгоритмов и настройку системы.    
Интерфейс отображает два окна: в первом показывается видеопоток с камеры с наложенной линией центра и маркером объекта, во втором — бинарная маска после сегментации.    
Пользователь может запускать и останавливать отслеживание, изменять диапазоны HSV и управлять базовой скоростью движения. 

Интерфейс поддерживает удалённое подключение через VNC.
