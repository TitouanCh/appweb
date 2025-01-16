from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.search_sequences, name='search_sequences'),
    path('detail/<int:id>/', views.view_detail, name='view_detail')
]
