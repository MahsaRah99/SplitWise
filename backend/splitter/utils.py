from collections import defaultdict

from django.contrib.auth import get_user_model
from django.db.models import Sum

from .models import ParticipantExpense

User = get_user_model()


def get_total_owed_to_payer(group, payer):
    User = get_user_model()

    totals = (
        ParticipantExpense.objects.filter(
            expense__group=group,
            expense__payer=payer,
            is_paid=False,
        )
        .values("user")
        .annotate(total_owed=Sum("amount_owed"))
    )

    user_ids = [entry["user"] for entry in totals]
    user_map = {user.id: user.username for user in User.objects.filter(id__in=user_ids)}

    result = {
        user_map.get(entry["user"], "Unknown"): entry["total_owed"] for entry in totals
    }

    return result


def simplify_transactions(group):
    net_balances = defaultdict(int)

    credited = (
        ParticipantExpense.objects.filter(expense__group=group, is_paid=False)
        .values("expense__payer")
        .annotate(total_paid=Sum("amount_owed"))
    )

    for entry in credited:
        payer_id = entry["expense__payer"]
        net_balances[payer_id] += entry["total_paid"]

    owed = (
        ParticipantExpense.objects.filter(expense__group=group, is_paid=False)
        .values("user")
        .annotate(total_owed=Sum("amount_owed"))
    )

    for entry in owed:
        user_id = entry["user"]
        net_balances[user_id] -= entry["total_owed"]

    user_map = {
        user.id: user.username
        for user in User.objects.filter(id__in=net_balances.keys())
    }
    return simplify_debts_with_names(net_balances, user_map)


def simplify_debts_with_names(net_balances, user_map):
    creditors = [
        (user, balance) for user, balance in net_balances.items() if balance > 0
    ]
    debtors = [(user, balance) for user, balance in net_balances.items() if balance < 0]

    transactions = []

    while creditors and debtors:
        creditor, credit_balance = creditors.pop()
        debtor, debt_balance = debtors.pop()

        transfer_amount = min(credit_balance, -debt_balance)

        transactions.append([user_map[debtor], user_map[creditor], transfer_amount])

        credit_balance -= transfer_amount
        debt_balance += transfer_amount

        if credit_balance > 0:
            creditors.append((creditor, credit_balance))
        if debt_balance < 0:
            debtors.append((debtor, debt_balance))

    return transactions
