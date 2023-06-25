import json
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F
from .models import Pedido, ItemEstoque
import firebase_admin as firestore
from firebase.firebase_init import db
from .tasks import send_sms, send_push_notification
from twilio.rest import Client
import os


@receiver(post_save, sender=Pedido)
def update_stock(sender, instance, created, **kwargs):
    if created:  # Só executa quando um novo Pedido é criado
        for detalhe in instance.detalhespedido_set.all():
            item = detalhe.item_menu
            quantidade = detalhe.quantidade

            # Atualizando no SQLite
            ItemEstoque.objects.filter(nome=item.nome).update(quantidade=F('quantidade') - quantidade)

            # Atualizando no Firestore
            doc_ref = db.collection('estoque').document(item.nome)
            try:
                doc = doc_ref.get()
                if doc.exists:
                    doc_ref.update({
                        'quantidade': firestore.Increment(-quantidade)
                    })
            except Exception as e:
                print(f"Erro ao acessar documento: {e}")

@receiver(post_save, sender=Pedido)
def notify_user(sender, instance, created, **kwargs):
    if not created:
        if instance.status == 'C':
            message = 'Seu pedido está sendo preparado. Em breve estará pronto para retirada.'
            send_sms.delay(instance.usuario.phone_number, message)
            if instance.usuario.fcm_token:
                send_push_notification.delay(instance.usuario.fcm_token, 'Pedido em preparo', message)
        elif instance.status == 'F':
            message = 'Seu pedido foi finalizado. Você pode retirá-lo agora.'
            send_sms.delay(instance.usuario.phone_number, message)
            if instance.usuario.fcm_token:
                send_push_notification.delay(instance.usuario.fcm_token, 'Pedido finalizado', message)