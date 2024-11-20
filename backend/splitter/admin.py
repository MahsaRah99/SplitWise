from django.contrib import admin

from .models import Expense, Group, ParticipantExpense


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "invite_token")
    search_fields = ("name",)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("id", "group", "description", "payer", "amount")
    search_fields = ("description",)


@admin.register(ParticipantExpense)
class ParticipantExpenseAdmin(admin.ModelAdmin):
    list_display = ("id", "expense", "user", "amount_owed")
    list_filter = ("is_paid",)
