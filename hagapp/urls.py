from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('create-experiment/', views.create_experiment, name='create_experiment'),
    path('experiment-list/', views.experiment_list, name='experiment_list'),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('process-csv/<int:experiment_id>/<str:csv_path>/<str:threshold>/', views.process_csv, name='process_csv'),
    path('signal-data-list/', views.signal_data_list, name='signal_data_list'),
]
