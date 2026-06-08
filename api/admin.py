from django.contrib import admin
from .models import User, Item, Invoice, InvoiceItem


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_users']

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)
    approve_users.short_description = "Approve selected users"


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'hsn_sac', 'price', 'user')


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


# class InvoiceAdmin(admin.ModelAdmin):
#     list_display = ('customer_name', 'email', 'phone', 'date', 'user')
#     inlines = [InvoiceItemInline]
from django.contrib import admin
from .models import Invoice

class InvoiceAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False  # ❌ disables delete button

# admin.site.register(Invoice, InvoiceAdmin)


admin.site.register(User, UserAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItem)


# Optional UI customization
admin.site.site_header = "Invoice Admin Panel"
admin.site.site_title = "Invoice Dashboard"
admin.site.index_title = "Welcome Admin"