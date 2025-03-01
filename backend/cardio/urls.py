from django.urls import path
from cardio import views

urlpatterns = [
    path('predict/', views.predict, name='predict'),
    path('find_nearby_hospitals/', views.find_nearby_hospitals, name='find_nearby_hospitals'),
]