import requests
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# --- CONFIGURAÇÃO ---
BASE_URL = "http://127.0.0.1:50325"

if len(sys.argv) > 1:
    USER_ID = sys.argv[1]
else:
    print("Erro: Você precisa passar o User ID! Exemplo: python script.py k188brvh")
    sys.exit(1)

def obter_ultimos_dados_outlook():
    """Lê o arquivo de texto e retorna o último e-mail e senha salvos."""
    try:
        if not os.path.exists("contas_outlook.txt"):
            print("Erro: Arquivo contas_outlook.txt não encontrado!")
            return None, None
            
        with open("contas_outlook.txt", "r") as f:
            linhas = f.readlines()
            if not linhas:
                return None, None
            
            # Pega a última linha (última conta criada)
            ultima_conta = linhas[-1].strip()
            
            # Extrai o email e a senha (baseado no formato: Email: x | Senha: y)
            partes = ultima_conta.split(" | ")
            email = partes[0].replace("Email: ", "").strip()
            senha = partes[1].replace("Senha: ", "").strip()
            
            return email, senha
    except Exception as e:
        print(f"Erro ao ler arquivo de contas: {e}")
        return None, None

def executar_shopify_vinculado():
    try:
        # 1. Obter dados do Outlook
        email, senha = obter_ultimos_dados_outlook()
        if not email:
            print("Não foi possível carregar dados do Outlook. Abortando.")
            return

        print(f"Dados carregados: {email}")

        # 2. Conectar ao Perfil Aberto
        print(f"Conectando ao perfil ativo: {USER_ID}...")
        res = requests.get(f"{BASE_URL}/api/v1/browser/active?user_id={USER_ID}").json()
        
        if res["code"] != 0:
            print("Erro: O perfil precisa estar aberto no AdsPower!")
            return

        options = Options()
        options.add_experimental_option("debuggerAddress", res["data"]["ws"]["selenium"])
        service = Service(executable_path=res["data"]["webdriver"])
        driver = webdriver.Chrome(service=service, options=options)
                
        driver.set_page_load_timeout(40)
        driver.set_script_timeout(40)
        driver.implicitly_wait(10) 
        # ------------------------------------

        # 3. Ir para o Shopify
        print("Acessando Shopify...")
        driver.get("https://www.shopify.com/br/free-trial")
        time.sleep(6)
        
        actions = ActionChains(driver)

        # --- ETAPA: PERGUNTAS DE PESQUISA ---
        # print("Passando pelas pesquisas iniciais...")
        # for _ in range(3):
        #     actions.send_keys(Keys.ENTER).perform()
        #     time.sleep(2.5)


        # Confirmação de Região (Brasil)
        # print("Confirmando País...")
        # actions.send_keys(Keys.ENTER).perform()

        time.sleep(3)
        driver.switch_to.default_content() # Isso limpa erros de contexto/frames
        # --------------------------
        
        # --- ETAPA: SELEÇÃO DO MÉTODO DE E-MAIL ---
        print("Aguardando tela de métodos de cadastro...")
        time.sleep(7) 

        # Sequência de TABs para chegar em "Continuar com e-mail"
        print("Navegando até o botão de e-mail...")
        actions.send_keys(Keys.TAB).perform()
        time.sleep(0.5)
        actions.send_keys(Keys.TAB).perform()
        time.sleep(0.5)
        actions.send_keys(Keys.TAB).perform()
        time.sleep(0.5)
        actions.send_keys(Keys.ENTER).perform()
        
        # --- ETAPA: DIGITAR EMAIL E SENHA DO OUTLOOK ---
        time.sleep(4)
        print(f"Preenchendo Email do Outlook: {email}")
        actions.send_keys(email).send_keys(Keys.ENTER).perform()
        
        time.sleep(4)
        print("Preenchendo Senha do Outlook...")
        actions.send_keys(senha).send_keys(Keys.ENTER).perform()

        print("\n" + "="*40)
        print(f"LOJA VINCULADA COM SUCESSO!")
        print(f"USUÁRIO: {email}")
        print("="*40)

        # Salva o log do Shopify
        with open("lojas_shopify.txt", "a") as f:
            f.write(f"Email: {email} | Senha: {senha} | Status: Criada\n")

        input("\nCadastro Shopify finalizado! Pressione ENTER para fechar...")

    except Exception as e:
        print(f"Erro no script: {e}")

if __name__ == "__main__":
    executar_shopify_vinculado()