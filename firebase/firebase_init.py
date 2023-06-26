import firebase_admin
from firebase_admin import credentials, firestore
import json
import os
import threading

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

firebase_initialized = False  # Variável para verificar se o Firebase já foi inicializado
firebase_lock = threading.Lock()  # Lock para sincronização do acesso à variável global

def initialize_firebase():
    global firebase_initialized  # Acessar a variável global
    if not firebase_initialized:  # Verificar se o Firebase já foi inicializado 
        cred_path = os.path.join(BASE_DIR, "firebase/credentials.json")
        if os.path.exists(cred_path):
            with open(cred_path, 'r') as f:
                cred = json.load(f)
            try:
                firebase_admin.initialize_app(credentials.Certificate(cred))
                firebase_initialized = True  # Definir como True após a inicialização
            except ValueError as e:
                print(f"Erro ao inicializar o Firebase: {e}")
        else:
            print(f"Arquivo {cred_path} não encontrado.")


def db():
    if firebase_admin.get_app():
        return firestore.client()
    else:
        print("Firebase não inicializado.")
        return None