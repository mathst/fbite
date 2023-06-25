from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import CustomUser, Categoria, MenuItem, Carrinho, CarrinhoItem, Pedido, DetalhePedido, ItemEstoque, Venda, ItemVenda
from .serializers import UserSerializer, CategoriaSerializer, MenuItemSerializer, CarrinhoSerializer, CarrinhoItemSerializer, PedidoSerializer, DetalhePedidoSerializer, ItemEstoqueSerializer, VendaSerializer, ItemVendaSerializer
# from tasks import processar_pagamento


class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class CategoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class MenuItemList(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class MenuItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class CarrinhoList(generics.ListCreateAPIView):
    queryset = Carrinho.objects.all()
    serializer_class = CarrinhoSerializer

class CarrinhoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Carrinho.objects.all()
    serializer_class = CarrinhoSerializer

class CarrinhoItemList(generics.ListCreateAPIView):
    queryset = CarrinhoItem.objects.all()
    serializer_class = CarrinhoItemSerializer

class CarrinhoItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarrinhoItem.objects.all()
    serializer_class = CarrinhoItemSerializer

class PedidoList(generics.ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class PedidoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class DetalhePedidoList(generics.ListCreateAPIView):
    queryset = DetalhePedido.objects.all()
    serializer_class = DetalhePedidoSerializer

class DetalhePedidoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetalhePedido.objects.all()
    serializer_class = DetalhePedidoSerializer

class ItemEstoqueList(generics.ListCreateAPIView):
    queryset = ItemEstoque.objects.all()
    serializer_class = ItemEstoqueSerializer

class ItemEstoqueDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ItemEstoque.objects.all()
    serializer_class = ItemEstoqueSerializer

class VendaList(generics.ListCreateAPIView):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer

class VendaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer

class ItemVendaList(generics.ListCreateAPIView):
    queryset = ItemVenda.objects.all()
    serializer_class = ItemVendaSerializer

class ItemVendaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ItemVenda.objects.all()
    serializer_class = ItemVendaSerializer
    

# class CheckoutView(View):
#     def post(self, request, pedido_id):
#         # Iniciar o processamento de pagamento em segundo plano
#         pagamento_processado = processar_pagamento.delay(pedido_id)

#         if pagamento_processado:
#             response = {'message': 'Pagamento sendo processado'}
#             status = 202  # HTTP status code para 'Accepted'
#         else:
#             response = {'message': 'Houve um problema ao processar seu pagamento'}
#             status = 400  # HTTP status code para 'Bad Request'

#         return JsonResponse(response, status=status)
