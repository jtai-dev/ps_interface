from django.urls import path

from ps_harvester import views

app_name = 'ps_harvester'

urlpatterns = [
    path('', view=views.harvester, name='harvester'),
    path('file', view=views.file_harvester, name='file_harvester'),
    path('web_harvester', view=views.web_harvester, name='web_harvester')
]
