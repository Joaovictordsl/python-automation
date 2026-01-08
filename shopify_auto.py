import requests
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# --- CONFIGURAÇÃO INICIAL (RECEBE DADOS DO BASH) ---
# O Bash envia: ID ($1), EMAIL ($2), SENHA ($3)
if len(sys.argv) >= 4:
    USER_ID = sys.argv[1]
    EMAIL_CONTA = sys.argv[2]
    SENHA_CONTA = sys.argv[3]
    print(f"\n🚀 Iniciando Perfil: {USER_ID}")
    print(f"📧 Conta injetada: {EMAIL_CONTA}")
    print(f"📧 Conta injetada: {SENHA_CONTA}")
else:
    print("❌ Erro: Faltam argumentos! Use: python shopify_auto.py ID EMAIL SENHA")
    sys.exit(1)

BASE_URL = "http://127.0.0.1:50325"

def executar_shopify_vinculado():
    driver = None
    try:
        # 1. Conectar ao Perfil Aberto no AdsPower
        print(f"[{USER_ID}] Conectando ao navegador...")
        res = requests.get(f"{BASE_URL}/api/v1/browser/active?user_id={USER_ID}").json()
        
        if res["code"] != 0:
            print(f"❌ [{USER_ID}] Erro: O perfil não está aberto no AdsPower!")
            return

        options = Options()
        options.add_experimental_option("debuggerAddress", res["data"]["ws"]["selenium"])
        service = Service(executable_path=res["data"]["webdriver"])
        driver = webdriver.Chrome(service=service, options=options)
        
        # Estabilidade
        driver.set_page_load_timeout(90)
        driver.implicitly_wait(10)

        # 2. Acessar Shopify
        print(f"[{USER_ID}] Acessando Shopify...")
        try:
            driver.get("https://www.shopify.com/br/free-trial")
        except:
            print(f"[{USER_ID}] Timeout inicial, tentando prosseguir...")
        
        time.sleep(8)
        driver.switch_to.default_content()
        driver.execute_script(f"document.title = 'PERFIL: {USER_ID}';")

        actions = ActionChains(driver)

        # --- ETAPA: PULAR PESQUISAS (USANDO ENTER) ---
        print(f"[{USER_ID}] Passando pelas telas iniciais...")
        for _ in range(4): # 3 perguntas + confirmação de país
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(2.5)

        # --- ETAPA: SELEÇÃO DO MÉTODO DE E-MAIL ---
        print(f"[{USER_ID}] Navegando até botão de e-mail...")
        
        # Tentativa de clique direto via XPath para ser mais seguro que TAB
        # try:
        #     btn = driver.find_element("xpath", "//button[contains(., 'e-mail')]")
        #     btn.click()
        # except:
        #     # Backup com TABs se o botão não for clicável
        #     for _ in range(3):
        #         actions.send_keys(Keys.TAB).perform()
        #         time.sleep(0.8)
        #     actions.send_keys(Keys.ENTER).perform()
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(Keys.TAB).perform()

        # --- ETAPA: PREENCHER EMAIL ---
        time.sleep(5)
        print(f"[{USER_ID}] Digitando Email...")
        
        # Garante foco e limpa campo
        # actions.click().perform()
        time.sleep(1)
        # Seleciona tudo e apaga antes de digitar
        # cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
        # actions.key_down(cmd_ctrl).send_keys('a').key_up(cmd_ctrl).send_keys(Keys.BACKSPACE).perform()
        
        # Digita o e-mail real recebido do Bash
        actions.send_keys(EMAIL_CONTA).send_keys(Keys.ENTER).perform()

        # --- ETAPA: PREENCHER SENHA ---
        
        time.sleep(1)


        print(f"[{USER_ID}] Digitando Senha...")
        actions.send_keys(SENHA_CONTA).perform()
        time.sleep(3)
        actions.send_keys(Keys.ENTER).perform()

        print(f"\n✅ [{USER_ID}] SUCESSO: {EMAIL_CONTA}")

        # Salva o log
        with open("lojas_shopify.txt", "a") as f:
            f.write(f"Email: {EMAIL_CONTA} | Perfil: {USER_ID} | Status: Sucesso\n")

        input(f"[{USER_ID}] Pressione ENTER para fechar o script...")

    except Exception as e:
        print(f"❌ [{USER_ID}] Erro crítico: {e}")

if __name__ == "__main__":
    executar_shopify_vinculado()

