from rest_framework.viewsets import ModelViewSet

from casher.serializers import CategorySerializer, ActionSerilizer
from casher.models import Category, Action


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        self.queryset = self.queryset.filter(user=self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ActionViewSet(ModelViewSet):
    queryset = Action.objects.select_related('category').all()
    serializer_class = ActionSerilizer

    def get_queryset(self):
        self.queryset = self.queryset.filter(category__user=self.request.user)
        return super().get_queryset()
