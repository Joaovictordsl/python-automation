import requests
import random
import string
import time
import sys 
import os
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


def gerar_dados():
    nomes = ["joao", "maria", "pedro", "ana", "carlos", "lucas", "julia", "marcos", "fernanda", "ricardo"]
    sobrenomes = ["lima", "silva", "santos", "oliveira", "souza", "pereira", "costa", "ribeiro"]
    email_base = f"{random.choice(nomes)}{random.choice(sobrenomes)}{random.randint(1000,9999)}"
    email_completo = f"{email_base}@outlook.com"
    senha = "".join(random.choices(string.ascii_letters + string.digits, k=10)) + "A1!"
    return email_completo, senha

def executar():
    try:
        print(f"Iniciando Perfil {USER_ID}...")
        res = requests.get(f"{BASE_URL}/api/v1/browser/start?user_id={USER_ID}").json()
        
        service = Service(executable_path=res["data"]["webdriver"])
        options = Options()
        options.add_experimental_option("debuggerAddress", res["data"]["ws"]["selenium"])
        
        # Prefs de popups
        prefs = {
            "profile.default_content_setting_values.popups": 1,
            "profile.default_content_setting_values.notifications": 1
        }
        options.add_experimental_option("prefs", prefs)
        
        driver = webdriver.Chrome(service=service, options=options)
        
        # --- ALTERAÇÃO AQUI ---
        # Em vez de window.open (que abre a 2ª aba), use o .get na aba atual
        print("Navegando para o registro do Outlook...")
        driver.get('https://signup.live.com/signup.aspx?lic=1')
        
        # Como você não abriu uma aba nova, você já está na aba correta (index 0)
        # Se quiser garantir o foco nela:
        driver.switch_to.window(driver.window_handles[0])
        
        print("Aguardando carregamento...")
        time.sleep(8) 
        
        email, senha = gerar_dados()
        actions = ActionChains(driver)

        # --- ETAPA 1: EMAIL ---
        print(f"Digitando Email: {email}")
        actions.send_keys(email).send_keys(Keys.ENTER).perform()
        
        # --- ETAPA 2: SENHA ---
        time.sleep(3) 
        print(f"Digitando Senha: {senha}")
        actions.send_keys(senha).send_keys(Keys.ENTER).perform()

        # --- ETAPA 3: DATA DE NASCIMENTO (AGORA VEM PRIMEIRO) ---
        time.sleep(3)
        print("Preenchendo Data (Dia 10, Abril, 1993)...")
        # Pais (TAB) -> Dia -> TAB -> Mes -> TAB -> Ano -> ENTER
        actions.send_keys(Keys.TAB).send_keys("10").send_keys(Keys.TAB).perform()
        time.sleep(0.5)
        actions.send_keys("a").send_keys(Keys.TAB).perform() 
        time.sleep(0.5)
        actions.send_keys("1993").send_keys(Keys.ENTER).perform()

        # --- ETAPA 4: NOME E SOBRENOME (DEPOIS DA DATA) ---
        time.sleep(3) 
        print("Preenchendo Nome, TAB, Sobrenome e ENTER...")
        actions.send_keys("Gabriel").send_keys(Keys.TAB).send_keys("Silva").send_keys(Keys.ENTER).perform()

        # Tente salvar logo após gerar os dados ou antes do input
        try:
            # Usar 'a' (append) é seguro, mas o flush garante a saída do buffer
            with open("contas_outlook.txt", "a", encoding="utf-8") as f:
                f.write(f"Email: {email} | Senha: {senha} | Perfil: {USER_ID}\n")
                f.flush() # Força a gravação física no disco
                os.fsync(f.fileno()) # Garante que o sistema operacional liberou a escrita
            print(f"✅ [Perfil {USER_ID}] Salvo com sucesso.")
        except Exception as e:
            print(f"❌ [Perfil {USER_ID}] Erro ao salvar no arquivo: {e}")

        print("\n" + "="*40)
        print(f"CONTA: {email}")
        print(f"SENHA: {senha}")
        print("RESOLVA O CAPTCHA AGORA!")
        print("="*40)

        input("\nPressione ENTER no terminal após entrar na caixa de entrada para salvar e fechar...")

        # with open("contas_outlook.txt", "a") as f:
        #     f.write(f"Email: {email} | Senha: {senha} | Perfil: {USER_ID}\n")

        # requests.get(f"{BASE_URL}/api/v1/browser/stop?user_id={USER_ID}")
        # print("Perfil fechado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    executar()