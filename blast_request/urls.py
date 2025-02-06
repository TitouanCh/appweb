from django.urls import path
from . import views

urlpatterns = [
    path('', views.blast_request_view, name='blast_request_home'),  # 🔹 Rend accessible la bonne page dès l'accès
    path('blast_request/', views.blast_request_view, name='blast_request'),
]

# go directly to 127.0.0.1:8000/blast_request/databases/ because the page blast_request/ only doesn't coded for the moment
