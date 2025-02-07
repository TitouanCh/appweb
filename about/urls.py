from django.urls import path
from .views import about_view

urlpatterns = [
    # Autres chemins
    path('about/', about_view, name='about'),
]
