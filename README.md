# Django personal blog
## Project to track everything I learned and have done (for personal usage)

## Installation
Setup environment
```sh
cd blog
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
Create local config file
```sh
mkdir config
cd config/
touch __init__.py local_settings.py
```
Example of local_settings.py
```sh
from settings import *  # important

SECRET_KEY = 'your key'

DATABASES['default']['NAME'] = '<db_name>'        # redefine if necessary
DATABASES['default']['USER'] = '<db_user_name>'   # redefine if necessary
DATABASES['default']['PASSWORD'] = '<db_user_password>'

# url options
SITE_URL = 'personal-blog.local' # specify site base url
SITE_SCHEME = "http"
PARENT_HOST = ".%s" % SITE_URL
HOST_PORT = '4403'  # specify port if necessary 
SITE = "%s://%s:%s" % (SITE_SCHEME, SITE_URL, HOST_PORT)

# debug options
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True
```
Create database
```sh
sudo su postgres
psql
CREATE USER <db_user_name> WITH ENCRPPTED PASSWORD '<db_user_password>' superuser;
CREATE DATABASE <db_name> WITH OWNER <db_user_name> ENCODING 'UTF8';
```
Set hosts
```sh
sudo vim /etc/hosts
127.0.0.1               <SITE_URL>
127.0.0.1         admin.<SITE_URL>
```
example
```sh
127.0.0.1               personal-blog.local
127.0.0.1         admin.personal-blog.local
```

# Useful fab commands
**fab runserver** - start server \
**fab dump_db** - dump current database to .sql script in dumps/ folder \
**fab restore_db** - restore last found .sql file in dumps/ folder to EMPTY database \
**fab deploy_local** - deploy project
- branch (main by default)
- git checkout and pull from the branch
- install requirements.txt
- migrate database
- collect static

**fab check** - scan code in project \
**fab create_graph_models** - create class diagram of the project to graphs/ \
- parameters: Classes to display in .dot file \
- parameters example: fab create_graph_models:User,Post,PostLike

# Testing
Constants needed to set up: \
Required: \
DATABASE_TEST_NAME=<db_for_test_name> \
DATABASE_TEST_USER=<db_for_test_user_name> \
DATABASE_TEST_PSW=<db_for_test_user_password> \
Optional: \
DATABASE_TEST_HOST=<db_host> (localhost by default) \

### Tests counter: **99**
### Files coverage: **94%**
### Lines coverage: **95%**
