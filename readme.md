# Play Watcher : Log File Manager 
## 기술 스택 
* [DJango](https://djangoproject.com/) : Web Framework
  * [Django Github](https://github.com/django/django)
  * [Django 4.1 Docs](https://docs.djangoproject.com/en/4.1/)
* [bootstrap v5](https://getbootstrap.com/docs/5.0/) : UI & UX, Standard CSS 
* [dropzonee](https://www.dropzone.dev/) : File-Upload Drag&Drop Control
  * [dropzone+django example Github](https://github.com/nicksonlangat/django-dropzone)
  * [dropzone docs](https://docs.dropzone.dev/)
* [Nginx](https://www.nginx.com/) : Web Server & Proxy Server
  * [Nginx Docs](https://nginx.org/en/docs/?_ga=2.238970761.84488645.1663849073-1728988258.1663849073)
* Waitress : WSGI (Web Server Gateway Interface)
  * [Waitress Github](https://github.com/Pylons/waitress)
  * [Waitress Docs](https://docs.pylonsproject.org/projects/waitress/en/latest/)
  * [nginx + Waitress + windows](https://github.com/Johnnyboycurtis/webproject#nginx-and-waitress)

# 배포 
### 소스를 배포할 서버로 복사한다.
다음 경로를 예시로 설명한다. 
```bash
d:\vx_sol\playwatcher\fileuploadserver\src 
```

### 어플리케이션을 구동할 Python 가상 환경 생성한다. 
```bash
cd d:\vx_sol\playwatcher\fileuploadserver

python -m venv d:\vx_sol\playwatcher\fileuploadserver\venv
```

### 필수 패키지를 설정한다. 

어플케이션을 구동할 가상 환경을 활성화하고 requirements.txt 파일에 포함된 패키지를 설치한다.
```bash
d:\vx_sol\playwatcher\fileuploadserver\venv\scripts\activate

pip install -r d:\vx_sol\playwatcher\fileuploadserver\src\requirements.txt
```

### site 설정 
{src root}<code>\mysite\settings.py</code> 을 열고 다음 값을 설정한다.
```python 
### 서버 구동 정보 
U_HOST = '127.0.0.1'
U_PORT_RANGE = (8000, 8003)     # ex) ( 8000, 8003 ) 으로 지정할 경우 8000~8003 까지 총 4개의 어플리케이션 구동된다.
```

### Nginx 설정 
다음 <code>scripts\nginx_sample.conf</code>를 참고하여 설정한다.
파일 업로드를 진행하기 위해서 다음 설정이 반드시 추가되어 한다. 
```bash
proxy_request_buffering off;    # 파일업로드를 위한 설정.
...
client_max_body_size 10M;       # 업로드 파일 사이즈 제한.
```

또한, 어플리케이션 정상 동작하기 위해서는 <code>location /fs</code><code>location /fs_static</code>, <code>location /fs_media</code>는 반드시 설정해야 한다. 
```bash
    # 생략 ...
    # mysite\settings.py 에서 다음과 같이 설정했을 때 기준의 upstream 설정.
    # U_PORT_RANGE = (8000, 8003)  
    upstream fs {
        least_conn;
        server 127.0.0.1:8000;
        server 127.0.0.1:8001;
        server 127.0.0.1:8002;
        server 127.0.0.1:8003;
    }
    # 생략 ...
    server{
        # 생략 ...
        ## Log File Manager Application 
        location /fs {
            proxy_pass http://fs;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_hide_header 'x-frame-options';
            access_log off;
	        client_max_body_size 10M;       # 업로드 파일 사이즈 제한.
        }

        ## Log File Manager Application에서 사용하는 static file을 host를 위한 설정. 
        # ( mysite/settings.py : STATIC_ROOT 값을 지정 )
        location /fs_static {
            # 어플리케이션에 소스에 있는 fs_static 폴더의 절대경로 지정 
            alias D:\sol\playwatcher\fileuploadserver\src\fs_static;    
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            gzip_static on;
            expires max;
            add_header Cache-Control public;
            access_log off;
        }

        ## Log File Manager Application에서 업로드된 파일을 host하기 위한 설정. .  
        # ( mysite/settings.py : MEDIA_ROOT 값을 지정 )
        location /fs_madia {
            # 어플리케이션에 소스에 있는 fs_media 폴더의 절대경로 지정 
            alias D:\sol\playwatcher\fileuploadserver\src\fs_media;   
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            gzip_static on;
            expires max;
            add_header Cache-Control public;
            access_log off;
        }
        # 생략 ...
    }
```



## 서버 구동
----
### 디버그용 서버 시작
```bash
run_debug.bat
```

### 디버그용 서버 시작
```bash
run_debug.bat
```


## Django 관리 도구 및 설정 

### Django static 파일 수집 
```bash
python manage.py collectstatic
```

## Django 모델 생성하는 방법. 
---
[원문(https://learnbatta.com/course/django/django-create-table-from-model/)]


### 1) 모델 생성 
```python 
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
```

### 2) 마이그레이션 파일 생성

```bash
python manage.py makemigrations core

```

migrations/ 폴더에 마이그레이션 파일이 생성된다.

예시)
```bash
Migrations for 'core':
  core\migrations\0002_trans.py
    - Create model Trans       
```

### 3) 마이그레이션 실행
```bash
python manage.py migrate core
```

테스트로 실행해볼 경우 --fake 옵션을 지정하면 된다.
```bash
python manage.py migrate core --fake
```

예시)
```bash
Migrations for 'core':
  core\migrations\0002_trans.py
    - Create model Trans       
```

예시)
```bash
Operations to perform:
  Apply all migrations: core
Running migrations:
  Applying core.0002_trans... OK
```

## Bootstrap v5 설치
---
```python 
pip install django-bootstrap-v5
```

Add to INSTALLED_APPS in your settings.py:
```python 
INSTALLED_APPS  = [
#...
'bootstrap5'
#...
]
```


# 디렉토리 구조
```bash
Log File Manager
│  db.sqlite3               # Main db
│  manage.py                # DJango Application 관리 도구 
│  readme.md                # readme.md
│  requirements.txt         # requirements.txt 
│  run_debug.bat            # 디버그용 서버 실행 
│  run_server.py            # 프로덕션용 서버 실행 
├─core                      # File-Upload, File-List 기능 구현.
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │  
│  ├─migrations
│       __init__.py
│   
├─fs_media                  # 업로드된 파일 저장하는 ROOT 폴더
│  └─playlog                
│   
├─fs_static
│  │  fsdropzone_main.js    # template/index.html에서 사용되는 dropzone 객체 설정함수 
│  │  style.css             # 공통 CSS
│  │  utils.js              # 공통 함수
│  ├─admin                  # admin site static files
│  ├─django_tables2         # django_tables2 모듈 CSS 
│  ├─dropzone
│  └─font-awesome
│          
├─logs                      # 로그 폴더
│      
├─mysite                    # 메인 application 폴더
│  │  asgi.py
│  │  settings.py
│  │  urls.py
│  │  wsgi.py
│  └─ __init__.py
│
├─scripts                       # 모듈 설치나 배포 서버에서 서버 실행 등의 스크립트
│      deployment_readme.md
│      fileserver_sever_run.cmd
│      makesourcetree.cmd
│      nginx_sample.conf        # Nginx 설정파일 예시
│      package_intall.bat
│      venv_console.cmd
│      
├─templates                     # 어플리케이션 템플릿 (html)
│  │  base.html
│  │  filelist.html
│  │  footer.html
│  │  index.html
│  │  navi.html
│  │  
│  └─admin                      # Admin 용 어플리케이션
│          base_site.html
│          
└─test                          # 각종 테스트
    │  gunicorn.py
    │  uwsgi.py
    └─__pycache__
            gunicorn.cpython-37.pyc
            
```


# 이슈
### python manage.py collectstatic 에러
```bash
django.core.exceptions.ImproperlyConfigured: You're using the staticfiles app without having set the STATIC_ROOT setting to a filesystem path.
``` 
위와 같은 오류가 발생하면 settings.py에 다음 코드 추가.
```python
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

# Reference Site
* [bootstrap](https://getbootstrap.com/docs/5.0/forms/layout/) : Standard CSS 
* [dropzonee](https://github.com/nicksonlangat/django-dropzone) : File-Upload Drag&Drop Control
* [DJango](https://docs.djangoproject.com/) : Web Framework
  * [Django Github](https://github.com/django/django)



