from django.urls import path
from . import views

app_name = "wamtram2"


urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("turtles/", views.TurtleListView.as_view(), name="turtle_list"),
    path("turtles/<int:pk>/", views.TurtleDetailView.as_view(), name="turtle_detail"),
    path("new-data-entry/<int:batch_id>/", views.TrtDataEntryFormView.as_view(), name="newtrtdataentry"),
    path("new-data-entry/<int:batch_id>/<int:turtle_id>/", views.TrtDataEntryFormView.as_view(), name="existingtrtdataentry"),
    path("data-entry/<int:entry_id>/", views.TrtDataEntryFormView.as_view(), name="trtdataentry"),
    path("find-tagged-turtle/<int:batch_id>/", views.FindTurtleView.as_view(), name="find_turtle"),
    path("entry-batches/", views.EntryBatchesListView.as_view(), name="entry_batches"),
    path("entry-batches/<int:batch_id>/", views.EntryBatchDetailView.as_view(), name="entry_batch_detail"),
    path("delete-entry/<int:pk>/<int:batch_id>/", views.DeleteEntryView.as_view(), name="delete_entry"),
    path("new-entry-batch/", views.EntryBatchDetailView.as_view(), name="new_batch_detail"),
    path("delete-batch/<int:batch_id>/", views.DeleteBatchView.as_view(), name="delete_batch"),
    path("validate-data-entry-batch/<int:batch_id>/", views.ValidateDataEntryBatchView.as_view(), name="validate_data_entry_batch"),
    path("process-data-entry-batch/<int:batch_id>/", views.ProcessDataEntryBatchView.as_view(), name="process_data_entry_batch"),
    path("observations/<int:pk>/", views.ObservationDetailView.as_view(), name="observationdetail"),
    path('validate-tag/', views.ValidateTagView.as_view(), name='validate_tag'),
    path("templates-manage/", views.TemplateManageView.as_view(), name="template_manage"),
    path("templates-manage/<str:template_key>/", views.TemplateManageView.as_view(), name="template_manage_key"),
    path('templates-manage/get-places/', views.TemplateManageView.as_view(), name='get_places'),
]
