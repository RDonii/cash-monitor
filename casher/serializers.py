from rest_framework import serializers

from casher.models import Category, Action


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'user', 'created']
        read_only_fields = ['id', 'user']


class ActionSerilizer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Action
        fields = ['id', 'category', "name", "type", 'issuer', "amount_dollar", "amount_sum", "description", "dolar_price", "issued", "created", "updated"]
        extra_kwargs = {
            'category': {"write_only": True}
        }

    def get_type(self, action: Action):
        return action.category.type

    def get_name(self, action: Action):
        return action.category.name


class ActionSumSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    amount = serializers.DecimalField(max_digits=11, decimal_places=2)

    class Meta:
        model = Action
        fields = ['id', 'category', "name", "type", "amount"]

    def get_type(self, action: Action):
        return action.category.type

    def get_name(self, action: Action):
        return action.category.name
