from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('change_pass/', views.change_pass, name='change_pass'),
    path('signup/', views.signup, name="signup"),
    path('patients/', views.patients, name='patients'),
    path('patients/details/<int:id>', views.details, name='details'),
    path('patients/details/<int:id>/exams', views.exams, name='exams'),
    path('patients/details/<int:id>/new_measurement', views.new_measurement, name='new_measurement'),
    path('testing/', views.testing, name='testing')
]
