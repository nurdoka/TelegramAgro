from django.contrib import admin
from .models import Station, Message

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("name", "location")
    filter_horizontal = ("observers",)  # nicer UI for selecting observers

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("station", "observer", "text", "created_at")
    list_filter = ("station", "observer")
    search_fields = ("text",)
    readonly_fields = ("created_at",)
