#!/usr/bin/env python3

import socket
import json

result_file = "check_domains_results.json"     # Файл, в котором хранятся результаты прошлого выполнения скрипта

# Формирование словаря прошлых результатов
try:                        # Пробуем считать прошлые результаты из файла
    with open(result_file, 'r') as f:
        previous_ip_dict = json.load(f)
except FileNotFoundError:
    print('[WARN] Previous results not found!')
    previous_ip_dict = {}

# Определяем словарь для свежих результатов работы скрипта
current_ip_dict = {}

# Кортеж из доменов для проверки
SERVICES_DOMAINS = (
    'drive.google.com',
    'mail.google.com',
    'google.com'
)

# Формирование словаря текущих адресов
for domain in SERVICES_DOMAINS:                 # Перебираем имеющиеся домены
    current_ip = socket.gethostbyname(domain)   # Записываем текущий ip в переменную
    current_ip_dict[domain] = current_ip        # Заполняем

# Сравнение старого и нового адреса
for key in current_ip_dict:
    newIP = current_ip_dict[key]
    print(' - '.join([key, newIP]))

    # Проверим что у нас есть старый адрес для этого домена, если нет - следующая итерация
    try:
        oldIP = previous_ip_dict[key]
    except KeyError:
        print(f'[WARN] Previous IP for {key} not found!')
        continue

    # Сравним старый и текущий адрес ресурса
    if newIP != oldIP:
        print('[ERROR]', key, 'IP mismatch:', 'previous -', oldIP, 'now -', newIP)

# Записываем результаты в файл
with open(result_file, 'w') as f:
    json.dump(current_ip_dict, f, indent='    ')
