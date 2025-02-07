from django.urls import path
from search.views import search_sequences

urlpatterns = [
    path('search/', search_sequences, name='search_sequences'),
]
