from rest_framework import serializers
from .models import CustomUser, Categoria, MenuItem, Carrinho, CarrinhoItem, Pedido, DetalhePedido, ItemEstoque, Venda, ItemVenda

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = '__all__'

class CarrinhoItemSerializer(serializers.ModelSerializer):
    item_menu = MenuItemSerializer(read_only=True)
    class Meta:
        model = CarrinhoItem
        fields = '__all__'

class CarrinhoSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    carrinho_itens = CarrinhoItemSerializer(many=True)
    class Meta:
        model = Carrinho
        fields = '__all__'

class DetalhePedidoSerializer(serializers.ModelSerializer):
    item_menu = MenuItemSerializer(read_only=True)
    class Meta:
        model = DetalhePedido
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    detalhes_pedido = DetalhePedidoSerializer(many=True)
    class Meta:
        model = Pedido
        fields = '__all__'

class ItemEstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemEstoque
        fields = '__all__'

class ItemVendaSerializer(serializers.ModelSerializer):
    item_menu = MenuItemSerializer(read_only=True)
    class Meta:
        model = ItemVenda
        fields = '__all__'

class VendaSerializer(serializers.ModelSerializer):
    pedido = PedidoSerializer(read_only=True)
    itens_venda = ItemVendaSerializer(many=True)
    class Meta:
        model = Venda
        fields = '__all__'
