
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os 
from . import views

urlpatterns = [
#    path('fileserver/', include([ 
#            path('uploadview/', views.IndexView.as_view()),
#            path('upload/', views.file_upload),
#            path('list/', views.LogFileListView.as_view(http_method_names=['post','get'])),
#        ] + static_urls #+ static('/static/', document_root=static_root) + static('/madia/', document_root=media_root)
#        )),
    path('', views.IndexView.as_view()),
    path('list/', views.LogFileListView.as_view(http_method_names=['post','get'])),
    path('upload/', views.file_upload),
    path('admin/', admin.site.urls),
]
