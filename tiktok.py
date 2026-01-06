import requests
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# --- CONFIGURAÇÃO ---
BASE_URL = "http://127.0.0.1:50325"
USER_ID = "k18bcpw0" 

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
        
        # 1. Localizar e Focar no Shopify
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if "shopify" in driver.title.lower():
                break

        actions = ActionChains(driver)

        # 2. Pesquisa TikTok
        # print("Iniciando busca por TikTok...")
        # actions.key_down(Keys.COMMAND).send_keys("k").key_up(Keys.COMMAND).perform()
        # time.sleep(1.5)
        # actions.send_keys("tiktok").perform()
        # time.sleep(2)
        # actions.send_keys(Keys.ENTER).perform()
        # time.sleep(1)
        # actions.send_keys(Keys.ENTER).perform()

        # # 3. Aguardar página do App e clicar no primeiro 'Instalar'
        # time.sleep(6)
        # # Tenta focar na aba do TikTok se ela abriu separada
        # for handle in driver.window_handles:
        #     driver.switch_to.window(handle)
        #     if "tiktok" in driver.title.lower(): break

        # print("Clicando no primeiro botão de instalação...")
        # # XPath que aceita SPAN dentro de botões
        # xpath_instalar = "//*[(self::button or self::a or self::span) and (text()='Instalar' or text()='Install')]"
        
        # try:
        #     botao = driver.find_element(By.XPATH, xpath_instalar)
        #     driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao)
        #     time.sleep(1)
        #     botao.click()
        # except:
        #     print("Botão não encontrado via texto, tentando fallback de 7 TABs...")
        #     actions.send_keys(Keys.TAB * 7).send_keys(Keys.ENTER).perform()

        # # 4. A TELA FINAL (Onde está o span Polaris)
        # print("Aguardando tela final de permissões (10s)...")
        # time.sleep(10)
        
        # # FOCO NA ÚLTIMA ABA (Sempre a mais recente)
        # driver.switch_to.window(driver.window_handles[-1])
        
        # print("Buscando o botão Instalar final (Polaris span)...")
        
        # # Procuramos o SPAN específico que você mencionou
        # try:
        #     iframes = driver.find_elements(By.TAG_NAME, "iframe")
            
        #     if len(iframes) > 0:
        #         print(f"Encontrados {len(iframes)} quadros. Entrando no conteúdo do App...")
        #         # O iframe do App costuma ser o primeiro ou ter 'app' no nome
        #         driver.switch_to.frame(0) 
        #     # Este XPath busca o span com o texto exato e clica nele ou no botão pai
        #     span_final = driver.find_element(By.XPATH, "//span[contains(text(), 'Instalar') or contains(text(), 'Continuar a configuração')]")
        #     print("Span 'Instalar' encontrado. Clicando...")
        #     driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", span_final)
        #     time.sleep(1)
            
        #     # Clicar via JavaScript é mais garantido para spans do Polaris
        #     driver.execute_script("arguments[0].click();", span_final)
        #     print("Clique final realizado!")
            
        # except Exception as e:
        #     print(f"Não achei o span, tentando 5 TABs: {e}")
        #     actions = ActionChains(driver)
        #     for _ in range(5):
        #         actions.send_keys(Keys.TAB).perform()
        #         time.sleep(0.3)
        #     actions.send_keys(Keys.ENTER).perform()

        #     time.sleep(5)
        #     driver.switch_to.window(driver.window_handles[-1])

        # # --- BUSCANDO 'CONFIGURAR AGORA' ---
        # # --- PARTE PARA ENTRAR NO CONTEÚDO DO APP ---
        # print("Aguardando carregamento da interface interna do App...")
        # time.sleep(12) # Tempo maior para o App carregar o iFrame

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

        # try:

        #     iframes = driver.find_elements(By.TAG_NAME, "iframe")
            
        #     if len(iframes) > 0:
        #         print(f"Encontrados {len(iframes)} quadros. Entrando no conteúdo do App...")
        #         # O iframe do App costuma ser o primeiro ou ter 'app' no nome
        #         driver.switch_to.frame(0) 
        #         #xpath_instalar = "//*[(self::button or self::a or self::span) and (text()='Instalar' or text()='Install')]"

        #     span_final = driver.find_element(By.XPATH, "//*[(self::span or self::a or self::button) and (contains(text(), 'Criar novo') or contains(text(), 'Continuar'))]")

        #     driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", span_final)
        #     time.sleep(3)

        #     driver.execute_script("arguments[0].click();", span_final)
        #     print("Clique final realizado!")
            
        # except:
        #     print(f"Erro ao buscar: {e}")

        try:
                    # Tente isso antes de buscar o ID se o botão estiver 'invisível' para o script
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for index, frame in enumerate(iframes):
                try:
                    driver.switch_to.frame(index)
                    if len(driver.find_elements(By.ID, "TikTokAds_Register-aggrement-guidline")) > 0:
                        print(f"Elemento encontrado no iframe {index}")
                        break
                    driver.switch_to.default_content()
                except:
                    driver.switch_to.default_content()

            time.sleep(2)

            actions.send_keys(Keys.TAB).perform()

            executar_tiktok_vinculado()

            print("Buscando a caixinha de confirmação do TikTok Ads...")
    
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





        except:
            print(f"Erro ao buscar: {e}")


    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    executar_fluxo_final()