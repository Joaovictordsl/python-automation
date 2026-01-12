import requests
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:50325"

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
        print(f"[{user_id}] Preenchendo Email: {email}")
        actions.send_keys(email).send_keys(Keys.ENTER).perform()
        actions.send_keys(Keys.TAB).perform()
        time.sleep(4)
        print(f"[{user_id}] Preenchendo Senha...")
        actions.send_keys(senha).send_keys(Keys.ENTER).perform()

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

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python tiktok_single.py <USER_ID> <EMAIL> <SENHA>")
        sys.exit(1)

    user_id = sys.argv[1]
    email = sys.argv[2]
    senha = sys.argv[3]

    executar_fluxo_tiktok(user_id, email, senha)
