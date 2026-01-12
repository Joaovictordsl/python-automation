import requests
import time
import sys
import os
import subprocess
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# --- CONFIGURACAO ---
BASE_URL = "http://127.0.0.1:50325"
NOME_GRUPO = "JOAO LIMA 03 - 21/12/25"

def buscar_perfis_recentes(quantidade):
    """Busca os perfis mais recentes do AdsPower (os primeiros da lista)."""
    url = f"{BASE_URL}/api/v1/user/list"
    params = {"page_size": 100}

    try:
        response = requests.get(url, params=params).json()
        if response["code"] == 0:
            perfis = response["data"]["list"]
            ids = [p["user_id"] for p in perfis if p.get("group_name") == NOME_GRUPO]
            # Retorna os X primeiros (mais recentes)
            return ids[:quantidade]
        else:
            print(f"Erro na API: {response['msg']}")
            return []
    except Exception as e:
        print(f"Erro ao buscar perfis: {e}")
        return []

def carregar_contas_recentes(quantidade):
    """Carrega as X contas mais recentes do arquivo (ultimas linhas)."""
    contas = []
    try:
        if not os.path.exists("contas_outlook.txt"):
            print("Erro: Arquivo contas_outlook.txt nao encontrado!")
            return contas

        with open("contas_outlook.txt", "r") as f:
            linhas = f.readlines()
            # Pega as ultimas X linhas (mais recentes)
            linhas_recentes = linhas[-quantidade:] if len(linhas) >= quantidade else linhas

            for linha in linhas_recentes:
                linha = linha.strip()
                if not linha:
                    continue
                partes = linha.split(" | ")
                if len(partes) >= 2:
                    email = partes[0].replace("Email: ", "").strip()
                    senha = partes[1].replace("Senha: ", "").strip()
                    contas.append({"email": email, "senha": senha})
        return contas
    except Exception as e:
        print(f"Erro ao ler contas: {e}")
        return contas

def abrir_perfil(user_id):
    """Abre um perfil no AdsPower."""
    try:
        res = requests.get(f"{BASE_URL}/api/v1/browser/start?user_id={user_id}").json()
        if res["code"] == 0:
            print(f"[{user_id}] Perfil aberto")
            return True
        else:
            print(f"[{user_id}] Erro ao abrir: {res.get('msg', 'Desconhecido')}")
            return False
    except Exception as e:
        print(f"[{user_id}] Erro: {e}")
        return False

def signup_shopify(user_id, email, senha):
    """Faz o cadastro no Shopify para um perfil."""
    driver = None
    try:
        print(f"[{user_id}] Conectando ao navegador...")
        res = requests.get(f"{BASE_URL}/api/v1/browser/active?user_id={user_id}").json()

        if res["code"] != 0:
            print(f"[{user_id}] Erro: Perfil nao esta aberto!")
            return False

        options = Options()
        options.add_experimental_option("debuggerAddress", res["data"]["ws"]["selenium"])
        service = Service(executable_path=res["data"]["webdriver"])
        driver = webdriver.Chrome(service=service, options=options)

        driver.set_page_load_timeout(60)
        driver.set_script_timeout(60)
        driver.implicitly_wait(10)

        # Acessar Shopify
        print(f"[{user_id}] Acessando Shopify...")
        driver.get("https://www.shopify.com/br/free-trial")
        time.sleep(6)

        actions = ActionChains(driver)
        driver.switch_to.default_content()

        # Aguardar tela de metodos de cadastro
        print(f"[{user_id}] Aguardando tela de cadastro...")
        time.sleep(7)

        # Navegar ate botao de email (3 TABs + ENTER)
        print(f"[{user_id}] Navegando ate botao de email...")
        actions.send_keys(Keys.TAB).perform()
        time.sleep(0.5)
        actions.send_keys(Keys.TAB).perform()
        time.sleep(0.5)
        actions.send_keys(Keys.TAB).perform()
        time.sleep(0.5)
        actions.send_keys(Keys.ENTER).perform()

        # Digitar email
        time.sleep(4)
        print(f"[{user_id}] Preenchendo Email: {email}")
        actions.send_keys(email).send_keys(Keys.ENTER).perform()

        # Digitar senha
        time.sleep(4)
        print(f"[{user_id}] Preenchendo Senha...")
        actions.send_keys(senha).send_keys(Keys.ENTER).perform()

        print(f"\n{'='*40}")
        print(f"[{user_id}] LOJA VINCULADA COM SUCESSO!")
        print(f"Email: {email}")
        print(f"{'='*40}\n")

        # Salvar log
        with open("lojas_shopify.txt", "a") as f:
            f.write(f"Email: {email} | Senha: {senha} | Perfil: {user_id} | Status: Criada\n")

        return True

    except Exception as e:
        print(f"[{user_id}] Erro no signup: {e}")
        return False

def executar_signup_thread(user_id, email, senha):
    """Wrapper para executar signup em thread."""
    signup_shopify(user_id, email, senha)

def main():
    if len(sys.argv) < 2:
        print("Uso: python shopify_batch.py <QUANTIDADE>")
        print("Exemplo: python shopify_batch.py 3")
        print("\nIsso vai cadastrar 3 contas em paralelo")
        sys.exit(1)

    quantidade = int(sys.argv[1])
    print(f"\n{'='*50}")
    print(f"SHOPIFY BATCH SIGNUP - {quantidade} conta(s)")
    print(f"{'='*50}\n")

    # Buscar perfis e contas
    print("Buscando perfis no AdsPower...")
    perfis = buscar_perfis_recentes(quantidade)

    print("Carregando contas do arquivo...")
    contas = carregar_contas_recentes(quantidade)

    if len(perfis) < quantidade:
        print(f"Aviso: Apenas {len(perfis)} perfis disponiveis")
    if len(contas) < quantidade:
        print(f"Aviso: Apenas {len(contas)} contas disponiveis")

    # Usar a menor quantidade disponivel
    total = min(len(perfis), len(contas))
    if total == 0:
        print("Erro: Nenhum perfil ou conta disponivel!")
        sys.exit(1)

    print(f"\nVao ser usados {total} perfil(is) e conta(s):\n")

    # Mostrar pareamento
    for i in range(total):
        print(f"  {i+1}. Perfil: {perfis[i]} -> Email: {contas[i]['email']}")

    print(f"\n{'='*50}")
    input("Pressione ENTER para abrir os perfis...")

    # Abrir todos os perfis primeiro
    print("\nAbrindo perfis no AdsPower...")
    for perfil in perfis[:total]:
        abrir_perfil(perfil)
        time.sleep(2)

    print(f"\nAguardando {10} segundos para os navegadores carregarem...")
    time.sleep(10)

    input("Perfis abertos! Pressione ENTER para iniciar os signups em paralelo...")

    # Executar signups em paralelo usando threads
    threads = []
    for i in range(total):
        t = threading.Thread(
            target=executar_signup_thread,
            args=(perfis[i], contas[i]['email'], contas[i]['senha'])
        )
        threads.append(t)
        t.start()
        time.sleep(1)  # Pequeno delay entre inicios

    # Aguardar todas as threads
    for t in threads:
        t.join()

    print(f"\n{'='*50}")
    print("BATCH FINALIZADO!")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
