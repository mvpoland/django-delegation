from .models import DelegatedView

from django.contrib import admin


class DelegatedViewAdmin(admin.ModelAdmin):
    raw_id_fields = ('owner',)

admin.site.register(DelegatedView, DelegatedViewAdmin)
