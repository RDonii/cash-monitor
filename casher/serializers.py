from rest_framework import serializers

from core.models import User
from casher.models import Category, Action


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'user', 'created']


class ActionSerilizer(serializers.ModelSerializer):
    type = serializers.CharField(source='category__type')
    name = serializers.CharField(source='category__name')

    class Meta:
        model = Action
        fields = ['id', 'issuer', "amount_dollar", "amount_sum", "description", "dolar_price", "issued", "created", "updated"]
