import os
import sys
import random
import time
from datetime import datetime

# Фейковые ответы для команд
FAKE_RESPONSES = {
    'dir': """ Том в устройстве C имеет метку Windows
 Серийный номер тома: 1234-5678

 Содержимое папки C:\\Users\\User

29.06.2024  15:30    <DIR>          .
29.06.2024  15:30    <DIR>          ..
29.06.2024  14:20    <DIR>          Desktop
29.06.2024  13:45    <DIR>          Documents
29.06.2024  12:10    <DIR>          Downloads
29.06.2024  11:30             1,024 file1.txt
29.06.2024  10:15             2,048 file2.exe
29.06.2024  09:00             3,072 file3.dll
               3 файлов          6,144 байт
               5 папок  100,000,000 байт свободно""",
    
    'ipconfig': """
Настройка протокола IP для Windows

Адаптер Ethernet Ethernet0:

   DNS-суффикс подключения . . . . . : 
   IPv4-адрес. . . . . . . . . . . . : 192.168.1.100
   Маска подсети . . . . . . . . . . : 255.255.255.0
   Основной шлюз. . . . . . . . . . : 192.168.1.1

Адаптер Ethernet VirtualBox Host-Only Network:

   DNS-суффикс подключения . . . . . : 
   IPv4-адрес. . . . . . . . . . . . : 169.254.123.45
   Маска подсети . . . . . . . . . . : 255.255.0.0
   Основной шлюз. . . . . . . . . . :""",
    
    'ping': """
Обмен пакетами с 127.0.0.1 по 32 байт:
Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128
Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128
Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128
Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128

Статистика Ping для 127.0.0.1:
    Пакетов: отправлено = 4, получено = 4, потеряно = 0 (0% потерь),
Приблизительное время приема-передачи в мс:
    Минимальное = 0мсек, Максимальное = 0мсек, Среднее = 0мсек""",
    
    'echo': '',
    'cls': 'CLEAR',
    'exit': 'EXIT',
    'help': """
Доступные команды:
  dir         - Показать содержимое папки
  ipconfig    - Показать сетевые настройки
  ping        - Проверить сетевое соединение
  echo        - Вывести текст
  cls         - Очистить экран
  help        - Показать эту справку
  exit        - Выйти из программы
  time        - Показать текущее время
  date        - Показать текущую дату
  ver         - Показать версию ОС
  systeminfo  - Показать информацию о системе
  hostname    - Показать имя компьютера
  whoami      - Показать имя пользователя""",
    
    'time': datetime.now().strftime('Текущее время: %H:%M:%S'),
    'date': datetime.now().strftime('Текущая дата: %d.%m.%Y'),
    'ver': """
Microsoft Windows [Version 10.0.19045.3693]""",
    'systeminfo': """
Имя узла:               DESKTOP-ABC123
Имя ОС:                 Microsoft Windows 10 Pro
Версия ОС:              10.0.19045 Сборка 19045
Изготовитель ОС:        Microsoft Corporation
Время загрузки системы: 29.06.2024, 8:00:00
Изготовитель:           Dell Inc.
Модель:                 OptiPlex 7080
Тип системы:            x64-based PC
Процессор(ы):           1 установлено.
[01]: Intel64 Family 6 Model 165 Stepping 3 GenuineIntel ~3600 МГц
Всего памяти:           16,384 МБ
Доступно памяти:        8,192 МБ""",
    
    'hostname': 'DESKTOP-ABC123',
    'whoami': 'DESKTOP-ABC123\\User'
}

class FakeCMD:
    def __init__(self):
        self.current_dir = "C:\\Users\\User"
        self.history = []
        self.running = True
    
    def get_prompt(self):
        return f"Microsoft Windows [Version 10.0.19045.3693]\n(c) Корпорация Майкрософт (Microsoft Corporation). Все права защищены.\n\n{self.current_dir}>"
    
    def execute_command(self, command):
        if not command.strip():
            return ""
        
        self.history.append(command)
        parts = command.strip().split()
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        # Специальная обработка для echo
        if cmd == 'echo':
            return ' '.join(args) if args else ''
        
        # Специальная обработка для ping с аргументами
        if cmd == 'ping':
            if args:
                return self.fake_ping(args[0])
            return "Неверный синтаксис команды ping."
        
        # Поиск в словаре
        if cmd in FAKE_RESPONSES:
            response = FAKE_RESPONSES[cmd]
            if response == 'CLEAR':
                return None  # Сигнал для очистки экрана
            if response == 'EXIT':
                self.running = False
                return "Выход..."
            return response
        
        # Неизвестная команда
        return f"'{cmd}' не является внутренней или внешней командой, исполняемой программой или пакетным файлом."
    
    def fake_ping(self, target):
        if target == 'localhost' or target == '127.0.0.1':
            return FAKE_RESPONSES['ping']
        return f"""
Обмен пакетами с {target} по 32 байт:
Ответ от {target}: число байт=32 время={random.randint(1, 50)}мс TTL={random.randint(64, 128)}
Ответ от {target}: число байт=32 время={random.randint(1, 50)}мс TTL={random.randint(64, 128)}
Ответ от {target}: число байт=32 время={random.randint(1, 50)}мс TTL={random.randint(64, 128)}
Ответ от {target}: число байт=32 время={random.randint(1, 50)}мс TTL={random.randint(64, 128)}

Статистика Ping для {target}:
    Пакетов: отправлено = 4, получено = 4, потеряно = 0 (0% потерь),
Приблизительное время приема-передачи в мс:
    Минимальное = 1мсек, Максимальное = 50мсек, Среднее = 25мсек"""

def main():
    cmd = FakeCMD()
    print(cmd.get_prompt())
    
    while cmd.running:
        try:
            user_input = input()
            result = cmd.execute_command(user_input)
            
            if result is None:
                # Очистка экрана
                os.system('cls' if os.name == 'nt' else 'clear')
                print(cmd.get_prompt())
            elif result:
                print(result)
                if cmd.running:  # Не показывать приглашение после exit
                    print(cmd.get_prompt())
            else:
                # Пустой вывод (например, echo без аргументов)
                if cmd.running:
                    print(cmd.get_prompt())
                    
        except KeyboardInterrupt:
            print("\n^C")
            continue
        except EOFError:
            break
    
    print("До свидания!")

if __name__ == "__main__":
    main()
