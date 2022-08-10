from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class UserAdmin(UserAdmin):
    list_display = ('pk','email','date_of_inactive','is_active','is_used','is_admin','is_headveterinarian','is_secretary','is_veterinarian','is_petowner','date_joined','last_login')
    search_fields = ('email',)
    readonly_fields = ('date_joined','last_login')
    ordering = ('pk',)
    filter_horizontal = ()
    list_filter = ('is_active','is_admin','is_headveterinarian','is_secretary','is_veterinarian','is_petowner')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active','date_of_inactive','is_used','is_admin','is_headveterinarian','is_secretary','is_veterinarian','is_petowner')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','is_admin','is_headveterinarian','is_secretary','is_veterinarian','is_petowner'),
        }),
    )

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'image_tag', 'useracc','firstName','lastName')
    search_fields = ('pk','firstName','lastName',)
    ordering = ('lastName',)
    filter_horizontal = ()
    list_filter = ('firstName','lastName',)

class SecProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'image_tag','useracc','firstName','lastName')
    search_fields = ('pk','firstName','lastName',)
    ordering = ('lastName',)
    filter_horizontal = ()
    list_filter = ('firstName','lastName',)

class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('pk','species')
    search_fields = ('pk','species')
    ordering = ('pk',)
    filter_horizontal = ()
    list_filter = ('species',)

class PetAdmin(admin.ModelAdmin):
    list_display = ('pk', 'image_tag','petOwner','petName','dob')
    search_fields = ('pk','petOwner','petName','dob','sex','species','description','colorMarking')
    autocomplete_fields = ['petOwner']
    ordering = ('pk',)
    filter_horizontal = ()
    list_filter = ('species','is_deleted')

class VaccineTypeAdmin(admin.ModelAdmin):
    list_display = ('pk','vaccineType')
    search_fields = ('pk','vaccineType')
    ordering = ('pk',)
    filter_horizontal = ()
    list_filter = ('vaccineType',)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('pk','serviceName','description','price','is_labTest')
    search_fields = ('pk','serviceName','price')
    ordering = ('pk',)
    filter_horizontal = ()
    list_filter = ('is_labTest',)

class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('pk','product_name')
    search_fields = ('pk','product_name')
    ordering = ('pk',)
    filter_horizontal = ()
    list_filter = ('product_name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk','product','manuDate','expireDate','quantity')
    search_fields = ('pk','product','manuDate','expireDate','quantity')
    ordering = ('pk',)
    filter_horizontal = ()
    list_filter = ('product',)

class GenderAdmin(admin.ModelAdmin):
    list_display = ('pk','gender')
    search_fields = ('pk','gender')
    ordering = ('pk',)
    filter_horizontal = ()
    list_filter = ('gender',)

class ServiceHistoryAdmin(admin.ModelAdmin):
    list_display = ('pk','medHistory','dateofService','service','vet')
    search_fields = ('pk','service')
    ordering = ('pk',)
    filter_horizontal = ()
    list_filter = ('service',)

class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('pk','pet','date','vet')
    search_fields = ('pk','pet')
    ordering = ('pk',)
    filter_horizontal = ()
    list_filter = ('pet','vet',)

class ServiceInvoiceAdmin(admin.ModelAdmin):
    list_display = ('pk','chargeslip','date','service','total')
    search_fields = ('pk','service')
    ordering = ('pk',)
    filter_horizontal = ()
    list_filter = ('service',)

admin.site.register(User,UserAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(StaffProfile,SecProfileAdmin)
admin.site.register(petspecies,SpeciesAdmin)
admin.site.register(pets,PetAdmin)
admin.site.register(vaxType,VaccineTypeAdmin)
admin.site.register(services,ServiceAdmin)
admin.site.register(ProductInfo,ProductInfoAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Gender,GenderAdmin)
admin.site.register(MedicalHistory,MedicalHistoryAdmin)
admin.site.register(serviceHistory,ServiceHistoryAdmin)
admin.site.register(labHistory)
admin.site.register(ProductType)
admin.site.register(vaccineHistory)
admin.site.register(chargeSlip)
admin.site.register(productInvoice)
admin.site.register(serviceInvoice,ServiceInvoiceAdmin)
admin.site.register(transaction)
admin.site.register(breed)
admin.site.register(schedule_slot)
admin.site.register(scheduling)
admin.site.register(flagsystem)