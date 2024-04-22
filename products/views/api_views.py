

from rest_framework import viewsets  # type: ignore
from rest_framework.decorators import action  # type: ignore
from rest_framework.permissions import BasePermission  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.viewsets import ViewSet  # type:ignore

from products.models import Product


class IsAuthenticatedOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in ('POST', 'DELETE'):
            return request.user and request.user.is_authenticated
        return True


class ProductViewSet(ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['post'])
    def create_product(self, request):
        name = request.data.get('name')
        description = request.data.get('description')
        price = request.data.get('price')

        product = Product.objects.create(
            name=name,
            description=description,
            price=price
        )

        return Response({'message': 'Product created successfully', 'product_id': product.pk})

    @action(detail=True, methods=['delete'])
    def delete_product(self, request, pk=None):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=404)

        if request.user != product.name:
            return Response({'message': 'Permission denied'}, status=403)

        product.delete()

        return Response({'message': 'Product deleted successfully'})
