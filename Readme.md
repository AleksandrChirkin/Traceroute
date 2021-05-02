# Traceroute
Автор: Чиркин Александр (КБ-201)
Утилита трассировки 


## Требования

Python версии не ниже 3.7
Для запуска трассировки в UNIX необходимо войти в режим sudo

```

## Пример использования

```bash
$ sudo python3 -m traceroute archlinux.org
1. 95.217.163.246
10.113.224.1, local

2. 95.217.163.246
10.254.253.252, local

3. 95.217.163.246
10.255.201.6, local

4. 95.217.163.246
10.255.101.5, local

5. 95.217.163.246
10.255.100.2, local

6. 95.217.163.246
195.239.186.161, Russia, AS3216 PJSC Vimpelcom

7. 95.217.163.246
79.104.225.146, Russia

8. 95.217.163.246
80.249.209.55, Netherlands

9. 95.217.163.246
213.239.252.218, Germany, AS24940 Hetzner Online GmbH

10. 95.217.163.246
213.239.245.69, Germany, AS24940 Hetzner Online GmbH

11. 95.217.163.246
88.198.249.94, Germany, AS24940 Hetzner Online GmbH

12. 95.217.163.246
95.216.132.37, Finland, AS24940 Hetzner Online GmbH

13. 95.217.163.246
95.217.163.246, Finland, AS24940 Hetzner Online GmbH
```
