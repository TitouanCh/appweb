from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('annotate/<int:sequence_id>/', views.annotate_sequence, name='annotate_sequence'),

    path('search/', views.search_sequences, name='search_sequences'),
    path('detail/<int:id>/', views.view_detail, name='view_detail'),
]
