# inspection-xls-processing


## Requirements
- git
- docker-ce

## Install
```
git clone https://github.com/btrungchi/inspection-xls-processing
cd inspection-xls-processing
sudo docker build -t inspection-xls-processing .
```

## How to run
```
sudo docker run -it -p 8000:8000 inspection-xls-processing
```

Then access the site at http://localhost:8000

## Run test case
```
sudo docker exec -it [CONTAINER ID] python web/manage.py test mainapp
```

## Critical source files

- xsl parsing source code: web/mainapp/xlsparse.py

- database schema source code:  web/mainapp/postgresql.py

- unit test source code: web/mainapp/tests.py

- logging directory:  web/logs/


