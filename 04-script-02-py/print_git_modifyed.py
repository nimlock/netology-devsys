#!/usr/bin/env python3

import os

REPO_PATH = '~/study/netology.devsys/test42'
HOME_FULLPATH = os.popen('echo -n $HOME').read()

if REPO_PATH.find('~', 1, 1):
    REPO_FULLPATH = REPO_PATH.replace("~", HOME_FULLPATH, 1)
else:
    REPO_FULLPATH = REPO_PATH

bash_command = [f"cd {REPO_FULLPATH}", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
for result in result_os.split('\n'):
    if result.find('новый файл') != -1:
        prepare_result = result.replace('\tновый файл:   ', '')
        print(REPO_FULLPATH + "/" + prepare_result)