# Домашнее задание к занятию "3.5. Файловые системы"

## Модуль 3. Основы системного администрирования

## Студент: Иван Жиляев

Ответы на вопросы из задания:

1. >Узнайте о [sparse](https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D0%B7%D1%80%D0%B5%D0%B6%D1%91%D0%BD%D0%BD%D1%8B%D0%B9_%D1%84%D0%B0%D0%B9%D0%BB) (разряженных) файлах.

   Ознакомился со статьёй. Мне кажется, что использование разрежённых файлов достаточно редко имеет смысл - только в специфичных случаях, хорошие примеры которых есть в статье (бэкапы блочных устройств, образы дисков).

1. >Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?

   Нет, так сделать нельзя, т.к. информация о владельце и правах для файла по сути является информацией о правах на `inode`. Она хранится в метаданных файловой системы и, раз жёсткие ссылки указывают на один и тот же `inode`, то и права будут одинаковые.

1. >Сделайте `vagrant destroy` на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile следующим:
   >
   >```bash
   >Vagrant.configure("2") do |config|
   >  config.vm.box = "bento/ubuntu-20.04"
   >  config.vm.provider :virtualbox do |vb|
   >    lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
   >    lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
   >    vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
   >    vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
   >    vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
   >    vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
   >  end
   >end
   >```
   >
   >Данная конфигурация создаст новую виртуальную машину с двумя дополнительными неразмеченными дисками по 2.5 Гб.

   Создал требуемый [Vagrantfile](vagrant/Vagrantfile); виртуалка запустилась успешно, пустые диски видны.

   ```
   vagrant@vagrant:~$ lsblk
   NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
   sda                    8:0    0   64G  0 disk 
   ├─sda1                 8:1    0  512M  0 part /boot/efi
   ├─sda2                 8:2    0    1K  0 part 
   └─sda5                 8:5    0 63.5G  0 part 
     ├─vgvagrant-root   253:0    0 62.6G  0 lvm  /
     └─vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]
   sdb                    8:16   0  2.5G  0 disk 
   sdc                    8:32   0  2.5G  0 disk 
   ```

1. >Используя `fdisk`, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.

   Программа `fdisk` работает в интерактивном режиме, необходимые настройки были выполнены следующим образом:

   ```
   vagrant@vagrant:~$ sudo fdisk /dev/sdb

   ...

   Command (m for help): g
   Created a new GPT disklabel (GUID: C64B3E5F-43ED-5949-A3FD-EA4A4325AEB7).

   Command (m for help): n
   Partition number (1-128, default 1): 
   First sector (2048-5242846, default 2048): 
   Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-5242846, default 5242846): +2G

   Created a new partition 1 of type 'Linux filesystem' and of size 2 GiB.

   Command (m for help): n
   Partition number (2-128, default 2): 
   First sector (4196352-5242846, default 4196352): 
   Last sector, +/-sectors or +/-size{K,M,G,T,P} (4196352-5242846, default 5242846): 

   Created a new partition 2 of type 'Linux filesystem' and of size 511 MiB.

   Command (m for help): w
   The partition table has been altered.
   Calling ioctl() to re-read partition table.
   Syncing disks.
   ```

1. >Используя `sfdisk`, перенесите данную таблицу разделов на второй диск.

   Для переноса таблицы разделов воспользовался дамп-файлом:

   ```
   vagrant@vagrant:~$ sudo sfdisk --dump /dev/sdb > sdb.dump
   vagrant@vagrant:~$ sudo sfdisk /dev/sdc < sdb.dump
   ```

1. >Соберите `mdadm` RAID1 на паре разделов 2 Гб.

   Массив создал командой `sudo mdadm --create /dev/md0 --raid-devices=2 --level=1 /dev/sd[bc]1`.

1. >Соберите `mdadm` RAID0 на второй паре маленьких разделов.

   Этот массив создал командой `sudo mdadm --create /dev/md1 --raid-devices=2 --level=0 /dev/sd[bc]2`.  
   На данный момент структура блочных устройств выглядит так:

   ```
   vagrant@vagrant:~$ lsblk /dev/sd[bc]
   NAME    MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
   sdb       8:16   0  2.5G  0 disk  
   ├─sdb1    8:17   0    2G  0 part  
   │ └─md0   9:0    0    2G  0 raid1 
   └─sdb2    8:18   0  511M  0 part  
     └─md1   9:1    0 1017M  0 raid0 
   sdc       8:32   0  2.5G  0 disk  
   ├─sdc1    8:33   0    2G  0 part  
   │ └─md0   9:0    0    2G  0 raid1 
   └─sdc2    8:34   0  511M  0 part  
     └─md1   9:1    0 1017M  0 raid0 
   ```

1. >Создайте 2 независимых PV на получившихся md-устройствах.

   PV создадим командой `sudo pvcreate /dev/md[01]`.  
   Проверка успешного создания:

   ```
   vagrant@vagrant:~$ sudo pvdisplay /dev/md[01]
     "/dev/md0" is a new physical volume of "<2.00 GiB"
     --- NEW Physical volume ---
     PV Name               /dev/md0
     VG Name               
     PV Size               <2.00 GiB
     Allocatable           NO
     PE Size               0   
     Total PE              0
     Free PE               0
     Allocated PE          0
     PV UUID               5rQ3UB-Hmk8-RRlE-aJfE-mJBv-DNi1-jHtWGP
      
     "/dev/md1" is a new physical volume of "1017.00 MiB"
     --- NEW Physical volume ---
     PV Name               /dev/md1
     VG Name               
     PV Size               1017.00 MiB
     Allocatable           NO
     PE Size               0   
     Total PE              0
     Free PE               0
     Allocated PE          0
     PV UUID               LkPtro-bOSg-tWCt-aApM-4Ckd-dMKR-nbDh41
   ```

1. >Создайте общую volume-group на этих двух PV.

   Для этого выполним команду `sudo vgcreate VG0 /dev/md[01]`.  
   Проверим корректность получивнейся группы:

   ```
   vagrant@vagrant:~$ sudo vgdisplay VG0
     --- Volume group ---
     VG Name               VG0
     System ID             
     Format                lvm2
     Metadata Areas        2
     Metadata Sequence No  1
     VG Access             read/write
     VG Status             resizable
     MAX LV                0
     Cur LV                0
     Open LV               0
     Max PV                0
     Cur PV                2
     Act PV                2
     VG Size               <2.99 GiB
     PE Size               4.00 MiB
     Total PE              765
     Alloc PE / Size       0 / 0   
     Free  PE / Size       765 / <2.99 GiB
     VG UUID               3pIXql-f3yT-wPZA-0u7b-sRDy-bWBW-gzUbkJ
   ```

1. >Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.

   Создадим LV командой `sudo lvcreate --name LV0 --size 100M --type linear VG0 /dev/md1`.  
   Проверка:
   ```
   vagrant@vagrant:~$ sudo lvdisplay VG0/LV0
     --- Logical volume ---
     LV Path                /dev/VG0/LV0
     LV Name                LV0
     VG Name                VG0
     LV UUID                7XRvMh-3Q7P-eae0-lqeS-ZyN2-FPhJ-iCdiCf
     LV Write Access        read/write
     LV Creation host, time vagrant, 2020-09-21 22:29:57 +0500
     LV Status              available
     # open                 0
     LV Size                100.00 MiB
     Current LE             25
     Segments               1
     Allocation             inherit
     Read ahead sectors     auto
     - currently set to     4096
     Block device           253:2
   ```

1. >Создайте `mkfs.ext4` ФС на получившемся LV.

   Выполнил команду `sudo mkfs.ext4 /dev/VG0/LV0`.

1. >Смонтируйте этот раздел в любую директорию, например, `/tmp/new`.

   Создадим точку монтирования и смонтируем раздел:

   ```
   vagrant@vagrant:~$ sudo mkdir /tmp/new
   vagrant@vagrant:~$ sudo mount /dev/VG0/LV0 /tmp/new
   ```

1. >Поместите туда тестовый файл, например `wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz`.

   Тестовый файл успешно загрузился:

   ```
   vagrant@vagrant:~$ ll /tmp/new/test.gz 
   -rw-r--r-- 1 root root 19275240 Sep 21 21:43 /tmp/new/test.gz
   ```

1. >Прикрепите вывод `lsblk`.

   Прикрепляю полный вывод `lsblk`:

   ```
   vagrant@vagrant:~$ lsblk
   NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
   sda                    8:0    0   64G  0 disk  
   ├─sda1                 8:1    0  512M  0 part  /boot/efi
   ├─sda2                 8:2    0    1K  0 part  
   └─sda5                 8:5    0 63.5G  0 part  
     ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /
     └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
   sdb                    8:16   0  2.5G  0 disk  
   ├─sdb1                 8:17   0    2G  0 part  
   │ └─md0                9:0    0    2G  0 raid1 
   └─sdb2                 8:18   0  511M  0 part  
     └─md1                9:1    0 1017M  0 raid0 
       └─VG0-LV0        253:2    0  100M  0 lvm   /tmp/new
   sdc                    8:32   0  2.5G  0 disk  
   ├─sdc1                 8:33   0    2G  0 part  
   │ └─md0                9:0    0    2G  0 raid1 
   └─sdc2                 8:34   0  511M  0 part  
     └─md1                9:1    0 1017M  0 raid0 
       └─VG0-LV0        253:2    0  100M  0 lvm   /tmp/new
   ```

1. >Протестируйте целостность файла:
   >
   >```bash
   >root@vagrant:~# gzip -t /tmp/new/test.gz
   >root@vagrant:~# echo $?
   >0
   >```

   Тестирование целостности прошло успешно.

1. >Используя pvmove, переместите содержимое PV с RAID0 на RAID1.

   Переместил командой `sudo pvmove /dev/md1 /dev/md0`.  
   Посмотрим на структуру дисков теперь:

   ```
   vagrant@vagrant:~$ lsblk /dev/sd[bc]
   NAME          MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
   sdb             8:16   0  2.5G  0 disk  
   ├─sdb1          8:17   0    2G  0 part  
   │ └─md0         9:0    0    2G  0 raid1 
   │   └─VG0-LV0 253:2    0  100M  0 lvm   /tmp/new
   └─sdb2          8:18   0  511M  0 part  
     └─md1         9:1    0 1017M  0 raid0 
   sdc             8:32   0  2.5G  0 disk  
   ├─sdc1          8:33   0    2G  0 part  
   │ └─md0         9:0    0    2G  0 raid1 
   │   └─VG0-LV0 253:2    0  100M  0 lvm   /tmp/new
   └─sdc2          8:34   0  511M  0 part  
     └─md1         9:1    0 1017M  0 raid0
   ```

1. >Сделайте `--fail` на устройство в вашем RAID1 md.

   Развалил зеркало:

   ```
   vagrant@vagrant:~$ sudo mdadm /dev/md0 --fail /dev/sdb1
   mdadm: set /dev/sdb1 faulty in /dev/md0
   ```

1. >Подтвердите выводом `dmesg`, что RAID1 работает в деградированном состоянии.

   Получаем подтверждение:

   ```
   vagrant@vagrant:~$ dmesg -e | tail -n2
   [Sep21 23:00] md/raid1:md0: Disk failure on sdb1, disabling device.
                 md/raid1:md0: Operation continuing on 1 devices.
   ```

1. >Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:
   >
   >```bash
   >root@vagrant:~# gzip -t /tmp/new/test.gz
   >root@vagrant:~# echo $?
   >0
   >```

   Да, с файлом всё в порядке:

   ```
   vagrant@vagrant:~$ ll /tmp/new/test.gz
   -rw-r--r-- 1 root root 19275240 Sep 21 21:43 /tmp/new/test.gz
   vagrant@vagrant:~$ gzip -t /tmp/new/test.gz
   vagrant@vagrant:~$ echo $?
   0
   ```

1. >Погасите тестовый хост, `vagrant destroy`.

   Стенд был успешно ликвидирован.
