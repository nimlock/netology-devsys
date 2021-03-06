# Домашнее задание к занятию "3.2. Работа в терминале, лекция 2"

## Модуль 3. Основы системного администрирования

## Студент: Иван Жиляев

Ответы на вопросы из задания:

1. >Какого типа команда `cd`? Попробуйте объяснить, почему она именно такого типа; опишите ход своих мыслей, если считаете что она могла бы быть другого типа.

   Вызовом команды `type` можно узнать тип команды:
   
   ```
   vagrant@vagrant:~$ type -a cd
   cd is a shell builtin
   ```

   Мы наблюдаем, что `cd` является командой, встроенной в оболочку `bash`. Я считаю что она именно `builtin`, так как её задача - менять файловый дескриптор `cwd` через изменение переменной `PWD` именно используемого экземпляра оболочки. Её использование в виде отдельной программы только усложнило бы это преобразование.

1. >Какая альтернатива без pipe команде `grep <some_string> <some_file> | wc -l`? `man grep` поможет в ответе на этот вопрос. Ознакомьтесь с [документом](http://www.smallo.ruhr.de/award.html) о других подобных некорректных вариантах использования pipe.

   Альтернативой является добавление параметра `--count` (подсчёт строк количества строк, содержащих искомый запрос) к grep: `grep -c <some_string> <some_file>`

1. >Какой процесс с PID `1` является родителем для всех процессов в вашей виртуальной машине Ubuntu 20.04?

   Это процесс `systemd(1)` - самый верхний уровень в выводе `pstree -p`.

1. >Как будет выглядеть команда, которая перенаправит вывод stderr `ls` на другую сессию терминала?

   Сперва убедимся что имеется другая сессия терминала, методом исключения определим её номер и тогда искомая команда будет выглядеть так:

   ```
   vagrant@vagrant:~$ ls /dev/pts
   0  1  ptmx
   vagrant@vagrant:~$ tty
   /dev/pts/0
   vagrant@vagrant:~$ ls /root 2> /dev/pts/1
   ```

1. >Получится ли одновременно передать команде файл на stdin и вывести ее stdout в другой файл? Приведите работающий пример.

   Да, так можно сделать:

   ```
   vagrant@vagrant:~$ cat file1 
   text template
   vagrant@vagrant:~$ sed 's/text/string/' <file1 >file2
   vagrant@vagrant:~$ cat file2
   string template
   ```

1. >Получится ли вывести находясь в графическом режиме данные из PTY в какой-либо из эмуляторов TTY? Сможете ли вы наблюдать выводимые данные?

   Да, это получится сделать, но следует учесть аспект полномочий. Так, например, командой `echo HELLo! > /dev/tty2` можно вывести сообщение в tty2, если в нём был выполнен вход под тем же пользователем. Однако, с привелегиями суперпользователя возможно доставить сообщение в терминал и без выполнения авторизации в нём.

   Отправленные сообщения можно наблюдать переключившить в соответствующий терминал.

1. >Выполните команду `bash 5>&1`. К чему она приведет? Что будет, если вы выполните `echo netology > /proc/$$/fd/5`? Почему так происходит?

   После выполнения команды `bash 5>&1` будет запущен новый интерактивный экземпляр оболочки с дополнительным файловым дескриптором `5`, перенаправляющим свой поток данных в `stdout`.

   При выполнении `echo netology > /proc/$$/fd/5` мы увидим вывод на `stdout` слова `netology`, так как всё, что направлено на файловый дескриптор `5` перенаправляется на дескриптор `1`.

1. >Получится ли в качестве входного потока для pipe использовать только stderr команды, не потеряв при этом отображение stdout на pty? Напоминаем: по умолчанию через pipe передается только stdout команды слева от `|` на stdin команды справа.
Это можно сделать, поменяв стандартные потоки местами через промежуточный новый дескриптор, который вы научились создавать в предыдущем вопросе.

   Да, получится. Пример команды, с учётом наличия перенаправления `5>&1` из предыдущего задания:

   ```
   vagrant@vagrant:~$ ls /root ~/test_dir/ 2>&1 1>&5 | sed s/'Permission denied'/'You need more power!'/
   /home/vagrant/test_dir/:
   some_file1  some_file2  some_file3  some_file4
   ls: cannot open directory '/root': You need more power!
   ```

1. >Что выведет команда `cat /proc/$$/environ`? Как еще можно получить аналогичный по содержанию вывод?

   Эта команда отобразит все переменные для процесса текущей оболочки bash. Переменные разделены символом `NULL`.

   Аналогичный по содержанию (но не по форматированию) вывод можно получить командой `env`.

1. >Используя `man`, опишите что доступно по адресам `/proc/<PID>/cmdline`, `/proc/<PID>/exe`.

   В файле `/proc/<PID>/cmdline` содержится команда, породившая процесс, вместе с аргументами. Они представленны как массив строк, разделённых символом `NULL` - `'\0'`. В случае, если процесс становится `zombie`, этот файл будет пустым.

   Файл `/proc/<PID>/exe` представляет собой символьную ссылку на бинарный файл, который был запущен для запуска процесса.

1. >Узнайте, какую наиболее старшую версию набора инструкций SSE поддерживает ваш процессор с помощью `/proc/cpuinfo`.

   Согласно секции `flags` указанного файла самая старшая версия поддерживаемых инструкций SSE - __4.2__, на что указывает запись `sse4_2`.

1. >При открытии нового окна терминала и `vagrant ssh` создается новая сессия и выделяется pty. Это можно подтвердить командой `tty`, которая упоминалась в лекции 3.2. Однако:
   > ```bash
	>vagrant@netology1:~$ ssh localhost 'tty'
	>not a tty
   > ```
	>Почитайте, почему так происходит, и как изменить поведение.

   Вывод `not a tty` мы получаем, т.к. команда `tty` запускается не интерактивно и, соответственно, pty не выделяется. Вот цитата из `man ssh` описывающая это:

   >> When the user's identity has been accepted by the server, the server either executes the given command in a non-interactive session ...
   
   Для изменения этого поведения мы можем добавить к команде ключ `-t`:

   ```
   vagrant@vagrant:/proc/6020$ ssh -t localhost 'tty'
   vagrant@localhost's password: 
   /dev/pts/2
   Connection to localhost closed.
   ```

1. >Бывает, что есть необходимость переместить запущенный процесс из одной сессии в другую. Попробуйте сделать это, воспользовавшись `reptyr`. Например, так можно перенести в `screen` процесс, который вы запустили по ошибке в обычной SSH-сессии.

   Провёл опыты с использованием `reptyr`, в том числе по схеме "типичного использования" из [официального README.md](https://github.com/nelhage/reptyr#typical-usage-pattern).

   Перемещение процесса в другой сеанс работает, однако структура процессов (через pstree) после переноса несколько удивляет: 
   
   - переносимый процесс по факту остаётся в старой сессии (до её завершения)
   - у целевого процесса появляется такой же дочерний процесс, но в статусе `zombie` - в документации не нашёл ответа зачем он нужен
   - после завершения старой сессии целевой процесс в качестве PPID берёт `systemd(1)`, а не оболочку, в которой запускали `reptyr`

   Предполагаю, что всё станет понятно после изучения системных вызовов `ptrace(2)`, через которые работает `reptyr`, но пока понимания не хватает.
