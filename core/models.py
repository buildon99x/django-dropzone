''' core 패키지(어플리케이션)의 db모델 정의하는 모듈
'''
from csv import field_size_limit
from django.db import models
from datetime import datetime
import os

def get_upload_path(instance, filename):
    basedir = get_basedir(filename)
    return os.path.join(f"{basedir}" , filename)

def get_basedir(filename):
    # Create your models here.
    now = datetime.now()    
    basedir = filename[0:8]
    #print (basedir.isdigit())
    if basedir.isdigit():
        return 'playlog/'+basedir 
    else:
        return 'playlog/_etc'

class LogFile(models.Model):
    id          = models.BigAutoField   ( primary_key=True )
    file        = models.FileField      ( upload_to=get_upload_path, db_index=True )
    file_size   = models.IntegerField   ( default=0 )
    tags        = models.CharField      ( max_length=100, db_index=True, blank=True )
    udt_ip      = models.CharField      ( max_length=15 )
    udt         = models.DateTimeField  ('udt', auto_now=True )

    def get_file_size_kb(self):
        return int(self.file_size/1024)
        
    def __str__(self):
        ''' admin Log files 리스트에 출력되는 포맷을 정의한다.
        '''
        return f"{str(self.pk)} : {self.file} ({int(self.file_size/1024)}kb) | {self.udt:%Y-%m-%D %H:%M:%S} | {self.tags}"
