from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Account(models.Model):
    """
    Account model.
    """

    number = models.AutoField(primary_key=True)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    """
    Transaction model.
    """

    class TransactionType(models.TextChoices):
        CREDIT = "credit"
        DEBIT = "debit"

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=6, choices=TransactionType.choices)
    note = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BalanceHistory(models.Model):
    """
    Balance history model.
    """

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)


@receiver(post_save, sender=Account)
def create_balance_history(sender, instance, created, **kwargs):
    """
    Create balance history when account is created or if it is
    the first update of the day. If it is not the first
    transaction of the day, update balance history with
    the new balance.
    """

    if created:
        BalanceHistory.objects.create(
            account=instance, balance=instance.current_balance
        )
    else:
        balance_history = (
            BalanceHistory.objects.filter(account=instance)
            .order_by("-created_at")
            .first()
        )
        if balance_history.created_at.date() != instance.updated_at.date():
            BalanceHistory.objects.create(
                account=instance, balance=instance.current_balance
            )
        else:
            balance_history.balance = instance.current_balance
            balance_history.save()


@receiver(post_save, sender=Transaction)
def update_account_balance(sender, instance, created, **kwargs):
    """
    Update account balance after transaction
    """
    if created:
        # Update account balance
        if instance.type == Transaction.TransactionType.CREDIT:
            instance.account.current_balance += instance.amount
        elif instance.type == Transaction.TransactionType.DEBIT:
            instance.account.current_balance -= instance.amount
        else:
            raise ValueError("Invalid transaction type")
        instance.account.save()
