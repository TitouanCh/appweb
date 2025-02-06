from django.contrib import admin
from blast_request.models import BioDatabase

@admin.register(BioDatabase)
class BioDatabaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'blastn_url', 'blastp_url')
    list_filter = ('name',)
