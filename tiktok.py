import requests
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    
def executar_tiktok_vinculado():
    try:

        
        # 1. Obter dados do Outlook
        email, senha = obter_ultimos_dados_outlook()
        if not email:
            print("Não foi possível carregar dados do Outlook. Abortando.")
            return
        
        res = requests.get(f"{BASE_URL}/api/v1/browser/active?user_id={USER_ID}").json()
        
        options = Options()
        options.add_experimental_option("debuggerAddress", res["data"]["ws"]["selenium"])
        service = Service(executable_path=res["data"]["webdriver"])
        driver = webdriver.Chrome(service=service, options=options)
        
        actions = ActionChains(driver)

        # actions.send_keys(Keys.TAB).perform()
        #driver.switch_to.window(driver.window_handles[-1])

        print(f"Preenchendo Email do Outlook: {email}")
        actions.send_keys(email).send_keys(Keys.ENTER).perform()
        
        actions.send_keys(Keys.TAB).perform()

        time.sleep(4)
        print("Preenchendo Senha do Outlook...")
        actions.send_keys(senha).send_keys(Keys.ENTER).perform()

    except Exception as e:
        print(f"Erro ao ler arquivo de contas: {e}")
        return None, None

def executar_fluxo_final():
    try:
        print(f"Conectando ao perfil {USER_ID}...")
        res = requests.get(f"{BASE_URL}/api/v1/browser/active?user_id={USER_ID}").json()
        
        options = Options()
        options.add_experimental_option("debuggerAddress", res["data"]["ws"]["selenium"])
        service = Service(executable_path=res["data"]["webdriver"])
        driver = webdriver.Chrome(service=service, options=options)
        
        # # 1. Localizar e Focar no Shopify
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if "shopify" in driver.title.lower():
                break

        actions = ActionChains(driver)

        # 2. Pesquisa TikTok
        print("Iniciando busca por TikTok...")
        time.sleep(5)
        actions.send_keys(Keys.ESCAPE).perform()
        actions.key_down(Keys.COMMAND).send_keys("k").key_up(Keys.COMMAND).perform()
        time.sleep(1.5)
        actions.send_keys("tiktok").perform()
        time.sleep(5)
        actions.send_keys(Keys.ENTER).perform()
        time.sleep(1)
        actions.send_keys(Keys.ENTER).perform()

        # # 3. Aguardar página do App e clicar no primeiro 'Instalar'
        time.sleep(6)
        # Tenta focar na aba do TikTok se ela abriu separada
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if "tiktok" in driver.title.lower(): break

    except Exception as e:
        print(f"Erro ao clicar no botão: {e}")

        print("Clicando no primeiro botão de instalação...")

    try:
        botao_instalar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-component-name="install-button"]'))
        )
        
        # 2. Scroll para garantir que o botão está na visão
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_instalar)
        
        # 3. Clique
        botao_instalar.click()
        print("Botão Instalar clicado com sucesso!")

    except Exception as e:
        print(f"Erro ao clicar no botão: {e}")
    # Caso o clique normal falhe por algo estar na frente, tente via JavaScript:
        driver.execute_script("arguments[0].click();", botao_instalar)

            #################################
            # XPath que aceita SPAN dentro de botões
            # xpath_instalar = "//*[(self::button or self::a or self::span) and (text()='Instalar' or text()='Install')]"
            
            # try:
            #     botao = driver.find_element(By.XPATH, xpath_instalar)
            #     driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao)
            #     time.sleep(1)
            #     botao.click()
            # except:
            #     print("Botão não encontrado via texto, tentando fallback de 7 TABs...")
            #     actions.send_keys(Keys.TAB * 7).send_keys(Keys.ENTER).perform()

            #############################

            # # 4. A TELA FINAL (Onde está o span Polaris)
            # print("Aguardando tela final de permissões (10s)...")
    time.sleep(10)
            
            # # FOCO NA ÚLTIMA ABA (Sempre a mais recente)
    driver.switch_to.window(driver.window_handles[-1])
            
    print("Buscando o botão Instalar final (Polaris span)...")
            
            # # Procuramos o SPAN específico que você mencionou
    try:
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
                
            # if len(iframes) > 0:
            print(f"Encontrados {len(iframes)} quadros. Entrando no conteúdo do App...")
                # O iframe do App costuma ser o primeiro ou ter 'app' no nome
                # driver.switch_to.frame(0) 
                # Este XPath busca o span com o texto exato e clica nele ou no botão pai
            span_final = driver.find_element(By.XPATH, "//span[contains(text(), 'Instalar') or contains(text(), 'Continuar a configuração')]")
            print("Span 'Instalar' encontrado. Clicando...")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", span_final)
            time.sleep(3)
                
                # Clicar via JavaScript é mais garantido para spans do Polaris
            driver.execute_script("arguments[0].click();", span_final)
            print("Clique final realizado!")
            time.sleep(5)

            # else:
            #     print("Nenhum iframe encontrado, buscando na página principal...")
                    # Lógica de busca caso não haja iframe ficaria aqui
                
    except Exception as e:
            print(f"Não achei o span, tentando 5 TABs: {e}")
            actions = ActionChains(driver)
            for _ in range(5):
                actions.send_keys(Keys.TAB).perform()
                time.sleep(0.3)
            actions.send_keys(Keys.ENTER).perform()
            #     time.sleep(5)
            #     driver.switch_to.window(driver.window_handles[-1])
    try:
        # 1. Primeiro, voltamos para o topo da página para garantir um ponto de partida limpo
        driver.switch_to.default_content()
        time.sleep(2)

        # 2. Buscamos os iframes. O conteúdo do App da Shopify SEMPRE fica dentro de um iframe.
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        
        if len(iframes) > 0:
            print(f"Encontrados {len(iframes)} quadros. Entrando no primeiro...")
            driver.switch_to.frame(0) # Entra no quadro onde o botão realmente vive
        else:
            print("Aviso: Nenhum iframe encontrado, buscando na página principal...")

        print("Aguardando o botão aparecer (máximo 15s)...")
        
        # 3. Usamos o WebDriverWait em vez de find_element. 
        # Ele vai tentar encontrar o botão várias vezes durante 15 segundos.
        xpath_configurar = "//span[contains(text(), 'Continuar a configuração') or contains(text(), 'Configurar') or contains(text(), 'Instalar')]"            
        
        botao_configurar = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, xpath_configurar))
        )
            
        print(f"Botão localizado: '{botao_configurar.text}'")
        
        # 4. Scroll e Clique via JavaScript (mais seguro para elementos dentro de frames)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_configurar)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", botao_configurar)
        print("Clique em 'Configurar agora/Instalar' realizado com sucesso!")

    except Exception as e:
        print(f"Não achei o botão: {e}")
        # Se falhar, voltamos ao padrão antes de qualquer outra tentativa manual
        driver.switch_to.default_content()

        # try:
        #     # 1. Tenta encontrar o iFrame do aplicativo
        #     # O conteúdo do App não fica na página principal, fica dentro de um iframe
        #     iframes = driver.find_elements(By.TAG_NAME, "iframe")
            
        #     if len(iframes) > 0:
        #         print(f"Encontrados {len(iframes)} quadros. Entrando no conteúdo do App...")
        #         # O iframe do App costuma ser o primeiro ou ter 'app' no nome
        #         driver.switch_to.frame(0) 
            
        #     # 2. Agora que estamos 'dentro' do App, buscamos o botão
        #         xpath_configurar = "//span[contains(normalize-space(), 'Configurar') or contains(normalize-space(), 'Continuar') or contains(normalize-space(), 'Instalar')]"            
        #     # Espera o elemento ficar clicável dentro do frame
        #     botao_configurar = driver.find_element(By.XPATH, xpath_configurar)
            
        #     print(f"Botão localizado dentro do App: '{botao_configurar.text}'")
        #     driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_configurar)
        #     time.sleep(1)
        #     driver.execute_script("arguments[0].click();", botao_configurar)
        #     print("Clique em 'Configurar agora' realizado com sucesso!")

        #     # 3. Volta para o foco principal da página (opcional)
        #     driver.switch_to.default_content()

        # except Exception as e:
        #     print(f"Erro ao buscar no iFrame: {e}")
        #     # Se falhou, volta para o padrão e tenta os TABs
        #     driver.switch_to.default_content()
        #     print("Tentando alternativa via TAB...")
        #     driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE) # ESC para fechar IA
        #     time.sleep(1)
        #     # ... seus TABs aqui ...

    try:
        # 1. Garante que está no iframe certo
        driver.switch_to.default_content()
        time.sleep(2)
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        
        if len(iframes) > 0:
            print(f"Entrando no iframe do App...")
            driver.switch_to.frame(0)

        # 2. Busca o botão "Criar novo" usando CSS Selector (mais rápido) 
        # ou XPath (mais preciso para texto)
        print("Buscando botão 'Criar novo'...")
        
        # XPath que ignora espaços extras em volta do texto
        xpath_criar = "//button[contains(@class, 'Polaris-Link') and contains(normalize-space(), 'Criar novo')]"
        
        botao_criar = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, xpath_criar))
        )

        # 3. Ação de clicar
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_criar)
        time.sleep(1)
        
        try:
            botao_criar.click()
        except:
            # Se o clique normal falhar, o JavaScript força o clique
            driver.execute_script("arguments[0].click();", botao_criar)
            
        print("Sucesso: Botão 'Criar novo' clicado!")
        time.sleep(5)

    except Exception as e:
        print(f"Erro ao encontrar 'Criar novo': {e}")
        # Se falhar, tenta o plano B (TABs)
        driver.switch_to.default_content()
        actions = ActionChains(driver)
        # Tente 4 a 6 TABs dependendo de onde o foco parou
        for _ in range(6):
            actions.send_keys(Keys.TAB).perform()
            time.sleep(0.2)
        actions.send_keys(Keys.ENTER).perform()



    #actions.send_keys(Keys.ESCAPE).perform()
    time.sleep(2)

    #driver.switch_to.window(driver.window_handles[-1])

    actions.send_keys(Keys.TAB).perform()

    time.sleep(3) # Espera a aba carregar
    driver.switch_to.window(driver.window_handles[-1])
    print(f"Interagindo com a aba: {driver.title}")

    executar_tiktok_vinculado()
        
    try:
                    # Tente isso antes de buscar o ID se o botão estiver 'invisível' para o script
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for index, frame in enumerate(iframes):
                try:
                    driver.switch_to.frame(index)
                    if len(driver.find_elements(By.ID, "TikTokAds_Register-aggrement-guidline")) > 0:
                        print(f"Elemento encontrado no iframe {index}")
                        break
                    
                except Exception as e:
                    print(f"Erro: {e}")

            time.sleep(2)

    except Exception as e:
            print(f"Erro: {e}")


        #     print("Buscando a caixinha de confirmação do TikTok Ads...")
    
            # Localiza pelo ID específico que você forneceu
            # Se estiver dentro de um iframe, lembre-se de usar driver.switch_to.frame() antes
    checkbox_id = "TikTokAds_Register-aggrement-guidline"
            
            # Espera curta para garantir que o elemento existe
    time.sleep(2)
            
    confirmacao = driver.find_element(By.ID, checkbox_id)
            
            # Rola até a caixinha para garantir que está visível
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confirmacao)
    time.sleep(1)
            
            # Realiza o clique via JavaScript (ignora se houver sobreposição de outros elementos)
    driver.execute_script("arguments[0].click();", confirmacao)
            
    print("Caixinha de confirmação clicada com sucesso!")
                    
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()

    actions.send_keys(Keys.ENTER).perform()



    # except Exception as e:
    #     print(f"Erro: {e}")

if __name__ == "__main__":
    executar_fluxo_final()