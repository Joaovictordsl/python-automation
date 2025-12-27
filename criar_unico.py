import requests
import random
import string
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# --- CONFIGURAÇÃO ---
BASE_URL = "http://127.0.0.1:50325"
USER_ID = "k18bcpex" 

def gerar_dados():
    nomes = ["joao", "maria", "pedro", "ana", "carlos", "lucas", "julia", "marcos", "fernanda", "ricardo"]
    sobrenomes = ["lima", "silva", "santos", "oliveira", "souza", "pereira", "costa", "ribeiro"]
    email_base = f"{random.choice(nomes)}{random.choice(sobrenomes)}{random.randint(100,999)}"
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
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.execute_script("window.open('https://signup.live.com/signup.aspx?lic=1', '_blank');")
        
        while len(driver.window_handles) < 3:
            time.sleep(0.5)
        
        driver.switch_to.window(driver.window_handles[2])
        print("Foco na aba 3. Aguardando carregamento...")
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

        print("\n" + "="*40)
        print(f"CONTA: {email}")
        print(f"SENHA: {senha}")
        print("RESOLVA O CAPTCHA AGORA!")
        print("="*40)

        input("\nPressione ENTER no terminal após entrar na caixa de entrada para salvar e fechar...")

        with open("contas_outlook.txt", "a") as f:
            f.write(f"Email: {email} | Senha: {senha} | Perfil: {USER_ID}\n")

        requests.get(f"{BASE_URL}/api/v1/browser/stop?user_id={USER_ID}")
        print("Perfil fechado.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    executar()