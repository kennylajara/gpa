from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, serializers, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Account, Transaction, BalanceHistory
from .serializers import (
    AccountSerializer,
    BalanceHistorySerializer,
    TransactionSerializer,
)


class AccountViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        """The logged in user is always the owner"""
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Limit the queryset to the owner, i.e the logged in user, for fetching/updating data"""
        return self.queryset.filter(owner=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        """The logged in user always needs to be the account owner"""
        try:
            return serializer.save(
                account=Account.objects.get(
                    owner=self.request.user, number=str(self.request.data["account"])
                )
            )
        except Account.DoesNotExist:
            raise serializers.ValidationError("Account does not exist")

    def get_queryset(self):
        """Limit the queryset to the owner, i.e the logged in user, for fetching/updating data"""
        return self.queryset.filter(account__owner=self.request.user)


class BalanceHistoryViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):

    permission_classes = (IsAuthenticated,)
    serializer_class = BalanceHistorySerializer
    queryset = BalanceHistory.objects.all()

    def get_queryset(self):
        """Limit the queryset to the owner, i.e the logged in user, for fetching/updating data"""
        return self.queryset.filter(account__owner=self.request.user)

    @action(detail=False, methods=["GET"], url_path="account/(?P<account_id>[0-9]+)")
    def account(self, request, account_id):
        """Get the balance history for a specific account"""
        try:
            account = Account.objects.get(
                owner=self.request.user, number=str(account_id)
            )
        except Account.DoesNotExist:
            raise serializers.ValidationError("Account does not exist")
        return Response(
            BalanceHistorySerializer(account.balancehistory_set.all(), many=True).data
        )

    @action(
        detail=False,
        methods=["GET"],
        url_path="account/(?P<account_id>[0-9]+)/(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})",
    )
    def account_date(self, request, account_id, date):
        """Get the balance history for a specific account on a specific date, filtered by created_at"""
        try:
            account = Account.objects.get(
                owner=self.request.user, number=str(account_id)
            )
        except Account.DoesNotExist:
            raise serializers.ValidationError("Account does not exist")

        date = timezone.datetime.strptime(f"{date} 23:59:59", "%Y-%m-%d %H:%M:%S")
        date = timezone.make_aware(date, timezone.get_current_timezone())
        try:
            return Response(
                BalanceHistorySerializer(
                    account.balancehistory_set.filter(created_at__lte=date), many=True
                ).data[0]
            )
        except IndexError:
            raise serializers.ValidationError("No balance history found for this date")
