from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from enum import Enum
from django.contrib.auth.models import Group, Permission
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class TipoUsuario(models.TextChoices):
    ADM = 'adm', 'Administrador'
    GER = 'gerente', 'Gerente'
    FUN = 'funcionario', 'Funcionário'
    CLI = 'cliente', 'Cliente'

class UserManager(BaseUserManager):
    def create_user(self, email, uid, name=None, image=None, provider=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not uid:
            raise ValueError('The UID field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, uid=uid, name=name, image=image, provider=provider, **extra_fields)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    uid = models.CharField(max_length=100, unique=True)
    image = models.URLField(null=True, blank=True)
    provider = models.CharField(max_length=100, null=True, blank=True)
    tipo = models.CharField(max_length=15, choices=[(tipo.name, tipo.value) for tipo in TipoUsuario])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['uid']

    # Adicione o argumento related_name='custom_users' aos campos groups e user_permissions
    groups = models.ManyToManyField(Group, blank=True, related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='custom_users')

    def __str__(self):
        return self.email

class Categoria(models.Model):
    nome = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.nome

class MenuItem(models.Model):
    uid = models.CharField(max_length=100, blank=True, null=True)
    nome = models.CharField(max_length=200, null=False, blank=False, db_index=True)
    slug = models.SlugField(null=True, blank=True)
    descricao = models.TextField(null=False, blank=False)
    preco = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    categoria = models.ForeignKey(Categoria, related_name='menu_items', on_delete=models.SET_NULL, null=True)
    imagem = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    ativo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} - {self.descricao[:20]}..."

class Carrinho(models.Model):
    usuario = models.OneToOneField(User, related_name='carrinho', on_delete=models.CASCADE)
    itens = models.ManyToManyField(MenuItem, through='CarrinhoItem')

class CarrinhoItem(models.Model):
    carrinho = models.ForeignKey(Carrinho, related_name='carrinho_itens', on_delete=models.CASCADE)
    item_menu = models.ForeignKey(MenuItem, related_name='carrinho_itens', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('C', 'Cozinhando'),
        ('F', 'Finalizado'),
    ]

    uid = models.CharField(max_length=100, blank=True, null=True)
    usuario = models.ForeignKey(User, related_name='pedidos', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P') 
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    data_criado = models.DateTimeField(auto_now_add=True)
    itens = models.ManyToManyField(MenuItem, through='DetalhePedido')

    def __str__(self):
        status_dict = dict(self.STATUS_CHOICES)
        return f'Pedido {self.id} - Status: {status_dict[self.status]}'

@receiver(post_save, sender=Pedido)
def atualizar_estoque_signal(sender, instance, created, **kwargs):
    if created:
        # import the atualizar_estoque function here instead
        from .services import atualizar_estoque
        atualizar_estoque.delay(instance.id)

class DetalhePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalhes_pedido', on_delete=models.CASCADE)
    item_menu = models.ForeignKey(MenuItem, related_name='detalhes_pedido', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantidade} x {self.item_menu.nome} - Pedido {self.pedido.id}'
    

class ItemEstoque(models.Model):
    uid = models.CharField(max_length=100, blank=True, null=True)
    nome = models.CharField(max_length=200, null=False, blank=False)
    quantidade = models.IntegerField(null=False, blank=False)
    data_reposicao = models.DateTimeField(auto_now_add=True)
    data_validade = models.DateTimeField(null=False, blank=False)
    imagem = models.ImageField(upload_to='estoque_images/', null=True, blank=True)
    valor_unitario = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return f"{self.nome} - Quantidade em estoque: {self.quantidade}"

class Venda(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='vendas', on_delete=models.CASCADE)
    data_venda = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return f'Venda {self.id} - Valor Total: {self.valor_total}'


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name="itens_venda", on_delete=models.CASCADE)
    item_menu = models.ForeignKey(MenuItem, related_name='itens_venda', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return f'{self.quantidade} x {self.item_menu.nome} - Venda {self.venda.id}'