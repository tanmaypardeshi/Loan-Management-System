from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Loan


class LoanHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['user', 'granted_by', 'principal', 'interest', 'months', 'amount', 'emi', 'status',
                    'start_date', 'end_date', 'modified_date']
    history_list_display = ['id', 'user', 'granted_by', 'principal', 'interest', 'months', 'amount', 'emi', 'status',
                            'start_date', 'end_date', 'modified_date']
    search_fields = ['user']


admin.site.register(Loan, LoanHistoryAdmin)
