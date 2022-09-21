from csv import field_size_limit
from django.db import models
from datetime import datetime
import os

# Create your models here.
#now = datetime.now()
#today_dir = now.strftime("%Y%m%d")
#class Image(models.Model):
#    image=models.FileField(upload_to=f'playlog/{today_dir}')
#    udt = models.DateTimeField('udt', auto_now=True)
#    def __str__(self):
#        return str(self.pk)


def get_upload_path(instance, filename):
    return os.path.join(f"playlog/{filename[0:8]}" , filename)

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

#class Trans(models.Model):
#    col1 = models.TextField(max_length=20)
#    col2 = models.TextField(max_length=20)
#    def __str__(self):
#        return str(self.pk)
    