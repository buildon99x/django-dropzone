https://github.com/nicksonlangat/django-dropzone


# 모델 생성하는 방법. 
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
python manage.py makemigrations <app name>

```

migrations/ 폴더에 마이그레이션 파일이 생성된다.

예시)
```bash
Migrations for 'core':
  core\migrations\0002_trans.py
    - Create model Trans       
```


### 3) 마이그레이션 코드 실행해서 테이블 생성하기 
```bash
python manage.py migrate <app name>
```

예시)
```bash
Operations to perform:
  Apply all migrations: core
Running migrations:
  Applying core.0002_trans... OK
```