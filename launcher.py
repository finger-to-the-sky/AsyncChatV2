import subprocess

import subprocess

process = []

while True:
    action = input('Выберите действие: q - выход , s - запустить сервер c - запустить клиентов, '
                   'x - закрыть всех клиентов:')
    if action == 'q':
        break
    elif action == 's':
        # Запускаем сервер!
        serv = subprocess.Popen('cmd /K python \"server.py\"', creationflags=subprocess.CREATE_NEW_CONSOLE)
        # Запускаем клиентов:
    elif action == 'c':
        clients_count = int(input('Введите количество тестовых клиентов для запуска: '))
        for i in range(clients_count):
            process.append(
                subprocess.Popen(f'python client.py -n test{i + 1}', creationflags=subprocess.CREATE_NEW_CONSOLE))

    elif action == 'x':
        while process:
            process.pop().kill()

