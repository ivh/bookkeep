from bkweb.bk.models import Account,Transaction,Booking
from django.contrib import admin

class BookingInline(admin.StackedInline):
    model = Booking
    extra = 5

class TransactionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['description']}),
        (None, {'fields': ['date']}),
    ]
    inlines = [BookingInline]
    list_display=('description','date')
    list_filter = ['date']
    search_fields = ['description']
    date_hierarchy = 'date'

class BookingAdmin(admin.ModelAdmin):
    list_display=('trans','debit','credit','value')

admin.site.register(Transaction,TransactionAdmin)
admin.site.register(Account)
admin.site.register(Booking,BookingAdmin)
