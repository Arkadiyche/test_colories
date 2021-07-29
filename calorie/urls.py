from rest_framework import routers
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('activity/', views.ActivityView.as_view()),
    path('activity/', views.ActivityView.as_view()),
    path('dish/', views.DishView.as_view()),
    path('action/activity/', views.ActivityActionView.as_view()),
    path('action/dish/', views.DishActionView.as_view()),
    path('stat/', views.get_stats, name='get_stats'),
    path('calories/', views.get_person_calories, name='get_person_calories'),
]