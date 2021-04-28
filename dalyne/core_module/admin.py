from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core_module.models import User,Company, Profile, Plans,\
    UserPlans, CountryMaster, CurrencyMaster, ImportTable

admin.site.site_header = 'eximine superAdmin Dashboard'

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = [
        'id', 'email', 'name', 'is_active', 'is_superuser', 
        'is_staff', 'last_login']
    search_fields = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('personal Info'), {'fields': ('name',)}),
        (
            _('permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(User, UserAdmin)

@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = [
        field.name for field in Profile._meta.fields
        ]
@admin.register(Company)
class Company(admin.ModelAdmin):
    list_display = [
        field.name for field in Company._meta.fields
        ]

@admin.register(Plans)
class Plans(admin.ModelAdmin):
    list_display = [
        field.name for field in Plans._meta.fields
        ]

@admin.register(UserPlans)
class UserPlans(admin.ModelAdmin):
    list_display = [
        field.name for field in UserPlans._meta.fields
        ]

@admin.register(CountryMaster)
class CountryMaster(admin.ModelAdmin):
    list_display = [
        field.name for field in CountryMaster._meta.fields
        ]

@admin.register(CurrencyMaster)
class CurrencyMaster(admin.ModelAdmin):
    list_display = [
        field.name for field in CurrencyMaster._meta.fields
        ]

@admin.register(ImportTable)
class ImportTable(admin.ModelAdmin):
    list_display = [
        field.name for field in ImportTable._meta.fields
        ]