from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core_module.models import User, Profile, Plans, \
    UserPlans, CountryMaster, CurrencyMaster, ImportTable, \
    ExportTable, ProductMaster, CompanyMaster, Tenant, MailTemplate, FilterDataModel

admin.site.site_header = 'dalyne superAdmin Dashboard'


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


@admin.register(Tenant)
class Tenant(admin.ModelAdmin):
    list_display = [
        field.name for field in Tenant._meta.fields
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
    search_fields = ('IMPORTER_NAME', 'EXPORTER_NAME')


# @admin.register(ImportRawTable)
# class ImportRawTable(admin.ModelAdmin):
#     list_display = [
#         field.name for field in ImportRawTable._meta.fields
#     ]
    

# @admin.register(ExportRawTable)
# class ExportRawTable(admin.ModelAdmin):
#     list_display = [
#         field.name for field in ExportRawTable._meta.fields
#     ]

@admin.register(ExportTable)
class ExportTable(admin.ModelAdmin):
    list_display = [
        field.name for field in ExportTable._meta.fields
    ]
    search_fields = ('IMPORTER_NAME', 'EXPORTER_NAME')


@admin.register(ProductMaster)
class ProductMaster(admin.ModelAdmin):
    list_display = [
        field.name for field in ProductMaster._meta.fields
    ]
    search_fields = ('hs_code',)


@admin.register(CompanyMaster)
class CompanyMaster(admin.ModelAdmin):
    list_display = [
        field.name for field in CompanyMaster._meta.fields
    ]
    search_fields = ('name',)


@admin.register(MailTemplate)
class MailTemplate(admin.ModelAdmin):
    list_display = [
        field.name for field in MailTemplate._meta.fields
    ]


@admin.register(FilterDataModel)
class FilterDataModel(admin.ModelAdmin):
    list_display = [
        field.name for field in FilterDataModel._meta.fields
    ]

