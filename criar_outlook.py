import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Configurações
BASE_URL = "http://local.adspower.net:50325"
GROUP_ID = "team_hi6yeg" # Substitua pelo ID real

def get_profiles(group_id):
    """Busca todos os perfis de um grupo específico"""
    url = f"{BASE_URL}/api/v1/user/list?group_id={group_id}&page_size=20"
    res = requests.get(url).json()
    if res["code"] == 0:
        return res["data"]["list"]
    return []

def criar_conta(user_id):
    """Abre o navegador e executa o fluxo de criação"""
    # Abre o perfil
    open_url = f"{BASE_URL}/api/v1/browser/start?user_id={user_id}"
    resp = requests.get(open_url).json()
    
    if resp["code"] != 0:
        print(f"Erro ao abrir perfil {user_id}: {resp['msg']}")
        return

    chrome_driver = resp["data"]["webdriver"]
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
    
    driver = webdriver.Chrome(executable_path=chrome_driver, options=chrome_options)
    
    try:
        driver.get("https://signup.live.com/signup.aspx")
        print(f"Perfil {user_id} ativo. Preencha os dados e resolva o CAPTCHA.")
        
        # Aqui você pode adicionar os comandos .send_keys() para automatizar o nome/senha
        # Mas o script vai parar aqui para você intervir no CAPTCHA
        
        input("Pressione Enter no terminal APÓS terminar de criar a conta para ir ao próximo...")
        
    finally:
        # Fecha o navegador para economizar RAM e abre o próximo
        close_url = f"{BASE_URL}/api/v1/browser/stop?user_id={user_id}"
        requests.get(close_url)
        print(f"Perfil {user_id} fechado.")

# Execução principal
perfis = get_profiles(GROUP_ID)
for p in perfis:
    print(f"Iniciando automação para o perfil: {p['name']} (ID: {p['user_id']})")
    criar_conta(p['user_id'])