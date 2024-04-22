import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore

from products.forms import ProductForm
from products.models import Product
from products.permissions import IsSuperUser


def product_list(request):
    products = list(Product.objects.all().values())
    return JsonResponse(products, safe=False)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return JsonResponse({'product': {'name': product.name, 'description': product.description, 'price': str(product.price)}})


@csrf_exempt
def product_create(request):
    if request.method == 'POST':
        # Convertendo o JSON em dicionário Python
        json_data = json.loads(request.body)
        form = ProductForm(json_data)
        if form.is_valid():
            # Dados válidos, fazer algo com eles
            form.save()
            return JsonResponse({'success': True, 'message': 'Product created successfully'})
        else:
            # Dados inválidos, retornar erros
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)


@csrf_exempt
@permission_classes([IsAuthenticated, IsSuperUser])
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'PUT':
        json_data = json.loads(request.body)
        form = ProductForm(json_data, instance=product)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Product updated successfully'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)


@csrf_exempt
@permission_classes([IsAuthenticated, IsSuperUser])
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'DELETE':
        product.delete()
        return JsonResponse({'success': True, 'message': 'Product deleted successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
