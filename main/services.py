# services.py
import json
from django.conf import settings
from firebase.firebase_init import db

class FirestoreService:
    def __init__(self, credentials_path):
        self.credentials_path = credentials_path


    def criar_item(self, colecoes_documentos, dados):
        doc_ref = self.db
        for i in range(len(colecoes_documentos) - 1):
            if i % 2 == 0:
                doc_ref = doc_ref.collection(colecoes_documentos[i])
            else:
                doc_ref = doc_ref.document(colecoes_documentos[i])

        doc_ref = doc_ref.document(colecoes_documentos[-1])
        doc_ref.set(dados)

    def obter_item(self, colecoes_documentos):
        doc_ref = self.db
        for i in range(len(colecoes_documentos)):
            if i % 2 == 0:
                doc_ref = doc_ref.collection(colecoes_documentos[i])
            else:
                doc_ref = doc_ref.document(colecoes_documentos[i])

        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return None

    def atualizar_item(self, colecoes_documentos, dados):
        doc_ref = self.db
        for i in range(len(colecoes_documentos) - 1):
            if i % 2 == 0:
                doc_ref = doc_ref.collection(colecoes_documentos[i])
            else:
                doc_ref = doc_ref.document(colecoes_documentos[i])

        doc_ref = doc_ref.document(colecoes_documentos[-1])
        doc_ref.update(dados)

    def excluir_item(self, colecoes_documentos):
        doc_ref = self.db
        for i in range(len(colecoes_documentos) - 1):
            if i % 2 == 0:
                doc_ref = doc_ref.collection(colecoes_documentos[i])
            else:
                doc_ref = doc_ref.document(colecoes_documentos[i])

        doc_ref = doc_ref.document(colecoes_documentos[-1])
        doc_ref.delete()