# Generated by Django 3.2.19 on 2023-06-25 23:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='DetalhePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ItemEstoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(blank=True, max_length=100, null=True)),
                ('nome', models.CharField(max_length=200)),
                ('quantidade', models.IntegerField()),
                ('data_reposicao', models.DateTimeField(auto_now_add=True)),
                ('data_validade', models.DateTimeField()),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='estoque_images/')),
                ('valor_unitario', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(blank=True, max_length=100, null=True)),
                ('nome', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('descricao', models.TextField()),
                ('preco', models.DecimalField(decimal_places=2, max_digits=5)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='menu_images/')),
                ('ativo', models.BooleanField(default=True)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='menu_items', to='main.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(choices=[('P', 'Pendente'), ('C', 'Cozinhando'), ('F', 'Finalizado')], default='P', max_length=1)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('data_criado', models.DateTimeField(auto_now_add=True)),
                ('itens', models.ManyToManyField(through='main.DetalhePedido', to='main.MenuItem')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_venda', models.DateTimeField(auto_now_add=True)),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=6)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendas', to='main.pedido')),
            ],
        ),
        migrations.CreateModel(
            name='ItemVenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField()),
                ('item_menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_venda', to='main.menuitem')),
                ('venda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_venda', to='main.venda')),
            ],
        ),
        migrations.AddField(
            model_name='detalhepedido',
            name='item_menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalhes_pedido', to='main.menuitem'),
        ),
        migrations.AddField(
            model_name='detalhepedido',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalhes_pedido', to='main.pedido'),
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('uid', models.CharField(max_length=100, unique=True)),
                ('image', models.URLField(blank=True, null=True)),
                ('provider', models.CharField(blank=True, max_length=100, null=True)),
                ('tipo', models.CharField(choices=[('ADM', 'adm'), ('GER', 'gerente'), ('FUN', 'funcionario'), ('CLI', 'cliente')], max_length=15)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='custom_users', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='custom_users', to='auth.Permission')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CarrinhoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField()),
                ('carrinho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carrinho_itens', to='main.carrinho')),
                ('item_menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carrinho_itens', to='main.menuitem')),
            ],
        ),
        migrations.AddField(
            model_name='carrinho',
            name='itens',
            field=models.ManyToManyField(through='main.CarrinhoItem', to='main.MenuItem'),
        ),
        migrations.AddField(
            model_name='carrinho',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='carrinho', to=settings.AUTH_USER_MODEL),
        ),
    ]
