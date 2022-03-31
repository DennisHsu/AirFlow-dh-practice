# AirFlow-dh-practice
# 環境架設

```bash
docker pull ubuntu
```

```bash
# docker run -it -v [local path]:[docker path]  -p 8001:8001 --name airflow ubuntu:latest

docker run -it -v /Users/dennishsu/Documents/MyProject/Python_Project/AirFlowTutorial/storage:/storage  -p 8001:8001 --name airflow ubuntu:latest
```

## 安裝Airflow

### **安裝Python3**

```bash
apt-get update
apt-get install python3
apt-get install curl
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
apt-get install python3-distutils
python3 get-pip.py

# Create venv
apt-get install python3-venv
python3 -m venv server_venv
source /server_venv/bin/activate
```

建立一個Python3 環境的image (option)

`docker commit -m "init py3 image" -a "dh" [container id] python3_env:v1.0`

### 安裝 Postgres SQL

```bash
apt install postgresql postgresql-contrib

#安裝缺少的套件
apt-get install libpq-dev

pip install wheel

pip install psycopg2
# or
pip install psycopg2-binary

# 開啟 Service
service postgresql start

建立使用者
su - postgres
```

```bash
# 新建資料夾
mkdir /storage/db

# 關閉服務
service postgresql stop

# 找出資料路徑
find / -name postgresql.conf

#cp -rf [預設路徑] [自訂路徑]
cp -rf /var/lib/postgresql/12/main /storage/db

#chown -R postgres:postgres [自訂路徑]
chown -R postgres:postgres /storage/db

# 
chmod 700 /storage/db

# 修改 chmod 700 [自訂路徑]
vim /etc/postgresql/12/main/postgresql.conf
data_directory='/storage/db/main'

service postgresql start
```


以上都還在環境設定

接下來真的要安裝了 XD

[ssh, postgres, mongo, sftp, ftp, http] 代表我要安裝的Operator 清單

```bash
pip install 'apache-airflow[ssh, postgres, mongo, sftp, ftp, http]'

```

不相容問題

pip uninstall xxx

pip install xxx==[version]

```bash
ERROR: flask 1.1.4 has requirement Jinja2<3.0,>=2.10.1, but you'll have jinja2 3.0.3 which is incompatible.
ERROR: flask-jwt-extended 3.25.1 has requirement PyJWT<2.0,>=1.6.4, but you'll have pyjwt 2.3.0 which is incompatible.
ERROR: flask-appbuilder 3.4.4 has requirement PyJWT<2.0.0,>=1.7.1, but you'll have pyjwt 2.3.0 which is incompatible.
```

```bash
pip uninstall PyJWT

pip uninstall Jinja2

pip install Jinja2==2.10.1

pip install PyJWT==1.7.1
```

[此步驟可跳過]

開啟 airflow.cfg 檔案， 修改port

```bash
vim /root/airflow/airflow.cfg

[webserver]
# The base url of your website as airflow cannot guess what domain or
# cname you are using. This is used in automated emails that
# airflow sends to point links to the right web server
# base_url = http://localhost:8080 # 改成8001
base_url = http://localhost:8001

# Default timezone to display all dates in the UI, can be UTC, system, or
# any IANA timezone string (e.g. Europe/Amsterdam). If left empty the
# default value of core/default_timezone will be used
# Example: default_ui_timezone = America/New_York
default_ui_timezone = UTC

# The ip specified when starting the web server
web_server_host = 0.0.0.0

# The port on which to run the web server
# web_server_port = 8080 #改成8001
web_server_port = 8001
```

初步測試 使用Sqlite

```bash
airflow db init

airflow webserver -p 8001 # default 8080
```

http://127.0.0.1:8001

看到AirFlow畫面，代表運行成功

使用PostgreSQL

```bash
su - postgres
psql

CREATE DATABASE af_db;
CREATE USER af_user WITH PASSWORD 'airflow8001';
GRANT ALL PRIVILEGES ON DATABASE af_db TO af_user;
```

修改DB

```bash
vim /root/airflow/airflow.cfg

[core]
# executor = SequentialExecutor #改成executor = LocalExecutor
executor = LocalExecutor

#sql_alchemy_conn = sqlite:////root/airflow/airflow.db  #改成postgresql
sql_alchemy_conn = postgresql+psycopg2://af_user:airflow8001@localhost:5432/af_db
```

設定dag 位置

```bash
# 建立放dag的資料夾
mkdir -p /storage/airflow/dags

vim /root/airflow/airflow.cfg

[core]

#dags_folder = /root/airflow/dags #改成外部資料夾
dags_folder = /storage/airflow/dags
```

```bash
airflow db init

airflow users create --email youremail@mail.com --firstname D --lastname H --role Admin --username admin
# 輸入兩次密碼

airflow webserver -p 8001 # default 8080
```

Extra:

[https://airflow.apache.org/docs/apache-airflow/stable/extra-packages-ref.html](https://airflow.apache.org/docs/apache-airflow/stable/extra-packages-ref.html)
