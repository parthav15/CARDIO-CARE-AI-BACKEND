from django.urls import path
from cardio import views

urlpatterns = [
    path('predict/', views.predict, name='predict'),
]