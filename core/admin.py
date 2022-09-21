from django.contrib import admin
from .models import LogFile

class LogFileAdmin(admin.ModelAdmin):
    ''' LogFile  Model의 커스텀  admin 클래스
    '''
    search_fields   = ['id', 'file', 'tags']
    list_display    = ['id', 'file', 'file_size', 'udt', 'tags']
    editable_list   = ['tags']

# Register your models here.
admin.site.register(LogFile, LogFileAdmin)
#admin.site.register(Trans)
