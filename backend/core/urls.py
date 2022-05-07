from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

from apps.account.views import AccountViewSet, BalanceHistoryViewSet, TransactionViewSet
from apps.user.views import UserViewSet

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

router = DefaultRouter()
router.register("account", AccountViewSet, basename="account")
router.register("transaction", TransactionViewSet, basename="transaction")
router.register("balance", BalanceHistoryViewSet, basename="balance")

urlpatterns += router.urls

router = DefaultRouter()
router.register("user", UserViewSet, basename="user")

urlpatterns += router.urls
