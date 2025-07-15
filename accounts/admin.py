from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

class CustomUserAdmin(UserAdmin):
    model = get_user_model()
    list_display = ('phone','email','is_staff','phone_verified')
    ordering = ('phone',)
    list_filter = ('phone_verified','is_staff', 'is_active')
    search_fields = ('phone','email')
    fieldsets = (
        ('Critical Information', {'fields':('phone','phone_verified','password','email')}),
        ('Permissions', {'fields':('is_active','is_staff','groups','user_permissions')}),
        ('History', {'fields':('phone_history',)}),
    )
    add_fieldsets = (
        (None,{
            'classes': ('wide',),
            'fields':('phone','password1','password2','is_staff','is_active'),
        }),
    )
    readonly_fields = ('phone_history',)
admin.site.register(CustomUser, CustomUserAdmin)


admin.site.site_header = 'Allauth Administration'
admin.site.site_title = 'Allauth'
admin.site.index_title = 'Administration'
# admin.site.register(CustomUser)