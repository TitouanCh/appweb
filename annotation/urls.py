from django.urls import include, path
from . import views

urlpatterns = [
    path('annotate/<int:sequence_id>/', views.annotate_sequence, name='annotate_sequence'),
    path('view/<int:sequence_id>/', views.simple_view, name='simple_view'),
    path('annotation/delete/<int:annotation_id>/', views.delete_annotation, name='delete_annotation'),
    path('add-sequence/', views.add_sequence, name='add_sequence'),
    path('delete-all-sequences/', views.delete_all_sequences, name='delete_all_sequences'),

]