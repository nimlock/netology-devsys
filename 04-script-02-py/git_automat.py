#!/usr/bin/env python3

from github import Github
from git import Repo
import sys
import os


# --- Настраиваемая конфигурация ---

# Для работы с GitHub определим удалённый репозиторий
g = Github('user', 'password')     # Логин/пароль (два аргумента), либо ключ доступа (один аргумент)
GitHub_repo_name = 'user/repo'     # Название репозитория

# Скрипт по условию уже находится в локальном репозитории
repo_root_path = os.getcwd()

# Определяем локальный репозиторий
Local_repo = Repo(repo_root_path)
git = Local_repo.git

# - Умолчания для используемых функций -

current_branch = str(Local_repo.active_branch)

push_target_branch = current_branch
push_target_remote = 'origin'   # В какой remote делать push

PR_source_branch = current_branch
PR_target_branch = 'master'     # В какую ветку делать PR


# --- Блок функций ---

# Функция принимает имя новой ветки и пытается её создать;
# после - делается переключение на эту ветку
def switch_branch(branch_name):
    try:
        git.branch(branch_name)      # Создание новой локальной ветки
    except Exception:
        print('[WARN] Probably, branch already exist.')
    git.checkout(branch_name)       # Переключение на указанную ветку

# Функция делает commit всех staged изменений, затем push
def publish_workdir(branch, commit_msg):
    try:
        git.commit(m=commit_msg)
        git.push(u=[push_target_remote, branch])
    except Exception:
        print('[ERROR] Some problems with commit or push, check are staged files there')
        exit(1)

# Функция по API создаёт в GitHub ПР переданной ветки в master
# с заданным комментарием (не может быть пустым)
def make_PR_at_GitHub(src_branch, PR_msg):
    assert not PR_msg == ''                     # Проверка, что PR_msg не пустая строка
    assert not src_branch == PR_target_branch   # Проверка, что исходная и целевая ветки имеют разные имена

    GitHub_repo = g.get_repo(GitHub_repo_name)  # Создание объекта для работы с GitHub

    body = 'Empty body message'
    PR = GitHub_repo.create_pull(title=PR_msg, body=body, head=src_branch, base=PR_target_branch)
    try:
        PR
    except Exception:
        print(f'[ERROR] Some problems with PR of branch {src_branch} to {PR_target_branch}')
        exit(1)


# --- Ветвление поведения скрипта, исполнительная часть ---

actions_dict = {
    1: 'i_want_branch',
    2: 'commit_push',
    3: 'make_pr',
    4: 'combo'
}

action = sys.argv[1]
assert len(sys.argv) >= 3   # При любом сценарии должно быть минимум два аргумента

# --- i_want_branch ---
if action == actions_dict[1]:
    target_branch = sys.argv[2]

    switch_branch(target_branch)

# --- commit_push ---
elif action == actions_dict[2]:
    assert len(sys.argv) in [3, 4]  # Защита от "не тех кавычек" при введении сообщения коммита
    if len(sys.argv) == 3:          # Задан один аргумент: сообщение для коммита
        commit_msg = sys.argv[2]
    elif len(sys.argv) == 4:        # Заданы два аргумента: целевая ветвь и сообщение для коммита
        push_target_branch = sys.argv[2]
        commit_msg = sys.argv[3]
    else:
        print('[ERROR] Something go really wrong!')
        exit(1)

    switch_branch(push_target_branch)
    publish_workdir(push_target_branch, commit_msg)

# --- make_pr ---
elif action == actions_dict[3]:
    assert len(sys.argv) in [3, 4]  # Защита от "не тех кавычек" при введении сообщения PR
    if len(sys.argv) == 3:          # Задан один аргумент: сообщение для PR
        PR_msg = sys.argv[2]
    elif len(sys.argv) == 4:        # Заданы два аргумента: исходная ветвь и сообщение для PR
        PR_source_branch = sys.argv[2]
        PR_msg = sys.argv[3]
    else:
        print('[ERROR] Something go really wrong!')
        exit(1)

    make_PR_at_GitHub(PR_source_branch, PR_msg)

# --- combo ---
elif action == actions_dict[4]:
    assert len(sys.argv) == 5   # Должны быть определены: ветка, сообщения коммита и PR
    target_branch = sys.argv[2]
    push_target_branch = target_branch
    PR_source_branch = target_branch
    commit_msg = sys.argv[3]
    PR_msg = sys.argv[4]

    switch_branch(target_branch)
    publish_workdir(push_target_branch, commit_msg)
    make_PR_at_GitHub(PR_source_branch, PR_msg)

else:
    print(f'[ERROR] Sorry, < {action} > is wrong action!')
