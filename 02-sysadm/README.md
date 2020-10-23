# devops-netology-02
Репозиторий для заданий курса "DevOps и системное администрирование"  
Модуль 2. Системы управления версиями

### Студент: Иван Жиляев

# Домашнее задание к занятию «2.4. Инструменты Git»

При выполнении задания старался формализовать вывод команд, для более лёгкого применения в автоматизации. 

1. > Найдите полный хеш и комментарий коммита, хеш которого начинается на `aefea`.
   
   Команда:  
   
   __`git show aefea -s --format="Full hash is: %H%nAnd comment is: %s"`__  
   
   Вывод: 
   ```
   Full hash is: aefead2207ef7e2aa5dc81a34aedf0cad4c32545  
   And comment is: Update CHANGELOG.md
   ```

1. > Какому тегу соответствует коммит `85024d3`?

   Команда:  
   
   __`git show 85024d3 -s --format="%D"`__  
   
   Вывод: 
   ```
   tag: v0.12.23
   ```
   
1. > Сколько родителей у коммита `b8d720`? Напишите их хеши.

   Родителей двое.  
   Команда:  
   
   __`git show b8d720 -s --format="%P"`__  
   
   Вывод: 
   ```
   56cd7859e05c36c06b56d013b55a252d0bb7e158 9ea88f22fc6269854151c571162c5bcf958bee2b
   ```
   
1. > Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами  v0.12.23 и v0.12.24.

   Для изучения истории коммитов человеком достаточно задать аргумент `--format=oneline`, но для формализованного
   вывода без _decorate_ в формате указал желаемые параметры явно.  
   Команда:  
   
   __`git log v0.12.23~1..v0.12.24 --format="%H %s"`__  
   
   Вывод: 
   ```
   33ff1c03bb960b332be3af2e333462dde88b279e v0.12.24
   b14b74c4939dcab573326f4e3ee2a62e23e12f89 [Website] vmc provider links
   3f235065b9347a758efadc92295b540ee0a5e26e Update CHANGELOG.md
   6ae64e247b332925b872447e9ce869657281c2bf registry: Fix panic when server is unreachable
   5c619ca1baf2e21a155fcdb4c264cc9e24a2a353 website: Remove links to the getting started guide's old location
   06275647e2b53d97d4f0a19a0fec11f6d69820b5 Update CHANGELOG.md
   d5f9411f5108260320064349b757f55c09bc4b80 command: Fix bug when using terraform login on Windows
   4b6d06cc5dcb78af637bbb19c198faff37a066ed Update CHANGELOG.md
   dd01a35078f040ca984cdd349f18d0b67e486c35 Update CHANGELOG.md
   225466bc3e5f35baa5d07197bbc079345b77525e Cleanup after v0.12.23 release
   85024d3100126de36331c6982bfaac02cdab9e76 v0.12.23
   ```
   
1. > Найдите коммит в котором была создана функция `func providerSource`, ее определение в коде выглядит 
так `func providerSource(...)` (вместо троеточего перечислены аргументы).

   Команда:  
   
   __`git log --format="%H" -S"func providerSource(" --diff-filter=A`__  
   
   Вывод: 
   ```
   8c928e83589d90a031f811fae52a81be7153e82f
   ```
   
1. > Найдите все коммиты в которых была изменена функция `globalPluginDirs`.

   Сперва потребовалось выяснить имя файла, в котором была определена указанная функция.  
   Команда:  
   
   __`git log --format="" -S"globalPluginDirs" --diff-filter=A --name-only`__  
   
   Вывод: 
   ```
   plugins.go
   ```
   
   Затем стало возможно использовать поиск по имени функции, однако решил использовать
   регулярные выражения как более надёжный фильтр, в отличии от `-L :funcname:filename`.  
   Команда:  
   
   __`git log --format=oneline -s -L /globalPluginDirs/,/^}/:plugins.go`__  
   
   Вывод: 
   ```
   78b12205587fe839f10d946ea3fdc06719decb05 Remove config.go and update things using its aliases
   52dbf94834cb970b510f2fba853a5b49ad9b1a46 keep .terraform.d/plugins for discovery
   41ab0aef7a0fe030e84018973a64135b11abcd70 Add missing OS_ARCH dir to global plugin paths
   66ebff90cdfaa6938f26f908c7ebad8d547fea17 move some more plugin search path logic to command
   8364383c359a6b738a436d1b7745ccdce178df47 Push plugin discovery down into command package
   ```
   
1. > Кто автор функции `synchronizedWriters`? 

   Команда:  
   
   __`git log -S"func synchronizedWriters(" --diff-filter=A -s --format="%an"`__  
   
   Вывод: 
   ```
   Martin Atkins
   ```
   