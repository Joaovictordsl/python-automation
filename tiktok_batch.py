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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURACAO ---
BASE_URL = "http://127.0.0.1:50325"

def carregar_contas_com_perfil(quantidade):
    """Carrega as X contas mais recentes do arquivo que tem Perfil associado."""
    contas = []
    try:
        if not os.path.exists("contas_outlook.txt"):
            print("Erro: Arquivo contas_outlook.txt nao encontrado!")
            return contas

        with open("contas_outlook.txt", "r") as f:
            linhas = f.readlines()

            # Filtra apenas linhas que tem Perfil
            linhas_com_perfil = []
            for linha in linhas:
                if "Perfil:" in linha:
                    linhas_com_perfil.append(linha.strip())

            # Pega as ultimas X linhas (mais recentes)
            linhas_recentes = linhas_com_perfil[-quantidade:] if len(linhas_com_perfil) >= quantidade else linhas_com_perfil

            for linha in linhas_recentes:
                partes = linha.split(" | ")
                conta = {}
                for parte in partes:
                    if parte.startswith("Email:"):
                        conta["email"] = parte.replace("Email:", "").strip()
                    elif parte.startswith("Senha:"):
                        conta["senha"] = parte.replace("Senha:", "").strip()
                    elif parte.startswith("Perfil:"):
                        conta["perfil"] = parte.replace("Perfil:", "").strip()

                if "email" in conta and "senha" in conta and "perfil" in conta:
                    contas.append(conta)

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

def executar_tiktok_vinculado(driver, actions, email, senha, user_id):
    """Preenche os dados do Outlook na tela do TikTok."""
    try:
        print(f"[{user_id}] Preenchendo Email do Outlook: {email}")
        actions.send_keys(email).send_keys(Keys.ENTER).perform()

        actions.send_keys(Keys.TAB).perform()

        time.sleep(4)
        print(f"[{user_id}] Preenchendo Senha do Outlook...")
        actions.send_keys(senha).send_keys(Keys.ENTER).perform()

    except Exception as e:
        print(f"[{user_id}] Erro ao preencher dados: {e}")

def executar_fluxo_tiktok(user_id, email, senha):
    """Executa o fluxo completo do TikTok para um perfil."""
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

        actions = ActionChains(driver)

        # 1. Localizar e Focar no Shopify
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if "shopify" in driver.title.lower():
                break

        # 2. Pesquisa TikTok
        print(f"[{user_id}] Iniciando busca por TikTok...")
        time.sleep(5)
        actions.send_keys(Keys.ESCAPE).perform()
        actions.key_down(Keys.COMMAND).send_keys("k").key_up(Keys.COMMAND).perform()
        time.sleep(1.5)
        actions.send_keys("tiktok").perform()
        time.sleep(5)
        actions.send_keys(Keys.ENTER).perform()
        time.sleep(3)
        actions.send_keys(Keys.ENTER).perform()

        # 3. Aguardar pagina do App e clicar no primeiro 'Instalar'
        time.sleep(6)
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if "tiktok" in driver.title.lower():
                break

        try:
            botao_instalar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-component-name="install-button"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_instalar)
            botao_instalar.click()
            print(f"[{user_id}] Botao Instalar clicado com sucesso!")
        except Exception as e:
            print(f"[{user_id}] Erro ao clicar no botao: {e}")
            try:
                driver.execute_script("arguments[0].click();", botao_instalar)
            except:
                pass

        time.sleep(10)
        driver.switch_to.window(driver.window_handles[-1])

        print(f"[{user_id}] Buscando o botao Instalar final...")

        try:
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            print(f"[{user_id}] Encontrados {len(iframes)} quadros.")

            span_final = driver.find_element(By.XPATH, "//span[contains(text(), 'Instalar') or contains(text(), 'Continuar a configuração')]")
            print(f"[{user_id}] Span 'Instalar' encontrado. Clicando...")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", span_final)
            time.sleep(3)
            driver.execute_script("arguments[0].click();", span_final)
            print(f"[{user_id}] Clique final realizado!")
            time.sleep(5)

        except Exception as e:
            print(f"[{user_id}] Nao achei o span, tentando 5 TABs: {e}")
            actions = ActionChains(driver)
            for _ in range(5):
                actions.send_keys(Keys.TAB).perform()
                time.sleep(0.3)
            actions.send_keys(Keys.ENTER).perform()

        # Botao Configurar
        try:
            driver.switch_to.default_content()
            time.sleep(2)

            iframes = driver.find_elements(By.TAG_NAME, "iframe")

            if len(iframes) > 0:
                print(f"[{user_id}] Entrando no primeiro iframe...")
                driver.switch_to.frame(0)

            print(f"[{user_id}] Aguardando o botao aparecer...")

            xpath_configurar = "//span[contains(text(), 'Continuar a configuração') or contains(text(), 'Configurar') or contains(text(), 'Instalar')]"

            botao_configurar = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, xpath_configurar))
            )

            print(f"[{user_id}] Botao localizado: '{botao_configurar.text}'")

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_configurar)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", botao_configurar)
            print(f"[{user_id}] Clique em 'Configurar' realizado!")

        except Exception as e:
            print(f"[{user_id}] Nao achei o botao: {e}")
            driver.switch_to.default_content()

        # Botao Criar novo
        try:
            driver.switch_to.default_content()
            time.sleep(2)
            iframes = driver.find_elements(By.TAG_NAME, "iframe")

            if len(iframes) > 0:
                print(f"[{user_id}] Entrando no iframe do App...")
                driver.switch_to.frame(0)

            print(f"[{user_id}] Buscando botao 'Criar novo'...")

            xpath_criar = "//button[contains(@class, 'Polaris-Link') and contains(normalize-space(), 'Criar novo')]"

            botao_criar = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, xpath_criar))
            )

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_criar)
            time.sleep(1)

            try:
                botao_criar.click()
            except:
                driver.execute_script("arguments[0].click();", botao_criar)

            print(f"[{user_id}] Sucesso: Botao 'Criar novo' clicado!")
            time.sleep(5)

        except Exception as e:
            print(f"[{user_id}] Erro ao encontrar 'Criar novo': {e}")
            driver.switch_to.default_content()
            actions = ActionChains(driver)
            for _ in range(6):
                actions.send_keys(Keys.TAB).perform()
                time.sleep(0.2)
            actions.send_keys(Keys.ENTER).perform()

        time.sleep(2)
        actions.send_keys(Keys.TAB).perform()

        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        print(f"[{user_id}] Interagindo com a aba: {driver.title}")

        # Preencher dados do Outlook
        executar_tiktok_vinculado(driver, actions, email, senha, user_id)

        # Checkbox TikTok
        try:
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for index, frame in enumerate(iframes):
                try:
                    driver.switch_to.frame(index)
                    if len(driver.find_elements(By.ID, "TikTokAds_Register-aggrement-guidline")) > 0:
                        print(f"[{user_id}] Elemento encontrado no iframe {index}")
                        break
                except Exception as e:
                    print(f"[{user_id}] Erro: {e}")

            time.sleep(2)

        except Exception as e:
            print(f"[{user_id}] Erro: {e}")

        checkbox_id = "TikTokAds_Register-aggrement-guidline"
        time.sleep(2)

        confirmacao = driver.find_element(By.ID, checkbox_id)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confirmacao)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", confirmacao)

        print(f"[{user_id}] Caixinha de confirmacao clicada com sucesso!")

        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(Keys.ENTER).perform()

        print(f"\n{'='*40}")
        print(f"[{user_id}] TIKTOK VINCULADO COM SUCESSO!")
        print(f"Email: {email}")
        print(f"{'='*40}\n")

        return True

    except Exception as e:
        print(f"[{user_id}] Erro no fluxo TikTok: {e}")
        return False

def executar_tiktok_thread(user_id, email, senha):
    """Wrapper para executar em thread."""
    executar_fluxo_tiktok(user_id, email, senha)

def main():
    if len(sys.argv) < 2:
        print("Uso: python tiktok_batch.py <QUANTIDADE>")
        print("Exemplo: python tiktok_batch.py 3")
        print("\nIsso vai vincular TikTok em 3 perfis em paralelo")
        sys.exit(1)

    quantidade = int(sys.argv[1])
    print(f"\n{'='*50}")
    print(f"TIKTOK BATCH - {quantidade} perfil(is)")
    print(f"{'='*50}\n")

    # Carregar contas com perfil associado
    print("Carregando contas do arquivo (com Perfil)...")
    contas = carregar_contas_com_perfil(quantidade)

    if len(contas) < quantidade:
        print(f"Aviso: Apenas {len(contas)} contas com Perfil disponiveis")

    total = len(contas)
    if total == 0:
        print("Erro: Nenhuma conta com Perfil disponivel!")
        sys.exit(1)

    print(f"\nVao ser usados {total} perfil(is):\n")

    # Mostrar pareamento
    for i, conta in enumerate(contas):
        print(f"  {i+1}. Perfil: {conta['perfil']} -> Email: {conta['email']}")

    print(f"\n{'='*50}")
    input("Pressione ENTER para abrir os perfis...")

    # Abrir todos os perfis primeiro
    print("\nAbrindo perfis no AdsPower...")
    for conta in contas:
        abrir_perfil(conta['perfil'])
        time.sleep(2)

    print(f"\nAguardando 10 segundos para os navegadores carregarem...")
    time.sleep(10)

    input("Perfis abertos! Pressione ENTER para iniciar o TikTok em paralelo...")

    # Executar em paralelo usando threads
    threads = []
    for conta in contas:
        t = threading.Thread(
            target=executar_tiktok_thread,
            args=(conta['perfil'], conta['email'], conta['senha'])
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
