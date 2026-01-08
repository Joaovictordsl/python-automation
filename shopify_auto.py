import requests
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# --- CONFIGURAÇÃO INICIAL (RECEBE DADOS DO BASH) ---
# O Python agora espera 3 informações do terminal: ID, EMAIL e SENHA
if len(sys.argv) >= 4:
    USER_ID = sys.argv[1]
    EMAIL_CONTA = sys.argv[2]
    SENHA_CONTA = sys.argv[3]
    print(f"🚀 Iniciando Perfil: {USER_ID}")
    print(f"📧 Conta injetada: {EMAIL_CONTA}")
else:
    print("❌ Erro: Faltam argumentos! Use: python script.py ID EMAIL SENHA")
    sys.exit(1)

BASE_URL = "http://127.0.0.1:50325"

def executar_shopify_vinculado():
    try:
        # 1. Conectar ao Perfil Aberto no AdsPower
        print(f"[{USER_ID}] Conectando ao navegador...")
        try:
            res = requests.get(f"{BASE_URL}/api/v1/browser/active?user_id={USER_ID}").json()
            if res["code"] != 0:
                print(f"❌ [{USER_ID}] Erro: O perfil não está aberto no AdsPower!")
                return
        except Exception:
            print(f"❌ [{USER_ID}] Erro: Não foi possível conectar à API do AdsPower.")
            return

        # Configuração do Selenium
        options = Options()
        options.add_experimental_option("debuggerAddress", res["data"]["ws"]["selenium"])
        service = Service(executable_path=res["data"]["webdriver"])
        driver = webdriver.Chrome(service=service, options=options)
        
        # Configurações de estabilidade (Crucial para xargs)
        driver.set_page_load_timeout(60)
        driver.set_script_timeout(60)
        driver.implicitly_wait(10)

        # 2. Ir para o Shopify
        print(f"[{USER_ID}] Acessando Shopify...")
        driver.get("https://www.shopify.com/br/free-trial")
        
        # Adiciona o título na janela para você se achar visualmente
        driver.execute_script(f"document.title = '{USER_ID} - {EMAIL_CONTA}';")
        time.sleep(6)
        
        actions = ActionChains(driver)

        # --- ETAPA: PESQUISAS INICIAIS ---

        actions.send_keys(Keys.TAB).perform()

        time.sleep(2)

        # print(f"[{USER_ID}] Passando pelas pesquisas...")
        # driver.switch_to.default_content() # Garante o foco na página
        # for _ in range(3):
        #     actions.send_keys(Keys.ENTER).perform()
        #     time.sleep(2)

        # # Confirmando País
        # print(f"[{USER_ID}] Confirmando País...")
        # actions.send_keys(Keys.ENTER).perform()

        # # Reset de foco para evitar erro "no such execution context"
        # time.sleep(3)
        # driver.switch_to.default_content() 
        
        # --- ETAPA: SELEÇÃO DO MÉTODO DE E-MAIL ---
        print(f"[{USER_ID}] Navegando até opção de e-mail...")
        time.sleep(5) 
        
        # TABs mais lentos para garantir que o navegador processe
        # for _ in range(3):
        #     actions.send_keys(Keys.TAB).perform()
        #     time.sleep(1) # Delay entre TABs
        
        # actions.send_keys(Keys.ENTER).perform()
        
        # --- ETAPA: PREENCHER DADOS (Aqui usamos as variáveis injetadas) ---
        time.sleep(4)
        print(f"[{USER_ID}] Preenchendo Email: {EMAIL_CONTA}")
        actions.send_keys(EMAIL_CONTA).send_keys(Keys.ENTER).perform()
        
        time.sleep(4)
        print(f"[{USER_ID}] Preenchendo Senha...")
        actions.send_keys(SENHA_CONTA).send_keys(Keys.ENTER).perform()

        print("\n" + "="*40)
        print(f"✅ [{USER_ID}] SUCESSO! LOJA VINCULADA.")
        print(f"📧 {EMAIL_CONTA}")
        print("="*40)

        # Salva o log do Shopify
        with open("lojas_shopify.txt", "a") as f:
            f.write(f"Email: {EMAIL_CONTA} | Senha: {SENHA_CONTA} | Perfil: {USER_ID} | Status: Criada\n")

        input(f"\n[{USER_ID}] Pressione ENTER para finalizar este perfil...")

    except Exception as e:
        print(f"❌ [{USER_ID}] Erro crítico: {e}")

if __name__ == "__main__":
    executar_shopify_vinculado()