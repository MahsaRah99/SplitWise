from uuid import uuid4

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Group(models.Model):
    name = models.CharField(_("Name"), max_length=300)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    invite_token = models.UUIDField(_("Invite Token"), default=uuid4, unique=True)

    @property
    def invite_link(self):
        return f"{settings.SITE_URL}/group/join/{self.invite_token}/"

    def __str__(self):
        return self.name


class Expense(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    description = models.CharField(_("Description"), max_length=600)
    amount = models.IntegerField(_("Amount"), validators=[MinValueValidator(1000)])
    payer = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="payments", on_delete=models.PROTECT
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="ParticipantExpense", related_name="expenses"
    )
    date = models.DateField(_("Date"))

    def __str__(self):
        return self.description[:20]


class ParticipantExpense(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount_owed = models.IntegerField(_("Amount Owed"))
    is_paid = models.BooleanField(_("Is Paid"), default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "expense"], name="unique_userexpense"
            )
        ]
