from django.contrib import admin
from .models import FaSequence
from annotation.models import Annotation

@admin.register(FaSequence)
class FaSequenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'owner')
    list_filter = ('status', 'owner')
    search_fields = ('sequence',)

