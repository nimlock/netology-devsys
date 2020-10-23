# Домашнее задание к занятию "3.9. Элементы безопасности информационных систем"

## Модуль 3. Основы системного администрирования

## Студент: Иван Жиляев

Ответы на вопросы из задания:

1. >Установите [Hashicorp Vault](https://learn.hashicorp.com/vault) в виртуальной машине Vagrant/VirtualBox. Это не является обязательным для выполнения задания, но для лучшего понимания что происходит при выполнении команд (посмотреть результат в UI), можно по аналогии с netdata из прошлых лекций пробросить порт Vault на localhost:
   >
   >```bash
   >config.vm.network "forwarded_port", guest: 8200, host: 8200
   >```
   >
   >Однако, обратите внимание, что только-лишь проброса порта не будет достаточно – по-умолчанию Vault слушает на 127.0.0.1; добавьте к опциям запуска `-dev-listen-address="0.0.0.0:8200"`.

   Установку `vault` произвожу внутри [Vagrantfile](vagrant/Vagrantfile). Там же создаю override.unit-файл для него с желаемыми опциями запуска.

1. >Запустить Vault-сервер в dev-режиме (дополнив ключ `-dev` упомянутым выше `-dev-listen-address`, если хотите увидеть UI).

   Сервис запускается и доступен по URL `http://localhost:8200/`.

1. >Используя [PKI Secrets Engine](https://www.vaultproject.io/docs/secrets/pki), создайте Root CA и Intermediate CA.
   >Обратите внимание на [дополнительные материалы](https://learn.hashicorp.com/vault/secrets-management/sm-pki-engine) по созданию CA в Vault, если с изначальной инструкцией возникнут сложности.

   К сожалению, все действия пришлось проводить строго по оф.туториалу, т.к. используя лишь документацию вообще ничего не получалось.  
   В итоге я сформировал такой [алгоритм настройки](howto_setup_vault).

1. >Согласно этой же инструкции, подпишите Intermediate CA csr на сертификат для тестового домена (например, `netology.example.com` если действовали согласно инструкции).

   В качестве тестового домена я выбрал `lenta.ru`.

1. >Поднимите на localhost nginx, сконфигурируйте default vhost для использования подписанного Vault Intermediate CA сертификата и выбранного вами домена. Сертификат из Vault подложить в nginx руками.

   Не нашёл удобного способа экспорта полученных секретов из Vault (вижу что это key-value, но не ясно как правильно написать `vault kv get`), так что пришлось воспользоваться [stdout от команды запроса сертификата](stdout_of_cert_request) "в лоб". 
   
   Из консоли дёргаем части вывода и помещаем их в разнызые файлы:
   - приватный ключ получается из секции _private_key_
   - сертификат _certificate_ и _issuing\_ca_ согласно [мануалу](http://cuddletech.com/?p=959) сохраняем вместе в один файл

   Также пришлось форматировать содержимое "составного" файла, т.к. nginx ругался на то, что:
   - объявление сертификата (заключенное в дефисы) должно занимать всю строку (Vault добавляет значение поля key в начале строки)
   - сертификат должен иметь заголовок "BEGIN TRUSTED CERTIFICATE", но видимо из-за того, что сетрификат CA самоподписаный, слово "TRUSTED" отсутствовало - дописал вручную

   Полученные файлы указываем в дефолтном конфиге nginx в /etc/nginx/sites-enabled/default, проверяем правильность через `nginx -t`.

1. >Модифицировав `/etc/hosts` и [системный trust-store](http://manpages.ubuntu.com/manpages/focal/en/man8/update-ca-certificates.8.html), добейтесь безошибочной с точки зрения HTTPS работы curl на ваш тестовый домен (отдающийся с localhost). Рекомендуется добавлять в доверенные сертификаты Intermediate CA. Root CA добавить было бы правильнее, но тогда при конфигурации nginx потребуется включить в цепочку Intermediate, что выходит за рамки лекции. Так же, пожалуйста, не добавляйте в доверенные сам сертификат хоста.

   И этот шаг прошёл "со скрипом": сертификат Intermediate CA получилось "скормить" команде `update-ca-certificates` только после "ручного" помещения его в файл с расширением `.crt` и расположением в папке /usr/local/share/ca-certificates/.

   Итоговый результат успешный - `curl` считает, что с сертификатом всё хорошо:

   ```
   root@vagrant:~# dig +noall +answer lenta.ru
   lenta.ru.               0       IN      A       127.0.0.1

   root@vagrant:~# curl -I https://lenta.ru
   HTTP/1.1 200 OK
   Server: nginx/1.18.0 (Ubuntu)
   Date: Mon, 05 Oct 2020 16:47:18 GMT
   Content-Type: text/html
   Content-Length: 612
   Last-Modified: Mon, 05 Oct 2020 14:31:14 GMT
   Connection: keep-alive
   ETag: "5f7b2e32-264"
   Accept-Ranges: bytes

   root@vagrant:~# curl https://lenta.ru
   <!DOCTYPE html>
   <html>
   <head>
   <title>Welcome to nginx!</title>
   <style>
       body {
           width: 35em;
           margin: 0 auto;
           font-family: Tahoma, Verdana, Arial, sans-serif;
       }
   </style>
   </head>
   <body>
   <h1>Welcome to nginx!</h1>
   <p>If you see this page, the nginx web server is successfully installed and
   working. Further configuration is required.</p>

   <p>For online documentation and support please refer to
   <a href="http://nginx.org/">nginx.org</a>.<br/>
   Commercial support is available at
   <a href="http://nginx.com/">nginx.com</a>.</p>

   <p><em>Thank you for using nginx.</em></p>
   </body>
   </html>
   ```

1. >[Ознакомьтесь](https://letsencrypt.org/ru/docs/client-options/) с протоколом ACME и CA Let's encrypt. Если у вас есть во владении доменное имя с платным TLS-сертификатом, который возможно заменить на LE, или же без HTTPS вообще, попробуйте воспользоваться одним из предложенных клиентов, чтобы сделать веб-сайт безопасным (или перестать платить за коммерческий сертификат).

   У меня есть только купленное доменное имя, без сайта. Данное задание вынужден пропустить из-за отсутствия времени на выполнение - всё ушло на предшествующие пункты. Просить отсрочку не стал - не знаю сколько времени уйдёт на понимание работы с сертификатами. Однако обязательно выполню задание позже.

**Дополнительное задание вне зачета.**

>Вместо ручного подкладывания сертификата в nginx, воспользуйтесь [consul-template](https://medium.com/hashicorp-engineering/pki-as-a-service-with-hashicorp-vault-a8d075ece9a) для автоматического подтягивания сертификата из Vault.

   Дополнительное задание выполнить не успел, но ознакомился с приведённой статьёй. Кажется, она сможет хотя бы немного упорядочить для меня принципы работы Vault (да и PKI в целом), а её воспроизведение на стенде точно будет полезно как практика.
