from django.contrib import admin
from .models import FaSequence, Annotation

@admin.register(FaSequence)
class FaSequenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'owner')
    list_filter = ('status', 'owner')
    search_fields = ('sequence',)

@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('id', 'sequence', 'owner', 'created_at')
    list_filter = ('sequence', 'owner', 'created_at')
    search_fields = ('content',)
