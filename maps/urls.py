from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='site-home'),
    path('survey/', views.survey, name='site-survey'),
    path('loading/', views.loading, name='site-loading'),
    path('display/', views.display, name='site-display'),
    path('about/', views.about, name='site-about'),
    path('error/', views.error, name='site-error'),
]
