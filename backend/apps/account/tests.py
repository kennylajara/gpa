from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Account, Transaction


class AccountTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            id="00000000-0000-0000-0000-000000000001",
            username="test",
            email="test@mail.com",
            password="Test123!",
        )

        self.account = Account.objects.create(
            number=1,
            owner=self.user,
        )

        self.transaction = Transaction.objects.create(
            account=self.account,
            amount=100,
            note="Test transaction",
            type="credit",
            date="2020-01-01T00:00:00Z",
        )

    #
    # ACCOUNT
    #

    def test_create_account_with_user_authentication(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("account-list")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["ID"], 2)
        self.assertEqual(response.data["account_number"], "0000 0000 0000 0002")
        self.assertEqual(response.data["current_balance"], "0.00")
        self.assertEqual(response.data["user_id"], self.user.id)

    def test_create_account_without_user_authentication(self):
        url = reverse("account-list")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_account_without_user_authentication(self):
        url = reverse("account-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_account_with_user_authentication(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("account-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["ID"], 1)
        self.assertEqual(response.data[0]["account_number"], "0000 0000 0000 0001")
        self.assertEqual(response.data[0]["current_balance"], "100.00")
        self.assertEqual(response.data[0]["user_id"], self.user.id)

    def test_get_specific_account_without_user_authentication(self):
        url = reverse("account-detail", args=["1"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_specific_account_with_user_authentication(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("account-detail", args=["1"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["ID"], 1)
        self.assertEqual(response.data["account_number"], "0000 0000 0000 0001")
        self.assertEqual(response.data["current_balance"], "100.00")
        self.assertEqual(response.data["user_id"], self.user.id)

    #
    # TRANSACTION
    #

    def test_list_transaction_without_user_authentication(self):
        url = reverse("transaction-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_transaction_with_user_authentication(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("transaction-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["ID"], 1)
        self.assertEqual(response.data[0]["account_id"], 1)
        self.assertEqual(response.data[0]["amount"], "100.00")
        self.assertEqual(response.data[0]["note"], "Test transaction")
        self.assertEqual(response.data[0]["transaction_type"], "credit")
        self.assertEqual(response.data[0]["date"], "2020-01-01T00:00:00Z")

    def test_create_transaction_without_user_authentication(self):
        url = reverse("transaction-list")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_debit_transaction_with_user_authentication(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("transaction-list")
        data = {
            "account": 1,
            "amount": 100,
            "note": "Test transaction",
            "transaction_type": "debit",
            "date": "2020-01-02T12:00:00Z",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["ID"], 2)
        self.assertEqual(response.data["account_id"], 1)
        self.assertEqual(response.data["amount"], "100.00")
        self.assertEqual(response.data["note"], "Test transaction")
        self.assertEqual(response.data["date"], "2020-01-02T12:00:00Z")
        self.assertEqual(response.data["transaction_type"], "debit")

        # Check account balance
        account = Account.objects.get(number=1)
        self.assertEqual(str(account.current_balance), "0.00")

    def test_create_credit_transaction_with_user_authentication(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("transaction-list")
        data = {
            "account": 1,
            "amount": 100,
            "note": "Test transaction",
            "transaction_type": "credit",
            "date": "2020-01-02T12:00:00Z",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["ID"], 2)
        self.assertEqual(response.data["account_id"], 1)
        self.assertEqual(response.data["amount"], "100.00")
        self.assertEqual(response.data["note"], "Test transaction")
        self.assertEqual(response.data["date"], "2020-01-02T12:00:00Z")
        self.assertEqual(response.data["transaction_type"], "credit")

        # Check account balance
        account = Account.objects.get(number=1)
        self.assertEqual(str(account.current_balance), "200.00")

    def test_create_transaction_with_invalid_account_id(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("transaction-list")
        data = {
            "account": 2,
            "amount": 100,
            "note": "Test transaction",
            "transaction_type": "credit",
            "date": "2020-01-02T12:00:00Z",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "Account does not exist")

    def test_create_transaction_with_invalid_transaction_type(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("transaction-list")
        data = {
            "account": 1,
            "amount": 100,
            "note": "Test transaction",
            "transaction_type": "invalid",
            "date": "2020-01-02T12:00:00Z",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["transaction_type"][0], '"invalid" is not a valid choice.'
        )

    def test_get_transaction_without_user_authentication(self):
        url = reverse("transaction-detail", args=["1"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_transaction_with_user_authentication(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("transaction-detail", args=["1"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["ID"], 1)
        self.assertEqual(response.data["account_id"], 1)
        self.assertEqual(response.data["amount"], "100.00")
        self.assertEqual(response.data["note"], "Test transaction")
        self.assertEqual(response.data["transaction_type"], "credit")
        self.assertEqual(response.data["date"], "2020-01-01T00:00:00Z")

    #
    # Balance
    #

    def test_get_balance_history_without_user_authentication(self):
        url = reverse("balance-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_balance_history_with_user_authentication(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("balance-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["account_id"], 1)
        self.assertEqual(response.data[0]["balance"], "100.00")
        self.assertEqual(response.data[0]["date"], timezone.now().strftime("%Y-%m-%d"))

    def test_get_balance_history_with_user_authentication_and_account_id(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("balance-account", args=["1"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["account_id"], 1)
        self.assertEqual(response.data[0]["balance"], "100.00")
        self.assertEqual(response.data[0]["date"], timezone.now().strftime("%Y-%m-%d"))

    def test_get_balance_history_with_user_authentication_and_account_id_and_date(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(
            "balance-account-date", args=[1, timezone.now().strftime("%Y-%m-%d")]
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["account_id"], 1)
        self.assertEqual(response.data["balance"], "100.00")
        self.assertEqual(response.data["date"], timezone.now().strftime("%Y-%m-%d"))
