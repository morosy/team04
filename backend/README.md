[MySQL Install](https://dev.mysql.com/downloads/mysql/)


MySQL 8.4.5 LTS


```
CREATE DATABASE team04_db CHARACTER SET utf8mb4;
CREATE USER 'team04'@'localhost' IDENTIFIED BY 'advinfteam04';
GRANT ALL PRIVILEGES ON team04_db.* TO 'team04'@'localhost';
```


```
python manage.py createsuperuser
Username: team04
password: advinfteam04
```
