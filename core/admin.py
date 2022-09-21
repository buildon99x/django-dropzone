from django.contrib import admin
from .models import LogFile

class LogFileAdmin(admin.ModelAdmin):
    ''' LogFile  Model의 커스텀  admin 클래스

        참고문서 : 
        * https://www.geeksforgeeks.org/django-admin-redesign-and-customization/
        * https://velog.io/@qlgks1/Django-admin-custom
    '''
    search_fields   = ['id', 'file', 'tags']
    list_display    = ['id', 'file', 'file_size', 'udt', 'tags']
    list_filter     = ['udt', 'tags']
    #editable_list   = ['tags']

# Register your models here.
admin.site.register(LogFile, LogFileAdmin)
#admin.site.register(Trans)
