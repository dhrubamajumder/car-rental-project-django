from django.contrib import admin
from .models import Booking, Payment


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car', 'start_date', 'end_date', 'grand_total', 'status', 'payment_status')
    list_filter = ('status', 'payment_status')
    search_fields = ('user__email', 'car__brand', 'car__model')


admin.site.register(Payment)
