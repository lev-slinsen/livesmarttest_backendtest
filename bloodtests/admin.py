from django.contrib import admin

from .models import Test


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'unit', 'upper', 'lower')
    fields = ('code', 'name', 'unit', 'upper', 'lower', 'ideal_range')
    readonly_fields = ('id', 'ideal_range')

    def __str__(self):
        return self.code
