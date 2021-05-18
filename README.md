# brandi-admin

### server 실행 방법

1. config.py 파일을 만들고 DB접속 정보를 입력한다.
```
database = {
    'host' : 'localhost',
    'port' : 3306,
    'user' : 'root',
    'passwd' : 'your password',
    'db' : 'your db name',
    'charset' : 'utf8'
}
```

2.app.py가 있는 디렉토리에서 아래 명령어를 입력한다.
```
python run.py 
```
