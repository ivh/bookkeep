from bkweb.bk.models import Account,Transaction,Booking
from django.contrib import admin

class BookingInline(admin.TabularInline):
    model = Booking
    extra = 10

class TransactionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['description','date']}),
        #(None, {'fields': ['date']}),
    ]
    inlines = [BookingInline]
    list_display=('id','description','date','isbalanced')
    list_filter = ['date']
    search_fields = ['description']
    date_hierarchy = 'date'
    ordering = ['id']
    
    def save_model(self, request, obj, form, change):
        if obj.isbalanced(): obj.save()
        

class BookingAdmin(admin.ModelAdmin):
    list_display=('trans','acc','debit','credit')
    ordering = ['trans']

class AccountAdmin(admin.ModelAdmin):
    list_display=('accno','debinc','description','balance')
    search_fields = ['description']
    ordering = ['accno']

admin.site.register(Transaction,TransactionAdmin)
admin.site.register(Account,AccountAdmin)
admin.site.register(Booking,BookingAdmin)
