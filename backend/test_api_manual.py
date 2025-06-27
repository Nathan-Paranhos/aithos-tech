#!/usr/bin/env python
"""
Script para testar manualmente a API AgroGuard.
Este script permite testar os endpoints da API sem precisar configurar o ambiente de teste completo.

Exemplo de uso:
    python test_api_manual.py
"""

import requests
import json
from pprint import pprint
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
# Usamos 'localhost' ou '127.0.0.1' para conexões de cliente, não '0.0.0.0'
BASE_URL = f"http://localhost:{os.getenv('PORT', '8010')}"
TOKEN = None  # Será preenchido após o login

# Cores para o terminal
COLORS = {
    "reset": "\033[0m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
}

def print_colored(text, color):
    """Imprime texto colorido no terminal"""
    print(f"{COLORS[color]}{text}{COLORS['reset']}")

def print_response(response, endpoint):
    """Imprime a resposta de uma requisição de forma formatada"""
    print(f"\n{'-' * 50}")
    print_colored(f"Endpoint: {endpoint}", "blue")
    print_colored(f"Status: {response.status_code}", "yellow")
    print_colored("Headers:", "magenta")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    print_colored("Response:", "cyan")
    try:
        pprint(response.json())
    except json.JSONDecodeError:
        print(response.text)
    print(f"{'-' * 50}\n")

def test_health():
    """Testa o endpoint de saúde"""
    endpoint = "/health"
    response = requests.get(f"{BASE_URL}{endpoint}")
    print_response(response, endpoint)
    return response.status_code == 200

def test_root():
    """Testa o endpoint raiz"""
    endpoint = "/"
    response = requests.get(f"{BASE_URL}{endpoint}")
    print_response(response, endpoint)
    return response.status_code == 200

def test_login(email, password):
    """Testa o login e armazena o token"""
    global TOKEN
    endpoint = "/auth/login/email"
    data = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}{endpoint}", json=data)
    print_response(response, endpoint)
    
    if response.status_code == 200:
        TOKEN = response.json().get("access_token")
        print_colored(f"Token obtido: {TOKEN[:20]}...", "green")
        return True
    return False

def test_me():
    """Testa o endpoint /auth/me que requer autenticação"""
    if not TOKEN:
        print_colored("Erro: Token não disponível. Faça login primeiro.", "red")
        return False
    
    endpoint = "/auth/me"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    print_response(response, endpoint)
    return response.status_code == 200

def test_equipment_list():
    """Testa a listagem de equipamentos"""
    if not TOKEN:
        print_colored("Erro: Token não disponível. Faça login primeiro.", "red")
        return False
    
    endpoint = "/equipment"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    print_response(response, endpoint)
    return response.status_code == 200

def run_tests():
    """Executa todos os testes"""
    print_colored("Iniciando testes da API AgroGuard...", "green")
    print_colored(f"URL base: {BASE_URL}", "blue")
    
    # Testes públicos
    tests = [
        ("Teste do endpoint de saúde", test_health),
        ("Teste do endpoint raiz", test_root),
    ]
    
    # Executar testes públicos
    for test_name, test_func in tests:
        print_colored(f"Executando: {test_name}", "yellow")
        success = test_func()
        if success:
            print_colored("✓ Teste passou!", "green")
        else:
            print_colored("✗ Teste falhou!", "red")
    
    # Perguntar se deseja fazer login
    do_login = input("\nDeseja testar endpoints autenticados? (s/n): ").lower() == 's'
    if do_login:
        email = input("Email: ")
        password = input("Senha: ")
        login_success = test_login(email, password)
        
        if login_success:
            # Testes autenticados
            auth_tests = [
                ("Teste do endpoint /auth/me", test_me),
                ("Teste da listagem de equipamentos", test_equipment_list),
            ]
            
            for test_name, test_func in auth_tests:
                print_colored(f"Executando: {test_name}", "yellow")
                success = test_func()
                if success:
                    print_colored("✓ Teste passou!", "green")
                else:
                    print_colored("✗ Teste falhou!", "red")
        else:
            print_colored("Login falhou. Não é possível testar endpoints autenticados.", "red")
    
    print_colored("\nTestes concluídos!", "green")

if __name__ == "__main__":
    run_tests()