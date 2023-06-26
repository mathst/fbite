from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
# from allauth.account.views import ConfirmEmailView
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

from . import views

app_name = 'main'

schema_view = get_schema_view(
    openapi.Info(
        title="fbite API",
        default_version='v1',
        description="fbite API Documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('categorias/', views.CategoriaList.as_view(), name='categoria_list'),
    path('categorias/<int:pk>/', views.CategoriaDetail.as_view(), name='categoria_detail'),
    path('menuitems/', views.MenuItemList.as_view(), name='menu_item_list'),
    path('menuitems/<int:pk>/', views.MenuItemDetail.as_view(), name='menu_item_detail'),
    path('carrinhos/', views.CarrinhoList.as_view(), name='carrinho_list'),
    path('carrinhos/<int:pk>/', views.CarrinhoDetail.as_view(), name='carrinho_detail'),
    path('carrinhoitens/', views.CarrinhoItemList.as_view(), name='carrinho_item_list'),
    path('carrinhoitens/<int:pk>/', views.CarrinhoItemDetail.as_view(), name='carrinho_item_detail'),
    path('pedidos/', views.PedidoList.as_view(), name='pedido_list'),
    path('pedidos/<int:pk>/', views.PedidoDetail.as_view(), name='pedido_detail'),
    path('detalhepedidos/', views.DetalhePedidoList.as_view(), name='detalhe_pedido_list'),
    path('detalhepedidos/<int:pk>/', views.DetalhePedidoDetail.as_view(), name='detalhe_pedido_detail'),
    path('itensestoque/', views.ItemEstoqueList.as_view(), name='item_estoque_list'),
    path('itensestoque/<int:pk>/', views.ItemEstoqueDetail.as_view(), name='item_estoque_detail'),
    path('vendas/', views.VendaList.as_view(), name='venda_list'),
    path('vendas/<int:pk>/', views.VendaDetail.as_view(), name='venda_detail'),
    path('itemvendas/', views.ItemVendaList.as_view(), name='item_venda_list'),
    path('itemvendas/<int:pk>/', views.ItemVendaDetail.as_view(), name='item_venda_detail'),
    # path('api/auth/', include('django_rest_firebase_auth.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
