

from rest_framework import viewsets  # type: ignore
from rest_framework.decorators import action  # type: ignore
from rest_framework.response import Response  # type: ignore

from products.models import Product
from products.permissions import IsSuperUser
from products.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSuperUser]

    @action(detail=False, methods=['post'])
    def create_product(self, request):
        # Implement your create logic here
        return Response({'message': 'Product created successfully'})

    @action(detail=True, methods=['delete'])
    def delete_product(self, request, pk=None):
        # Implement your delete logic here
        return Response({'message': 'Product deleted successfully'})
