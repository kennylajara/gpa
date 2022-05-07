from django.utils import timezone
from rest_framework import serializers

from .models import Account, BalanceHistory, Transaction


class AccountSerializer(serializers.ModelSerializer):

    ID = serializers.IntegerField(source="number", read_only=True)
    account_number = serializers.SerializerMethodField()
    current_balance = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0, read_only=True
    )
    user_id = serializers.UUIDField(source="owner.id", read_only=True)

    class Meta:
        model = Account
        fields = ("ID", "account_number", "current_balance", "user_id")

    def get_account_number(self, obj):
        zeros_added = str(obj.number).rjust(16, "0")
        return f"{zeros_added[:4]} {zeros_added[4:8]} {zeros_added[8:12]} {zeros_added[12:]}"


class TransactionSerializer(serializers.ModelSerializer):

    ID = serializers.IntegerField(source="id", read_only=True)
    account_id = serializers.IntegerField(source="account.number", read_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    note = serializers.CharField(max_length=255, required=False, allow_blank=True)
    transaction_type = serializers.ChoiceField(
        source="type", choices=Transaction.TransactionType.choices, required=True
    )
    date = serializers.DateTimeField(default=timezone.now)

    class Meta:
        model = Transaction
        fields = ("ID", "date", "transaction_type", "note", "amount", "account_id")

    def get_transaction_id(self, obj):
        return str(obj.id).rjust(8, "0")


class BalanceHistorySerializer(serializers.ModelSerializer):

    account_id = serializers.IntegerField(source="account.number", read_only=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    date = serializers.SerializerMethodField()

    class Meta:
        model = BalanceHistory
        fields = ("date", "balance", "account_id")

    def get_date(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")
