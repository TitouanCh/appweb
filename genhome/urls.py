from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('annotate/<int:sequence_id>/', views.annotate_sequence, name='annotate_sequence'),
]
