from django.urls import path
from . import views

urlpatterns = [
    path('', views.blast_view, name='blast'),
    path('<int:sequence_id>/', views.blast_view, name='blast'),
]
