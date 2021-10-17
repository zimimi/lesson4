## lesson4 - Blue/Green Deployment

Адреса проксі: http://18.157.77.215/read_posts

Сервер1: http://18.195.204.94/read_posts

Сервер2: http://3.68.110.82/read_posts

### ЕТАПИ

#### JENKINS-JOB-1-Initial-Deploy

1 - ПОЧАТКОВЕ РОЗГОРТАННЯ

Jenkins стягує репозиторій з GitHub по комміту в master гілку, запускає ansible playbook, який копіює репозиторій на сервера (server1 server2) і запускає там скрипт для розгортання додатку.

#### JENKINS-JOB-2-Blue-Green_Deployment

1 - Запускається скрипт, який перевіряє час останньої зміни додатку на віддаленому сервері в секундах і на виході дає слово "blue" або "green"

```
#!/bin/bash
VAR1=$(ssh -i simple_server.pem ubuntu@18.157.176.111 stat -c%Y lesson4)
VAR2=$(ssh -i simple_server.pem ubuntu@3.70.189.58 stat -c%Y lesson4)

if [[ $VAR1 -gt $VAR2 ]]
then
  blue_green_color=green
else
  blue_green_color=blue
fi
```

2 - Запускається 2_playbook.yml, який на вході отримує параметр "blue" або "green" і в залежності від цього параметра вибирає на який сервер заливати оновлений додаток.

Після того як додаток залито, змінюється файл конфігурації на проксі сервері і сервер на який було залито свіжий додаток стає main.
``` 
ansible-playbook 2_playbook.yml --extra-var "blue_green_color=$blue_green_color"
```
#### Використані інструменти: Terraform, AWS, Jenkins, HAProxy. Apache2, Flask, Ansible
