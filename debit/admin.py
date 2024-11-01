from django.contrib import admin

from debit.models import DebitModel


@admin.register(DebitModel)
class DebitModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', 'amount', 'description', 'date_created', 'loan_type', 'is_closed')
    list_filter = ('is_closed',)
