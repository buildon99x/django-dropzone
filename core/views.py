from django.db import connection
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.http import HttpResponse, JsonResponse
from .models import LogFile
from datetime import datetime
import django_tables2 as tables

# Create your views here.


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
    # print(request.FILES)
    print("file_upload")
    if request.method == 'POST':
        my_file=request.FILES.get('file')
        client_ip = request.META['REMOTE_ADDR']
        print(my_file.name)
        basedir = get_basedir(my_file.name)
        fileexists = LogFile.objects.filter(file=basedir+"/"+my_file.name).exists() 
        save_file = basedir+"/"+my_file.name
        #print(connection.queries)
        #print( fileexists )
        if (not fileexists):
            print(basedir)
            LogFile.objects.create(file=my_file, udt_ip=client_ip)
            #return HttpResponse(f'Success. {my_file.name} saved.!')
            msg = f'Success. {my_file.name} --> {save_file} saved.!'
            return common_response(0, msg)
        else:
            msg = f"Duplicate file-name. ({save_file})"
            return common_response(-1001, msg, status=400)
    return common_response(-1002, 'Invailid request. only POST', status=400)

class LogFileTable(tables.Table):
    table_pagination = True
    class Meta:
        attrs = {'class': 'paleblue'}
        model = LogFile

class LogFileListView(tables.SingleTableView):
    table_class = LogFileTable
    #queryset = LogFile.objects.all().order_by('-udt') #Vehicles.objects.filter(makename__icontains='make')
    template_name = 'filelist.html'
    table_pagination = {"per_page": 20}
    fields = ('id', 'file', 'tags', 'udt_ip', 'udt')
    def get_queryset(self):
        page = self.request.GET.get("page")
        keyword = "" #self.request.GET.get("keyword")
        print(f"page:{page}")
        #return LogFile.objects.all().order_by('-udt') 
        if ( keyword==""):
            return LogFile.objects.all().order_by('-udt') 
        else:
            return LogFile.objects.filter(file__contains=keyword).order_by('-udt') 
    
    '''
    def get_queryset(self):
        make = self.request.GET.get('make')
        results = LogFile.objects.all().order_by('-udt') #Vehicles.objects.filter(makename__icontains='make')
        print (connection.queries)
        context = {'results': results}
        return render(self.request, self.template_name, context)
    '''

class IndexView(tables.SingleTableView):
    table_class = LogFileTable
    queryset = LogFile.objects.all().order_by('-udt')
    template_name='index.html'
    model = LogFile
    table_pagination = {"per_page": 20}
    #paginate_by = 100  # if pagination is desired
    #ordering = ["-udt"]
    
