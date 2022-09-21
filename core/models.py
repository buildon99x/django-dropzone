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
    file        = models.FileField( upload_to=get_upload_path )
    tags        = models.CharField( max_length=100 )
    udt_ip      = models.CharField( max_length=15 )
    udt         = models.DateTimeField('udt', auto_now=True)
    def __str__(self):
        return str(self.pk)

#class Trans(models.Model):
#    col1 = models.TextField(max_length=20)
#    col2 = models.TextField(max_length=20)
#    def __str__(self):
#        return str(self.pk)
    