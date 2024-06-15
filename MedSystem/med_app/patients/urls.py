from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('change_pass/', views.change_pass, name='change_pass'),
    path('signup/', views.signup, name="signup"),
    path('patients/', views.patients, name='patients'),
    path('patients/details/<int:id>', views.details, name='details'),
    path('patients/details/<int:id>/exams', views.exams, name='exams'),
    path('patients/details/<int:id>/exams/download', views.download_exams, name='down_exams'),
    path('patients/details/<int:id>/new_measurement', views.new_measurement, name='new_measurement'),
    path('patients/details/<int:id>/new_measure', views.new_measure, name='new_measure'),
    path('patients/details/<int:id>/edit_measure', views.edit_measure, name='edit_measure'),
    path('testing/', views.testing, name='testing')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


