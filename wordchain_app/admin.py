from django.contrib import admin
from .models import Chain, Level, IsAssignedTo, Display


class IsAssignedToInline(admin.TabularInline):
    model = IsAssignedTo
    extra = 1


class ModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super().__init__(model, admin_site)


class ChainAdmin(ModelAdmin):
    inlines = [
        IsAssignedToInline,
    ]


admin.site.register(Chain, ChainAdmin)
admin.site.register(Level, ModelAdmin)
admin.site.register(Display, ModelAdmin)




