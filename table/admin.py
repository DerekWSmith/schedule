from django.contrib import admin
from table.models import event


# Register your models here.

@admin.register(event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'location', 'notes')
    list_filter = ('start_date', 'end_date',)
    search_fields = ('name', 'notes',)
    # fields = ('name', 'notes', 'start_date', 'end_date',  )
    # readonly_fields = ('get_duration',)