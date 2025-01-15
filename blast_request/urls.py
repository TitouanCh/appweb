from django.urls import path
from . import views

urlpatterns = [
    path('databases/', views.database_list, name='database_list'),
]
