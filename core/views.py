from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.http import HttpResponse, JsonResponse
from .models import Image, Trans
# Create your views here.

class Index(TemplateView):
    template_name='index.html'

def file_upload(request):
    # print(request.FILES)
    if request.method == 'POST':
        my_file=request.FILES.get('file')
        Image.objects.create(image=my_file)
        Trans.objects.create(col1="1", col2="2")
        return HttpResponse('')
    return JsonResponse({'post':'fasle'})

class FileList(ListView):
    model = Image
    paginate_by = 100  # if pagination is desired
    template_name='fielist.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['now'] = timezone.now()
        return context 