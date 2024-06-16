from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('change_pass/', views.change_pass, name='change_pass'),
    path('signup/', views.signup, name="signup"),
    path('patients/', views.patients, name='patients'),
    path('patients/details/<int:id>/', views.details, name='details'),
    path('patients/details/<int:id>/exams', views.exams, name='exams'),
    path('patients/details/<int:id>/exams/del_measurement/<int:measurement_id>', views.del_measurement, name='del_measurement'),
    path('patients/details/<int:id>/exams/edit_measurement/<int:measurement_id>', views.edit_measurement, name='edit_measurement'),
    path('patients/details/<int:id>/exams/download', views.download_exams, name='down_exams'),
    path('patients/details/<int:id>/new_measurement', views.new_measurement, name='new_measurement'),
    path('patients/details/<int:id>/measurements_csv', views.measurements_csv, name='measurements_csv'),
    path('patients/details/<int:id>/measurements_csv/download', views.download_template, name='down_template'),
    path('patients/details/<int:id>/new_measure', views.new_measure, name='new_measure'),
    path('patients/details/<int:id>/edit_measure', views.edit_measure, name='edit_measure'),
    path('patients/details/<int:id>/delete_measure', views.delete_measure, name='delete_measure'),
    path('patients/details/<int:id>/select_measure', views.select_measure, name='select_measure'),
    path('patients/details/<int:id>/plot_graph', views.plot_graph, name='plot_graph'),
    path('testing/', views.testing, name='testing')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


