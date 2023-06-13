from django.urls import path
from rest_framework.routers import DefaultRouter

from casher.views import CategoryViewSet, ActionViewSet


router = DefaultRouter()
router.register('categories', CategoryViewSet)
router. register('actions', ActionViewSet)


urlpatterns = router.urls