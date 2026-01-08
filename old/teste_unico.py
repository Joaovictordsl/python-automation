import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service # Importação necessária
import time

# --- CONFIGURAÇÃO ÚNICA ---
BASE_URL = "http://local.adspower.net:50325"
USER_ID = "k18bcpex" 

def testar_perfil_unico():
    print(f"A tentar abrir o perfil {USER_ID}...")
    
    try:
        res = requests.get(f"{BASE_URL}/api/v1/browser/start?user_id={USER_ID}").json()
    except Exception as e:
        print(f"Erro: Não foi possível conectar à API do AdsPower. {e}")
        return

    if res["code"] == 0:
        webdriver_path = res["data"]["webdriver"]
        debugger_address = res["data"]["ws"]["selenium"]
        
        # --- AJUSTE PARA SELENIUM 4 ---
        options = Options()
        options.add_experimental_option("debuggerAddress", debugger_address)
        
        # Criamos o objeto Service com o caminho do driver
        service = Service(executable_path=webdriver_path)
        
        # Iniciamos o driver passando o service e as options
        driver = webdriver.Chrome(service=service, options=options)
        # ------------------------------
        
        print("Sucesso! A abrir a página do Outlook...")
        driver.get("https://signup.live.com/signup.aspx")
        
        input("\nPressione Enter aqui no terminal para fechar o navegador quando terminar...")
        
        requests.get(f"{BASE_URL}/api/v1/browser/stop?user_id={USER_ID}")
        print("Perfil fechado.")
    else:
        print(f"Erro ao abrir perfil: {res['msg']}")

if __name__ == "__main__":
    testar_perfil_unico()