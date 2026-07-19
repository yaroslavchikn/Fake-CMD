import sys
import os
import random
import datetime
import time
import platform
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import psutil
import cpuinfo
import math

class FakeCMD(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("C:\\Windows\\System32\\cmd.exe")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(700, 500)
        
        # Создаем иконку программно (как у CMD)
        self.setWindowIcon(self.create_icon())
        
        # Устанавливаем темный стиль как в CMD
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
            }
            QTextEdit {
                background-color: #000000;
                color: #ffffff;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
                border: none;
                padding: 10px;
            }
            QLineEdit {
                background-color: #000000;
                color: #ffffff;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
                border: none;
                padding: 5px 10px;
            }
            QScrollBar:vertical {
                background-color: #000000;
                width: 15px;
            }
            QScrollBar::handle:vertical {
                background-color: #444444;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Основной виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Верхняя панель (как в CMD)
        title_bar = QWidget()
        title_bar.setStyleSheet("background-color: #1a1a1a; border-bottom: 1px solid #333333;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(10, 5, 10, 5)
        
        # Заголовок
        title_label = QLabel("CMD - Выполняется от имени пользователя")
        title_label.setStyleSheet("color: #ffffff; font-size: 12px;")
        title_layout.addWidget(title_label)
        
        # Кнопки управления
        btn_style = """
            QPushButton {
                background-color: transparent;
                color: #cccccc;
                border: none;
                font-size: 16px;
                padding: 5px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #333333;
            }
            QPushButton#close:hover {
                background-color: #ff0000;
                color: white;
            }
        """
        
        self.min_btn = QPushButton("─")
        self.min_btn.setStyleSheet(btn_style)
        self.min_btn.clicked.connect(self.showMinimized)
        title_layout.addWidget(self.min_btn)
        
        self.max_btn = QPushButton("☐")
        self.max_btn.setStyleSheet(btn_style)
        self.max_btn.clicked.connect(self.toggle_maximize)
        title_layout.addWidget(self.max_btn)
        
        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("close")
        self.close_btn.setStyleSheet(btn_style)
        self.close_btn.clicked.connect(self.close)
        title_layout.addWidget(self.close_btn)
        
        layout.addWidget(title_bar)
        
        # Текстовое поле для вывода
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)
        
        # Строка ввода
        input_widget = QWidget()
        input_widget.setStyleSheet("background-color: #000000; border-top: 1px solid #333333;")
        input_layout = QHBoxLayout(input_widget)
        input_layout.setContentsMargins(10, 5, 10, 5)
        
        self.prompt_label = QLabel("C:\\Users\\User>")
        self.prompt_label.setStyleSheet("color: #00ff00; font-family: 'Consolas', monospace; font-size: 14px;")
        input_layout.addWidget(self.prompt_label)
        
        self.input_line = QLineEdit()
        self.input_line.setStyleSheet("""
            QLineEdit {
                background-color: #000000;
                color: #ffffff;
                font-family: 'Consolas', monospace;
                font-size: 14px;
                border: none;
                padding: 5px;
            }
        """)
        self.input_line.returnPressed.connect(self.execute_command)
        input_layout.addWidget(self.input_line)
        
        layout.addWidget(input_widget)
        
        # История команд
        self.command_history = []
        self.history_index = -1
        
        # Системная информация
        self.username = os.getenv('USERNAME', 'User')
        self.computername = os.getenv('COMPUTERNAME', 'PC')
        self.current_path = f"C:\\Users\\{self.username}"
        
        # Обновляем промпт
        self.update_prompt()
        
        # Приветственное сообщение
        self.print_welcome()
        
        # Фокус на ввод
        self.input_line.setFocus()
        
        # Таймер для эффектов
        self.effect_timer = QTimer()
        self.effect_timer.timeout.connect(self.update_effects)
        self.effect_timer.start(100)
        
        # Переменные для эффектов
        self.effect_counter = 0
    
    def create_icon(self):
        """Создает иконку CMD"""
        size = 64
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Черный фон
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.drawRect(0, 0, size, size)
        
        # Белый прямоугольник (окно)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.setPen(QPen(QColor(200, 200, 200), 2))
        painter.drawRect(8, 8, 48, 48)
        
        # Заголовок окна
        painter.setBrush(QBrush(QColor(0, 0, 200)))
        painter.setPen(Qt.NoPen)
        painter.drawRect(8, 8, 48, 12)
        
        # Текст "CMD"
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(QFont("Consolas", 10, QFont.Bold))
        painter.drawText(12, 18, "CMD")
        
        # Маленький курсор внизу
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.drawRect(30, 40, 10, 2)
        painter.drawRect(30, 44, 10, 2)
        
        painter.end()
        
        return QIcon(pixmap)
    
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    
    def update_prompt(self):
        """Обновляет приглашение ввода"""
        self.prompt_label.setText(f"{self.current_path}>")
    
    def print_welcome(self):
        """Выводит приветственное сообщение"""
        welcome = f"""
Microsoft Windows [Version {platform.release()}]
(c) Microsoft Corporation. All rights reserved.

{self.current_path}>
"""
        self.output.append(welcome)
    
    def execute_command(self):
        """Выполняет введенную команду"""
        command = self.input_line.text().strip()
        if not command:
            self.input_line.clear()
            return
        
        # Добавляем в историю
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Выводим команду
        self.output.append(f"{self.current_path}>{command}")
        
        # Обрабатываем команду
        if command.lower() in ['exit', 'quit']:
            self.close()
            return
        
        result = self.fake_command(command)
        if result:
            self.output.append(result)
        
        # Обновляем промпт
        self.update_prompt()
        
        # Очищаем поле ввода
        self.input_line.clear()
        
        # Прокручиваем вниз
        self.output.verticalScrollBar().setValue(
            self.output.verticalScrollBar().maximum()
        )
    
    def fake_command(self, command):
        """Обрабатывает фейковые команды"""
        cmd_lower = command.lower().strip()
        
        # Список всех команд с реалистичным выводом
        
        # 1. HELP
        if cmd_lower == 'help':
            return self.help_command()
        
        # 2. DIR
        if cmd_lower.startswith('dir'):
            return self.dir_command()
        
        # 3. SYSTEMINFO
        if cmd_lower == 'systeminfo':
            return self.systeminfo_command()
        
        # 4. TASKLIST
        if cmd_lower == 'tasklist':
            return self.tasklist_command()
        
        # 5. IPCONFIG
        if cmd_lower == 'ipconfig':
            return self.ipconfig_command()
        
        # 6. PING
        if cmd_lower.startswith('ping'):
            return self.ping_command(command)
        
        # 7. TRACERT
        if cmd_lower.startswith('tracert'):
            return self.tracert_command(command)
        
        # 8. NETSTAT
        if cmd_lower == 'netstat':
            return self.netstat_command()
        
        # 9. WHOAMI
        if cmd_lower == 'whoami':
            return self.whoami_command()
        
        # 10. DATE
        if cmd_lower == 'date':
            return self.date_command()
        
        # 11. TIME
        if cmd_lower == 'time':
            return self.time_command()
        
        # 12. VER
        if cmd_lower == 'ver':
            return self.ver_command()
        
        # 13. VOL
        if cmd_lower == 'vol':
            return self.vol_command()
        
        # 14. PATH
        if cmd_lower == 'path':
            return self.path_command()
        
        # 15. SET
        if cmd_lower == 'set':
            return self.set_command()
        
        # 16. CD
        if cmd_lower.startswith('cd '):
            return self.cd_command(command)
        
        # 17. CLS
        if cmd_lower == 'cls':
            self.output.clear()
            return None
        
        # 18. COLOR
        if cmd_lower.startswith('color'):
            return self.color_command(command)
        
        # 19. TITLE
        if cmd_lower.startswith('title'):
            return self.title_command(command)
        
        # 20. TREE
        if cmd_lower == 'tree':
            return self.tree_command()
        
        # 21. MEM
        if cmd_lower == 'mem':
            return self.mem_command()
        
        # 22. DRIVERQUERY
        if cmd_lower == 'driverquery':
            return self.driverquery_command()
        
        # 23. SC QUERY
        if cmd_lower.startswith('sc query'):
            return self.sc_query_command()
        
        # 24. REG QUERY
        if cmd_lower.startswith('reg query'):
            return self.reg_query_command()
        
        # 25. WMIC
        if cmd_lower.startswith('wmic'):
            return self.wmic_command(command)
        
        # 26. CHKDSK
        if cmd_lower.startswith('chkdsk'):
            return self.chkdsk_command()
        
        # 27. FORMAT (опасно!)
        if cmd_lower.startswith('format'):
            return "Недостаточно прав для выполнения операции."
        
        # 28. DEL (опасно!)
        if cmd_lower.startswith('del'):
            return "Недостаточно прав для выполнения операции."
        
        # 29. MKDIR
        if cmd_lower.startswith('mkdir'):
            return "Каталог создан успешно."
        
        # 30. RMDIR
        if cmd_lower.startswith('rmdir'):
            return "Каталог удален успешно."
        
        # 31. COPY
        if cmd_lower.startswith('copy'):
            return "Скопировано: 1 файл(ов)."
        
        # 32. MOVE
        if cmd_lower.startswith('move'):
            return "Перемещено: 1 файл(ов)."
        
        # 33. REN
        if cmd_lower.startswith('ren'):
            return "Переименовано: 1 файл(ов)."
        
        # 34. TYPE
        if cmd_lower.startswith('type'):
            return self.type_command()
        
        # 35. FIND
        if cmd_lower.startswith('find'):
            return "Текст найден."
        
        # 36. SORT
        if cmd_lower == 'sort':
            return self.sort_command()
        
        # 37. MORE
        if cmd_lower == 'more':
            return "--- Более ---"
        
        # 38. ATTRIB
        if cmd_lower.startswith('attrib'):
            return "Атрибуты файлов изменены."
        
        # 39. ASSOC
        if cmd_lower == 'assoc':
            return self.assoc_command()
        
        # 40. FTYPE
        if cmd_lower == 'ftype':
            return self.ftype_command()
        
        # 41. PROMPT
        if cmd_lower.startswith('prompt'):
            return "Приглашение изменено."
        
        # 42. START
        if cmd_lower.startswith('start'):
            return "Приложение запущено."
        
        # 43. SHUTDOWN (опасно!)
        if cmd_lower.startswith('shutdown'):
            return "Выключение отменено."
        
        # 44. TASKKILL
        if cmd_lower.startswith('taskkill'):
            return "Процесс завершен успешно."
        
        # 45. NBTSTAT
        if cmd_lower.startswith('nbtstat'):
            return self.nbtstat_command()
        
        # 46. ROUTE
        if cmd_lower.startswith('route'):
            return self.route_command()
        
        # 47. ARP
        if cmd_lower.startswith('arp'):
            return self.arp_command()
        
        # 48. NSLOOKUP
        if cmd_lower.startswith('nslookup'):
            return self.nslookup_command(command)
        
        # 49. HOSTNAME
        if cmd_lower == 'hostname':
            return self.hostname_command()
        
        # 50. GETMAC
        if cmd_lower == 'getmac':
            return self.getmac_command()
        
        # Неизвестная команда
        return f"'{command}' не является внутренней или внешней командой, исполняемой программой или пакетным файлом."
    
    # ========== РЕАЛИЗАЦИЯ КОМАНД ==========
    
    def help_command(self):
        return """
Поддерживаемые команды:
------------------------
ASSOC      - Вывод списка сопоставлений
ATTRIB     - Изменение атрибутов файлов
CD         - Смена текущего каталога
CHKDSK     - Проверка диска
CLS        - Очистка экрана
COLOR      - Изменение цвета консоли
COPY       - Копирование файлов
DATE       - Вывод даты
DEL        - Удаление файлов (заблокировано)
DIR        - Список файлов и папок
DRIVERQUERY - Список драйверов
EXIT       - Выход из программы
FIND       - Поиск текста в файлах
FORMAT     - Форматирование диска (заблокировано)
FTYPE      - Вывод типов файлов
GETMAC     - MAC-адрес
HELP       - Эта справка
HOSTNAME   - Имя компьютера
IPCONFIG   - Настройки сети
MKDIR      - Создание папки
MOVE       - Перемещение файлов
NETSTAT    - Статистика сети
NSLOOKUP   - DNS запросы
PATH       - Пути поиска
PING       - Проверка соединения
PROMPT     - Изменение приглашения
REG QUERY  - Запрос реестра (фейк)
REN        - Переименование
RMDIR      - Удаление папки
ROUTE      - Таблица маршрутизации
SC QUERY   - Список служб (фейк)
SET        - Переменные среды
SHUTDOWN   - Выключение (отменено)
SORT       - Сортировка текста
START      - Запуск приложения
SYSTEMINFO - Информация о системе
TASKKILL   - Завершение процесса (фейк)
TASKLIST   - Список процессов
TIME       - Вывод времени
TITLE      - Заголовок окна
TRACERT    - Трассировка маршрута
TREE       - Дерево каталогов
TYPE       - Вывод содержимого
VER        - Версия Windows
VOL        - Метка тома
WHOAMI     - Информация о пользователе
WMIC       - WMI запросы (фейк)

Введите HELP <команда> для детальной информации.
"""
    
    def dir_command(self):
        files = [
            "bootmgr",
            "pagefile.sys",
            "swapfile.sys",
            "Program Files",
            "Program Files (x86)",
            "Windows",
            "Users",
            "PerfLogs",
            "Documents and Settings"
        ]
        
        result = " Том в устройстве C имеет метку Windows\n"
        result += " Серийный номер тома: 1234-5678\n\n"
        result += " Содержимое папки " + self.current_path + "\n\n"
        
        for f in files:
            if '.' in f:
                result += f"  {f:20}  1,234,567 байт\n"
            else:
                result += f"  <DIR>      {f}\n"
        
        result += f"\nВсего: {len(files)} элементов"
        return result
    
    def systeminfo_command(self):
        return f"""
Имя узла:                    {self.computername}
Название ОС:                 Microsoft Windows {platform.release()}
Версия ОС:                   {platform.version}
Изготовитель ОС:             Microsoft Corporation
Конфигурация ОС:             Автономная рабочая станция
Тип сборки ОС:               Multiprocessor Free
Зарегистрированный владелец: {self.username}
Зарегистрированная компания: 
Тип системы:                 x64-based PC
Процессор(ы):                1 Установлено.
                             [{cpuinfo.get_cpu_info().get('brand_raw', 'Intel Core i7')}]
Версия BIOS:                 American Megatrends Inc. 1.2.3
Папка Windows:               C:\\Windows
Системная папка:             C:\\Windows\\system32
Загрузочный диск:            C:\\
Имя хоста:                   {self.computername}
Первичный DNS-суффикс:       domain.local
Тип узла:                    Гибридный
Включен IP-маршрутинг:       Нет
Включен прокси WINS:         Нет
Список DNS-суффиксов:        domain.local
    """
    
    def tasklist_command(self):
        processes = [
            ("System", "4", "88", "56,234 K"),
            ("svchost.exe", "1234", "12", "12,345 K"),
            ("explorer.exe", "2345", "5", "45,678 K"),
            ("chrome.exe", "3456", "25", "234,567 K"),
            ("firefox.exe", "4567", "18", "198,765 K"),
            ("cmd.exe", "5678", "2", "3,456 K"),
            ("notepad.exe", "6789", "1", "2,345 K"),
            ("winlogon.exe", "7890", "3", "8,901 K"),
            ("services.exe", "8901", "4", "6,789 K"),
            ("lsass.exe", "9012", "5", "9,012 K"),
        ]
        
        result = "Имя образа                      PID  Сессии  Память\n"
        result += "=========================  ======== ======== ============\n"
        
        for name, pid, session, mem in processes:
            result += f"{name:25} {pid:8} {session:8} {mem}\n"
        
        result += f"\nВсего процессов: {len(processes)}"
        return result
    
    def ipconfig_command(self):
        return """
Настройка протокола IP для Windows

Адаптер Ethernet Ethernet:

   DNS-суффикс подключения . . . . . : domain.local
   IPv4-адрес . . . . . . . . . . . . : 192.168.1.100
   Маска подсети . . . . . . . . . . : 255.255.255.0
   Основной шлюз . . . . . . . . . : 192.168.1.1

Адаптер Беспроводная локальная сеть:

   DNS-суффикс подключения . . . . . : domain.local
   IPv4-адрес . . . . . . . . . . . . : 192.168.1.101
   Маска подсети . . . . . . . . . . : 255.255.255.0
   Основной шлюз . . . . . . . . . : 192.168.1.1
    """
    
    def ping_command(self, command):
        parts = command.split()
        if len(parts) > 1:
            target = parts[1]
        else:
            target = "127.0.0.1"
        
        result = f"\nОбмен пакетами с {target} по 32 байт:\n"
        times = [random.randint(1, 50) for _ in range(4)]
        
        for i, t in enumerate(times, 1):
            result += f"Ответ от {target}: число байт=32 время={t}мс TTL=128\n"
            time.sleep(0.1)
        
        result += f"\nСтатистика Ping для {target}:\n"
        result += f"    Пакетов: отправлено = 4, получено = 4, потеряно = 0 (0% потерь)\n"
        result += f"Приблизительное время приема-передачи в мс:\n"
        result += f"    Минимальное = {min(times)}мсек, Максимальное = {max(times)}мсек, Среднее = {sum(times)//len(times)}мсек"
        return result
    
    def tracert_command(self, command):
        parts = command.split()
        if len(parts) > 1:
            target = parts[1]
        else:
            target = "google.com"
        
        result = f"\nТрассировка маршрута к {target}\n"
        result += "с максимальным числом прыжков 30:\n\n"
        
        hops = [
            ("1", "192.168.1.1", "1", "1", "1"),
            ("2", "10.0.0.1", "5", "4", "5"),
            ("3", "172.16.0.1", "12", "11", "12"),
            ("4", "89.123.45.67", "25", "24", "26"),
            ("5", "94.123.45.67", "35", "34", "36"),
            ("6", "195.34.56.78", "42", "41", "43"),
            ("7", target, "48", "47", "49"),
        ]
        
        for hop, ip, t1, t2, t3 in hops:
            result += f"  {hop}    {ip:15}  {t1} ms  {t2} ms  {t3} ms\n"
        
        result += "\nТрассировка завершена."
        return result
    
    def netstat_command(self):
        connections = [
            ("TCP", "0.0.0.0:80", "0.0.0.0:0", "LISTENING"),
            ("TCP", "0.0.0.0:443", "0.0.0.0:0", "LISTENING"),
            ("TCP", "192.168.1.100:49152", "172.217.16.14:443", "ESTABLISHED"),
            ("TCP", "192.168.1.100:49153", "172.217.16.15:443", "ESTABLISHED"),
            ("TCP", "192.168.1.100:49154", "173.194.222.113:443", "ESTABLISHED"),
            ("UDP", "0.0.0.0:5353", "*:*", ""),
            ("UDP", "0.0.0.0:12345", "*:*", ""),
        ]
        
        result = "\nАктивные подключения\n\n"
        result += "  Proto  Локальный адрес          Внешний адрес          Состояние\n"
        result += "  =====  ====================    ====================   ============\n"
        
        for proto, local, remote, state in connections:
            result += f"  {proto:4}  {local:20}  {remote:20}  {state}\n"
        
        return result
    
    def whoami_command(self):
        return f"{self.computername}\\{self.username}"
    
    def date_command(self):
        return f"Текущая дата: {datetime.datetime.now().strftime('%d.%m.%Y')}"
    
    def time_command(self):
        return f"Текущее время: {datetime.datetime.now().strftime('%H:%M:%S')}"
    
    def ver_command(self):
        return f"Microsoft Windows [Version {platform.release()}]"
    
    def vol_command(self):
        return "Том в устройстве C: имеет метку Windows\nСерийный номер тома: 1234-5678"
    
    def path_command(self):
        return "PATH=C:\\Windows\\system32;C:\\Windows;C:\\Windows\\System32\\Wbem"
    
    def set_command(self):
        variables = {
            "ALLUSERSPROFILE": "C:\\ProgramData",
            "COMPUTERNAME": self.computername,
            "NUMBER_OF_PROCESSORS": "8",
            "OS": "Windows_NT",
            "PATH": "C:\\Windows\\system32;C:\\Windows",
            "PROCESSOR_ARCHITECTURE": "AMD64",
            "PROCESSOR_IDENTIFIER": "Intel64 Family 6 Model 158",
            "PROCESSOR_LEVEL": "6",
            "PROCESSOR_REVISION": "9e09",
            "USERNAME": self.username,
            "WINDIR": "C:\\Windows"
        }
        
        result = ""
        for key, value in variables.items():
            result += f"{key}={value}\n"
        return result
    
    def cd_command(self, command):
        parts = command.split()
        if len(parts) > 1:
            path = parts[1]
            if path == "..":
                self.current_path = "\\".join(self.current_path.split("\\")[:-1])
                if not self.current_path:
                    self.current_path = "C:\\"
            elif path == "\\":
                self.current_path = "C:\\"
            elif path == "Users":
                self.current_path = f"C:\\Users\\{self.username}"
            else:
                self.current_path += f"\\{path}"
        self.update_prompt()
        return None
    
    def color_command(self, command):
        colors = {
            '0': 'черный', '1': 'синий', '2': 'зеленый',
            '3': 'голубой', '4': 'красный', '5': 'фиолетовый',
            '6': 'желтый', '7': 'белый', '8': 'серый',
            '9': 'светло-синий', 'A': 'светло-зеленый',
            'B': 'светло-голубой', 'C': 'светло-красный',
            'D': 'светло-фиолетовый', 'E': 'светло-желтый',
            'F': 'ярко-белый'
        }
        return "Цвет фона и текста изменен."
    
    def title_command(self, command):
        parts = command.split()
        if len(parts) > 1:
            new_title = " ".join(parts[1:])
            self.setWindowTitle(new_title)
            return "Заголовок окна изменен."
        return None
    
    def tree_command(self):
        return """
Структура папок:
C:.
├───Windows
│   ├───System32
│   │   ├───drivers
│   │   └───config
│   ├───Temp
│   └───Fonts
├───Program Files
│   ├───Common Files
│   └───Internet Explorer
├───Users
│   └───Public
│       └───Documents
└───PerfLogs
    """
    
    def mem_command(self):
        ram = psutil.virtual_memory()
        return f"""
Всего физической памяти:     {ram.total / (1024**3):.2f} GB
Доступно физической памяти: {ram.available / (1024**3):.2f} GB
Используется:              {ram.percent}%
Всего файла подкачки:      {ram.total / (1024**3):.2f} GB
Доступно файла подкачки:   {ram.available / (1024**3):.2f} GB
    """
    
    def driverquery_command(self):
        drivers = [
            ("1394ohci", "1394 OHCI Compliant Host Controller", "Kernel", "Running"),
            ("ACPI", "Microsoft ACPI Driver", "Kernel", "Running"),
            ("BTHUSB", "Bluetooth USB", "Kernel", "Running"),
            ("disk", "Disk Driver", "Kernel", "Running"),
            ("dxgkrnl", "DirectX Graphics Kernel", "Kernel", "Running"),
            ("usbhub", "USB Hub Driver", "Kernel", "Running"),
        ]
        
        result = "\nИмя модуля          Отображаемое имя                 Тип        Состояние\n"
        result += "===============     ===========================    ========   ===========\n"
        
        for name, display, typ, status in drivers:
            result += f"{name:18}  {display:25}  {typ:8}  {status}\n"
        
        return result
    
    def sc_query_command(self):
        services = [
            ("AeLookupSvc", "Application Experience", "Running"),
            ("ALG", "Application Layer Gateway", "Stopped"),
            ("AudioSrv", "Windows Audio", "Running"),
            ("BITS", "Background Intelligent Transfer", "Running"),
            ("Browser", "Computer Browser", "Stopped"),
            ("CryptSvc", "Cryptographic Services", "Running"),
            ("DcomLaunch", "DCOM Server Process Launcher", "Running"),
            ("Dhcp", "DHCP Client", "Running"),
            ("Dnscache", "DNS Client", "Running"),
            ("EventLog", "Windows Event Log", "Running"),
        ]
        
        result = "\nSERVICE_NAME: \n"
        for name, display, status in services:
            result += f"\nSERVICE_NAME: {name}\n"
            result += f"DISPLAY_NAME: {display}\n"
            result += f"STATE       : {status}\n"
        return result
    
    def reg_query_command(self):
        return """
! REG.EXE VERSION 3.0

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion
    ProductName    REG_SZ    Microsoft Windows 10 Pro
    CurrentVersion    REG_SZ    6.3
    CurrentBuild    REG_SZ    19045
    RegisteredOwner    REG_SZ    User
    RegisteredOrganization    REG_SZ    
    """
    
    def wmic_command(self, command):
        if "cpu" in command.lower():
            return """
CPU: Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz
Current Clock Speed: 2600 MHz
Max Clock Speed: 5000 MHz
Cores: 6
Logical Processors: 12
"""
        elif "memory" in command.lower():
            ram = psutil.virtual_memory()
            return f"""
Total Physical Memory: {ram.total / (1024**3):.2f} GB
Available Physical Memory: {ram.available / (1024**3):.2f} GB
Total Virtual Memory: {ram.total / (1024**3):.2f} GB
Available Virtual Memory: {ram.available / (1024**3):.2f} GB
"""
        elif "disk" in command.lower():
            return """
Disk: C: (System)
Size: 500 GB
Free Space: 300 GB
File System: NTFS
"""
        else:
            return "WMIC запрос выполнен."
    
    def chkdsk_command(self):
        return """
Тип файловой системы: NTFS.
Метка тома: Windows.

Проверка файлов:
   Фаза 1: Проверка базовой структуры файловой системы...
   Фаза 2: Проверка связей имен файлов...
   Фаза 3: Проверка дескрипторов безопасности...

Ошибок не найдено.
Общее пространство на диске: 500 123 456 789 байт.
    """
    
    def type_command(self):
        return "Это содержимое текстового файла.\nСтрока 1\nСтрока 2\nСтрока 3"
    
    def sort_command(self):
        return """
A
B
C
D
E
"""
    
    def assoc_command(self):
        return """
.txt=textfile
.docx=Word.Document.12
.xlsx=Excel.Sheet.12
.pptx=PowerPoint.Show.12
.jpg=JPEG Image
.png=PNG Image
.exe=exefile
"""
    
    def ftype_command(self):
        return """
textfile="C:\Windows\System32\NOTEPAD.EXE" %1
Word.Document.12="C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE" %1
Excel.Sheet.12="C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE" %1
"""
    
    def nbtstat_command(self):
        return """
Локальное имя:
   Имя:             {self.computername}
   Регистрация:     Уникальная
   IP-адрес:        192.168.1.100
   Транспорт:       NetBT
   Состояние:       Зарегистрировано
    """
    
    def route_command(self):
        return """
Список интерфейсов
  0x1 .......................... MS TCP Loopback interface
  0x2 ...00 15 5d 1a 2b 3c ...... Intel(R) PRO/1000 MT Network Connection

Активные маршруты:
Сетевой адрес          Маска сети       Адрес шлюза       Интерфейс
0.0.0.0               0.0.0.0          192.168.1.1       192.168.1.100
192.168.1.0           255.255.255.0    0.0.0.0           192.168.1.100
"""
    
    def arp_command(self):
        return """
Интерфейс: 192.168.1.100 --- 0x2
  Интернет-адрес           Физический адрес      Тип
  192.168.1.1             aa-bb-cc-dd-ee-ff     динамический
  192.168.1.101           11-22-33-44-55-66     динамический
  192.168.1.102           77-88-99-aa-bb-cc     динамический
"""
    
    def nslookup_command(self, command):
        parts = command.split()
        if len(parts) > 1:
            domain = parts[1]
        else:
            domain = "google.com"
        
        return f"""
Сервер:  {self.computername}.domain.local
Address:  192.168.1.1

Имя:    {domain}
Addresses:  173.194.222.113, 173.194.222.114, 173.194.222.115
    """
    
    def hostname_command(self):
        return self.computername
    
    def getmac_command(self):
        return """
Физический адрес    Транспорт
=================  ==============================
AA-BB-CC-DD-EE-FF  \Device\Tcpip_{12345678-1234-1234-1234-123456789012}
    """
    
    def update_effects(self):
        """Обновляет эффекты (мигание курсора и т.д.)"""
        self.effect_counter += 1
        
        # Меняем цвет текста каждые 5 секунд для эффекта CMD
        if self.effect_counter % 50 == 0:
            colors = ['#00ff00', '#00ffff', '#ffff00', '#ff00ff']
            # Самый минимальный эффект, чтобы не раздражать
    
    def keyPressEvent(self, event):
        """Обработка клавиш для истории команд"""
        if event.key() == Qt.Key_Up:
            if self.history_index > 0:
                self.history_index -= 1
                if self.history_index < len(self.command_history):
                    self.input_line.setText(self.command_history[self.history_index])
        elif event.key() == Qt.Key_Down:
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                self.input_line.setText(self.command_history[self.history_index])
            else:
                self.history_index = len(self.command_history)
                self.input_line.clear()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = FakeCMD()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
