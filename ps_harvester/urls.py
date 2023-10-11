from django.urls import path

from ps_harvester import views

app_name = 'ps_harvester'

urlpatterns = [
    path('', view=views.Harvester.as_view(), name='harvester'),
    path('file', view=views.file_harvester, name='file_harvester'),
    path('web_harvester', view=views.web_harvester, name='web_harvester'),
    path('resolve/<int:pk>', view=views.resolve_entry, name='resolve_entry'),
    path('delete/<int:pk>', view=views.delete_entry, name='delete_entry'),
]
