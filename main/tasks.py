# tasks.py
import stripe
from pydoc import stripid
from django.conf import settings
from firebase_admin import messaging
from twilio.rest import Client
from celery import shared_task
from firebase.firebase_init import db

# Twilio config
twilio_phone_number = settings.TWILIO_PHONE_NUMBER
clientT = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)

@shared_task
def send_sms(phone_number, message):
    message = clientT.messages.create(
        from_=twilio_phone_number,
        body=message,
        to=phone_number
    )
    return message.sid

@shared_task
def send_push_notification(token, title, message):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=message
        ),
        token=token,
    )

    response = messaging.send(message)
    return response


@shared_task
def criar_usuario(user_id, password):
    from django.contrib.auth.models import AbstractUser
    from .models import CustomUser as Usuario

    user = Usuario.objects.get(pk=user_id)
    user.set_password(password)
    user.save()

@shared_task
def login(user_id, password):
    from django.contrib.auth.models import AbstractUser
    from .models import CustomUser as Usuario
    user = Usuario.objects.get(pk=user_id)
    if user.check_password(password):
        return True
    else:
        return False

@shared_task
def atualizar_estoque(pedido_id):
    from .models import Pedido, DetalhePedido, ItemEstoque

    pedido = Pedido.objects.get(pk=pedido_id)
    detalhes = DetalhePedido.objects.filter(pedido=pedido)
    for detalhe in detalhes:
        item_estoque = ItemEstoque.objects.get(nome=detalhe.item.nome)
        item_estoque.quantidade -= detalhe.quantidade
        item_estoque.save()

        # Atualizar ingredientes individuais
        for ingrediente in detalhe.item.ingredientes:
            item_estoque_ingrediente = ItemEstoque.objects.get(nome=ingrediente)
            item_estoque_ingrediente.quantidade -= detalhe.quantidade
            item_estoque_ingrediente.save()

@shared_task
def sincronizar_dados():
    from .models import ItemEstoque
    itens_estoque = ItemEstoque.objects.all()

    for item_estoque in itens_estoque:
        doc_ref = db
        # Supondo que 'estoque' é uma subcoleção da coleção 'produtos'
        colecoes_documentos = ['produtos', 'produto_id', 'estoque', item_estoque.nome]
        
        for i in range(len(colecoes_documentos) - 1):
            if i % 2 == 0:
                doc_ref = doc_ref.collection(colecoes_documentos[i])
            else:
                doc_ref = doc_ref.document(colecoes_documentos[i])

        doc_ref = doc_ref.document(colecoes_documentos[-1])
        doc_ref.set({
            'nome': item_estoque.nome,
            'quantidade': item_estoque.quantidade
        })
        
# @shared_task
# def processar_pagamento(pedido_id):
#     from .models import Pedido
#     stripid.api_key = "your-stripe-api-key"

#     pedido = Pedido.objects.get(id=pedido_id)

#     # Substitua com a lógica para recuperar o token do cartão do cliente
#     token_do_cartao = "token-do-cartao"

#     try:
#         charge = stripe.Charge.create(
#             amount=int(pedido.total * 100),  # Stripe espera o valor em centavos
#             currency="usd",
#             source=token_do_cartao,  # obtido com o Stripe.js
#             description=f"Cobrança para o pedido {pedido.id}"
#         )

#         if charge.paid:
#             pedido.status = Pedido.PAGO
#             pedido.save()
#             return True

#     except stripe.error.CardError as e:
#         # O cartão foi recusado
#         print(f"O pagamento para o pedido {pedido.id} foi recusado.{e}")
#     except Exception as e:
#         print(f"Ocorreu um erro ao processar o pagamento para o pedido {pedido.id}.{e}")
    
#     return False