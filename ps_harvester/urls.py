from django.urls import path

from ps_harvester import views


app_name = "ps_harvester"


urlpatterns = [
    path(
        "processes",
        view=views.HarvestProcessList.as_view(),
        name="process_list",
    ),
    path(
        "file-harvest",
        view=views.FileHarvester.as_view(),
        name="file_harvest",
    ),
    path(
        "process/<int:pk>",
        view=views.HarvestProcessDetail.as_view(),
        name="harvest_process",
    ),
    path(
        "process/<int:pk>/note",
        view=views.EditProcessNotes.as_view(),
        name="harvest_process_note",
    ),
    path(
        "process/<int:pk>/delete",
        view=views.DeleteHarvestProcess.as_view(),
        name="delete_process",
    ),
    path(
        "entry/<int:pk>/note",
        view=views.EditEntryNotes.as_view(),
        name="harvest_entry_note",
    ),
    path(
        "entry/<int:pk>/resolve",
        view=views.ResolveHarvestEntry.as_view(),
        name="resolve_entry",
    ),
    path(
        "entry/<int:pk>/unresolve",
        view=views.UnresolveHarvestEntry.as_view(),
        name="unresolve_entry",
    ),
    path(
        "entry/<int:pk>/delete",
        view=views.DeleteHarvestEntry.as_view(),
        name="delete_entry",
    ),
]
