https://github.com/nicksonlangat/django-dropzone



pip install django-tables2
pip install django


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

# 서버 구동

### static 파일 수집 
```bash
python manage.py collectstatic
```

### 서버 시작
```bash
python runserver.py
```


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
* [bootstrap](https://getbootstrap.com/docs/5.0/forms/layout/)