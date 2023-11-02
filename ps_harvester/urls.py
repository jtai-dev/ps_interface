from django.urls import path

from ps_harvester import views


app_name = 'ps_harvester'


urlpatterns = [
    path('', view=views.HarvestProcessView.as_view(), name='harvester'),
    path('file', view=views.FileHarvester.as_view(), name='file_harvester'),
    path('web', view=views.web_harvester, name='web_harvester'),
    path('process/<int:pk>/note', view=views.EditProcessNotes.as_view(), name='harvest_process_note'),
    path('entry/<int:pk>/note', view=views.EditEntryNotes.as_view(), name='harvest_entry_note'),
    path('entry/resolve/<int:pk>', view=views.ResolveHarvestEntry.as_view(), name='resolve_entry'),
    path('entry/delete/<int:pk>', view=views.DeleteHarvestEntry.as_view(), name='delete_entry'),
]
