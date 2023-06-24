import os
from django.db import models
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
import pandas as pd

from casher.serializers import ActionSumSerializer, CategorySerializer, ActionSerilizer
from casher.models import Category, Action
from casher.filters import ActionRangeFilter


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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'category__type']
    filterset_class = ActionRangeFilter
    ordering_fields = ['issued']
    search_fields = ['issuer']

    def get_serializer_class(self):
        if self.action == 'excel':
            return ActionSumSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        self.queryset = self.queryset.filter(category__user=self.request.user)
        return super().get_queryset()
    
    @action(detail=False, methods=['GET'])
    def excel(self, request):
        queryset = self.get_queryset()
        filtered_quertset: models.QuerySet = self.filter_queryset(queryset=queryset)
        data = filtered_quertset.annotate(amount=models.Sum(models.F('amount_sum') + models.F('amount_dollar') * models.F('dolar_price')))
        serializer = self.get_serializer(data, many=True)
        df = pd.DataFrame(serializer.data, columns=['name', 'type', 'amount'])
        df['amount'] = pd.to_numeric(df['amount'])
        res = df.groupby('name')['amount'].sum().reset_index()
        res.index += 1

        filename = 'report.xlsx'
        path = settings.MEDIA_ROOT / str(request.user.id)
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)

        relative_file_path = settings.MEDIA_DIR + str(request.user.id) + "/" + filename

        with pd.ExcelWriter(
            path / filename,
            mode="w",
            engine="openpyxl",
        ) as writer:
            sheet_name = self.kwargs.get('date_after', '') + '-' + self.kwargs.get('date_before', '')
            res.to_excel(writer, sheet_name=sheet_name)

        return Response({'file_link': request.build_absolute_uri("/" + relative_file_path)})


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
