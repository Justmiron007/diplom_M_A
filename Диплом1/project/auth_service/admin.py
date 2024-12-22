from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_at')
    readonly_fields = ('created_at',)
    list_filter = ('created_at',)
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        ('Important Dates', {'fields': ('created_at',)}),
    )

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
