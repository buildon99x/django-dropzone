from django.db import connection
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.http import HttpResponse, JsonResponse
from .models import LogFile
from datetime import datetime
import django_tables2 as tables
import django_filters
#from  django_filters.widgets import RangeWidget
#from django_filters.widgets import RangeFilter
from django_filters.views import FilterView

def get_basedir(filename):
    # Create your models here.
    now = datetime.now()    
    basedir = filename[0:8]
    return 'playlog/'+basedir 

def common_response(rescode=0, msg="", data=None, status=None):
    res = {'rescode':rescode, 'msg':msg}
    if (data):
        res["data"]  = data
        
    if (status is None):
        return JsonResponse({'rescode':rescode, 'msg':msg, 'data':data})
    else:
        return JsonResponse({'rescode':rescode, 'msg':msg, 'data':data}, status=status)

def file_upload(request):
    ''' 업로드된 파일을 처리/저장하는 함수 
    '''
    # print(request.FILES)
    print("file_upload")
    if request.method == 'POST':
        my_file=request.FILES.get('file')
        tags_in=request.POST.get('tags_in')
        client_ip = request.META['REMOTE_ADDR']
        print(f"Uploaded files : {my_file.name} ({my_file.size})")
        print(tags_in)
        basedir = get_basedir(my_file.name)
        fileexists = LogFile.objects.filter(file=basedir+"/"+my_file.name).exists() 
        save_file = basedir+"/"+my_file.name
        #print(connection.queries)
        #print( fileexists )
        if (not fileexists):
            print(basedir)
            
            LogFile.objects.create(file=my_file, tags=tags_in, file_size=my_file.size, udt_ip=client_ip)
            #return HttpResponse(f'Success. {my_file.name} saved.!')
            msg = f'Success. {my_file.name} --> {save_file} saved.!'
            return common_response(0, msg)
        else:
            msg = f"Duplicate file-name. ({save_file})"
            return common_response(-1001, msg, status=400)
    return common_response(-1002, 'Invailid request. only POST', status=400)

class LogFileTable(tables.Table):
    ''' LogFileListView 에서 파일 리스트 테이블 클래스
    '''
    table_pagination = True

    file_size = tables.Column(accessor='get_file_size_kb', verbose_name='Size(KB)', attrs={ "td": {"style": "text-align:right"} })
    udt  = tables.DateTimeColumn(format ='Y-m-d h:i:s', verbose_name='Time')
    udt_ip = tables.Column(verbose_name='IP Addr')
    class Meta:
        attrs = {'class': 'paleblue'}
        fields = ["id", "file", "file_size", "udt_ip", "udt", "tags"]
        model = LogFile

class LogFileFiter(django_filters.FilterSet):
    ''' LogFileListView 에서 파일 리스트 필터(검색) 클래스
    '''
    #udt = django_filters.NumberFilter(field_name='udt', lookup_expr='udt')
    #udt__gt = django_filters.NumberFilter(field_name='udt', lookup_expr='udt__gt')
    #udt__lt = django_filters.NumberFilter(field_name='udt', lookup_expr='udt__lt')
    
    # django_filters.CharFilter는 django.form.fields.Field가 최상위 객체
    # https://github.com/django/django/blob/main/django/forms/fields.py
    # 
    # https://github.com/carltongibson/django-filter/blob/2c81768188cd4ce65d5fd20919ea4a8b2b5f214b/django_filters/fields.py
    file_in = django_filters.CharFilter(field_name='file', label="File", lookup_expr='contains', initial="")
    tags_in = django_filters.CharFilter(field_name='tags', label="Tags", lookup_expr='contains', initial="")
    #udt_in = django_filters.DateFromToRangeFilter(field_name='udt', label="Time", initial="")
    #file_in.form.value=""
    #tags_in.form.value=""
    #file_in.field.widget = forms.TextInput(attrs={'class': 'form-control'})
    #udt  = django_filters.RangeFilter(field_name='udt', widget=CustomDateRangeWidget) #, widget=RangeWidget(attrs={'placeholder': 'YYYY/MM/DD'})
    #utd_ip__name = django_filters.CharFilter(field_name='utd_ip', lookup_expr='contains')
    class Meta:
        model = LogFile
        #fields = {
        #    'file': ['contains'],
        #}
        exclude = ['file']
        fields = ['tags']

class LogFileListView(FilterView, tables.SingleTableView):
    ''' /fs/list : 파일 리스트 뷰 클래스
    '''
    table_class = LogFileTable
    filterset_class = LogFileFiter
    #queryset = LogFile.objects.all().order_by('-udt') #Vehicles.objects.filter(makename__icontains='make')
    template_name = 'filelist.html'
    table_pagination = {"per_page": 20}
    fields = ('id', 'file', 'tags', 'udt_ip', 'udt')
    def get_queryset(self):
        # udt DESC 정렬 실행.
        return LogFile.objects.all().order_by('-udt') 
        #page = self.request.GET.get("page")
        #keyword = "" #self.request.GET.get("keyword")
        #print(f"page:{page}")
        #return LogFile.objects.all().order_by('-udt') 
        #if ( keyword==""):
        #    return LogFile.objects.all().order_by('-udt') 
        #else:
        #    return LogFile.objects.filter(file__contains=keyword).order_by('-udt') 
    
    '''
    def get_queryset(self):
        make = self.request.GET.get('make')
        results = LogFile.objects.all().order_by('-udt') #Vehicles.objects.filter(makename__icontains='make')
        print (connection.queries)
        context = {'results': results}
        return render(self.request, self.template_name, context)
    '''

''' 미사용.
from django import forms
class FileUploadForm(forms.Form):
    file = forms.FileField(required=True)
    tags_in = forms.CharField(max_length=50, initial="test")
'''
class IndexView(tables.SingleTableView):
    ''' /fs : 파일 관리자 메인 화면 ( 업로드 & List )
    '''
    table_class = LogFileTable
    template_name='index.html'
    model = LogFile
    #form = FileUploadForm()