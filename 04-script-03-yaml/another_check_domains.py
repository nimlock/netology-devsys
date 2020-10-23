#!/usr/bin/env python3

import socket
import os
import json
import yaml

json_file = "check_domains_results.json"     # Файл, в котором хранятся результаты прошлого выполнения скрипта
yaml_file = "check_domains_results.yml"     # Файл, в котором хранятся результаты прошлого выполнения скрипта

# Определение самого свежего файла с прошлыми результатами - JSON или YAML
modification_time_dict = {}
for file in [json_file, yaml_file]:
    try:
        modification_time_dict[file] = os.path.getmtime(file)
    except FileNotFoundError:
        print(f'[WARN] Previous results file {file} not found!')
        continue

# Если получили данные о времени изменения хоть одного фала, то выберем самый свежий файл из словаря
if len(modification_time_dict.keys()) >= 1:
    latest_file = max(modification_time_dict, key=modification_time_dict.get)
else:
    latest_file = ''

# Формирование словаря прошлых результатов
if latest_file == json_file:
    with open(json_file, 'r') as f:
        previous_dict = json.load(f)
elif latest_file == yaml_file:
    with open(yaml_file, 'r') as f:
        previous_dict = yaml.safe_load(f)
else:
    previous_dict = {}

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
        oldIP = previous_dict[key]
    except KeyError:
        print(f'[WARN] Previous IP for {key} not found!')
        continue

    # Сравним старый и текущий адрес ресурса
    if newIP != oldIP:
        print('[ERROR]', key, 'IP mismatch:', 'previous -', oldIP, 'now -', newIP)

# Записываем результаты в файл
with open(json_file, 'w') as f_json:
    json.dump(current_ip_dict, f_json, indent='  ')

with open(yaml_file, 'w') as f_yaml:
    yaml.dump(current_ip_dict, f_yaml)

# Для каждого домена также создадим по своему файлу каждого формата
for domain in current_ip_dict.keys():
    content = {domain: current_ip_dict[domain]}

    filename = domain + '.json'
    with open(filename, 'w') as f:
        json.dump(content, f, indent='  ')

    filename = domain + '.yml'
    with open(filename, 'w') as f:
        yaml.dump(content, f)