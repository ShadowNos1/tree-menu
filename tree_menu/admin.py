from django.contrib import admin
from .models import Menu, MenuItem

# Регистрация моделей в панели администратора.
# `Menu` отображается с inline-списком `MenuItem` для удобного редактирования.

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 0
    fields = ("title", "parent", "url", "named_url", "order", "new_tab")

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = (MenuItemInline,)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("title", "menu", "parent", "order", "url", "named_url")
    list_filter = ("menu",)
    ordering = ("menu", "parent__id", "order")
    search_fields = ("title", "url", "named_url")
