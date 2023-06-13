from django.urls import path
from rest_framework.routers import DefaultRouter

from casher.views import CategoryViewSet, ActionViewSet, BalanceView


router = DefaultRouter()
router.register('categories', CategoryViewSet)
router. register('actions', ActionViewSet)


urlpatterns = [
    path('get_balance/', BalanceView.as_view())
] + router.urls
