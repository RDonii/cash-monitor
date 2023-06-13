from django.db import models
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.request import Request
from django_filters.rest_framework import DjangoFilterBackend

from casher.serializers import CategorySerializer, ActionSerilizer
from casher.models import Category, Action


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type']
    search_fields = ['name']
    
    def get_queryset(self):
        self.queryset = self.queryset.filter(user=self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ActionViewSet(ModelViewSet):
    queryset = Action.objects.select_related('category').all()
    serializer_class = ActionSerilizer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'category__type']
    search_fields = ['category__name', 'issuer']

    def get_queryset(self):
        self.queryset = self.queryset.filter(category__user=self.request.user)
        return super().get_queryset()


class BalanceView(GenericAPIView):
    def get(self, request: Request, *args, **kwargs):
        income_sum = models.Sum('amount_sum', filter=models.Q(category__type=Category.TypeChoice.IN))
        outcome_sum = models.Sum('amount_sum', filter=models.Q(category__type=Category.TypeChoice.OUT))
        income_dollar = models.Sum('amount_dollar', filter=models.Q(category__type=Category.TypeChoice.IN))
        outcome_dollar = models.Sum('amount_dollar', filter=models.Q(category__type=Category.TypeChoice.OUT))
        balance = Action.objects\
                        .filter(category__user=request.user)\
                        .aggregate(sum=income_sum-outcome_sum, dollar=income_dollar-outcome_dollar)

        return Response(balance)
