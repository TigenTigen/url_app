from django.contrib import admin
from core.models import URL

class URLAdmin(admin.ModelAdmin):
    list_display = ['path', 'added', 'total_timeshift', 'requested', 'result',]
    list_display_links = ['path',]
    search_fields = ['path',]
    fields = ['path', ('timeshift_in_minutes', 'timeshift_in_seconds',), 'added', 'requested', 'result', 'encoding', 'title', 'h1_content',]
    readonly_fields= ['added', 'requested', 'result', 'encoding', 'title', 'h1_content',]

admin.site.register(URL, URLAdmin)
