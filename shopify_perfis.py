import requests
import time
import sys
import os
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# --- CONFIGURACAO ---
BASE_URL = "http://127.0.0.1:50325"
ARQUIVO_CONTAS = "contas_outlook.txt"

def buscar_conta_por_perfil(perfil):
    """Busca email e senha pelo codigo do perfil no arquivo de contas."""
    try:
        if not os.path.exists(ARQUIVO_CONTAS):
            print(f"Erro: Arquivo {ARQUIVO_CONTAS} nao encontrado!")
            return None, None

        with open(ARQUIVO_CONTAS, "r") as f:
            for linha in f:
                if f"Perfil: {perfil}" in linha:
                    partes = linha.strip().split(" | ")
                    email = partes[0].replace("Email: ", "").strip()
                    senha = partes[1].replace("Senha: ", "").strip()
                    return email, senha

        print(f"Erro: Perfil '{perfil}' nao encontrado em {ARQUIVO_CONTAS}")
        return None, None
    except Exception as e:
        print(f"Erro ao ler contas: {e}")
        return None, None

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

def listar_perfis_disponiveis():
    """Lista todos os perfis disponiveis no arquivo de contas."""
    print("Perfis disponiveis:")
    print("------------------------------------------")
    try:
        with open(ARQUIVO_CONTAS, "r") as f:
            for linha in f:
                if "Perfil:" in linha:
                    partes = linha.strip().split(" | ")
                    perfil = partes[2].replace("Perfil: ", "").strip() if len(partes) > 2 else "?"
                    email = partes[0].replace("Email: ", "").strip()
                    print(f"  {perfil} -> {email}")
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")

def main():
    if len(sys.argv) < 2:
        print("=" * 50)
        print("SHOPIFY - Signup por Perfil")
        print("=" * 50)
        print("")
        print("Uso: python shopify_perfis.py <PERFIL1> [PERFIL2] [PERFIL3] ...")
        print("")
        print("Exemplo:")
        print("  python shopify_perfis.py k188ap6w")
        print("  python shopify_perfis.py k188ap6w k18t5h7s k18meedg")
        print("")
        listar_perfis_disponiveis()
        print("=" * 50)
        sys.exit(0)

    perfis_input = sys.argv[1:]

    print(f"\n{'='*50}")
    print(f"SHOPIFY SIGNUP - {len(perfis_input)} perfil(is) selecionado(s)")
    print(f"{'='*50}\n")

    # Validar e buscar dados dos perfis
    perfis = []
    contas = []

    for perfil in perfis_input:
        email, senha = buscar_conta_por_perfil(perfil)
        if email and senha:
            perfis.append(perfil)
            contas.append({"email": email, "senha": senha})
            print(f"  Perfil: {perfil} -> Email: {email}")
        else:
            print(f"  ERRO: Perfil '{perfil}' nao encontrado!")

    total = len(perfis)

    if total == 0:
        print("\nNenhum perfil valido encontrado!")
        sys.exit(1)

    print(f"\nTotal de perfis validos: {total}")
    print(f"{'='*50}")
    input("Pressione ENTER para abrir os perfis...")

    # Abrir todos os perfis primeiro
    print("\nAbrindo perfis no AdsPower...")
    for perfil in perfis:
        abrir_perfil(perfil)
        time.sleep(2)

    print(f"\nAguardando 10 segundos para os navegadores carregarem...")
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
