from django.urls import path
from . import views
urlpatterns = [
    path('', views.Index.as_view()),
    path('filelist/', views.FileList.as_view()),
    path('upload/', views.file_upload),
]  