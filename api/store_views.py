from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .store_models import Product, CartItem, Order, OrderItem
from .store_serializers import ProductSerializer, CartItemSerializer, OrderSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def store_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Process/store the data here as needed
            return JsonResponse({'status': 'success', 'received': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)




class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartView(APIView):
    def get(self, request):
        user = request.query_params.get('user', 'guest')
        cart_items = CartItem.objects.filter(user=user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.data.get('user', 'guest')
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        try:
            product = Product.objects.get(id=product_id)
            if product.stock < quantity:
                return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)
            cart_item, created = CartItem.objects.get_or_create(user=user, product=product, defaults={'quantity': quantity})
            if not created:
                cart_item.quantity += quantity
                if cart_item.quantity > product.stock:
                    return Response({'error': 'Quantity exceeds available stock'}, status=status.HTTP_400_BAD_REQUEST)
                cart_item.save()
            product.stock -= quantity
            product.save()
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        user = request.query_params.get('user', 'guest')
        product_name = request.query_params.get('product_name')
        try:
            cart_items = CartItem.objects.filter(user=user, product__name=product_name)
            for item in cart_items:
                item.product.stock += item.quantity
                item.product.save()
            cart_items.delete()
            return Response({'message': 'Item removed from cart'}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

class OrderView(APIView):
    def post(self, request):
        name = request.data.get('name')
        address = request.data.get('address')
        items = request.data.get('items', [])
        user = request.data.get('user', 'guest')

        for item in items:
            product = Product.objects.get(id=item['product_id'])
            if product.stock < item['quantity']:
                return Response({'error': f"Insufficient stock for {product.name}"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(name=name, address=address)
        for item in items:
            product = Product.objects.get(id=item['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=product.price
            )
            product.stock -= item['quantity']
            product.save()

        CartItem.objects.filter(user=user).delete()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderConfirmationView(APIView):
    def post(self, request):
        order_id = request.data.get('order_id')
        payment_method = request.data.get('payment_method')
        try:
            order = Order.objects.get(id=order_id)
            order.payment_method = payment_method
            order.completed = True
            order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        order_id = request.query_params.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

