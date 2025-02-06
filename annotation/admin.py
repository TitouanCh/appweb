from django.contrib import admin
from .models import Annotation
from genhome.models import FaSequence


# Register your models here.
@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('id', 'sequence', 'owner', 'created_at')
    list_filter = ('sequence', 'owner', 'created_at')
    search_fields = ('content',)
