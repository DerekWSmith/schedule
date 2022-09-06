from django.contrib import admin
from table.models import event


# Register your models here.

@admin.register(event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'end', 'get_duration' , 'location', 'notes')
    list_filter = ('start', 'end',)
    search_fields = ('name', 'notes',)
    fields = ('name', 'notes', 'start', 'end','get_duration' ,  )
    readonly_fields = ('get_duration',)