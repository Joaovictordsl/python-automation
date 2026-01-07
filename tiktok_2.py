import requests
import time
import os
import random
import sys
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

BASE_URL = "http://127.0.0.1:50325"

if len(sys.argv) > 1:
    USER_ID = sys.argv[1]
else:
    print("Erro: Você precisa passar o User ID! Exemplo: python script.py k188brvh")
    sys.exit(1)

def gerar_telefone_bh():
    # DDD de Belo Horizonte
    ddd = "31"
    
    # O primeiro dígito do número é sempre 9
    # O segundo dígito para celulares geralmente varia entre 7, 8 e 9
    segundo_digito = random.choice([7, 8, 9])
    
    # Gera os outros 7 dígitos aleatórios
    restante = "".join([str(random.randint(0, 9)) for _ in range(7)])
    
    # Monta o número completo
    telefone_completo = f"{ddd}9{segundo_digito}{restante}"
    
    return telefone_completo


def executar_segunda_parte():
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

    
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
            
        if len(iframes) > 0:
            print(f"Encontrados {len(iframes)} quadros. Entrando no conteúdo do App...")
                # O iframe do App costuma ser o primeiro ou ter 'app' no nome
            driver.switch_to.frame(0) 
            # Este XPath busca o span com o texto exato e clica nele ou no botão pai
        span_final = driver.find_element(By.XPATH, "//*[(self::span or self::a or self::button) and (contains(text(), 'Criar novo') or contains(text(), 'Continuar'))]")

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", span_final)
        time.sleep(3)

        driver.execute_script("arguments[0].click();", span_final)
        print("Clique final realizado!")
            
            # Clicar via JavaScript é mais garantido para spans do Polaris
        driver.execute_script("arguments[0].click();", span_final)
        print("Clique final realizado!")

        time.sleep(1)

        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(Keys.TAB).perform()
            
        time.sleep(1)

#         # Gera o número


    except Exception as e:
        print(f"Erro ao preencher telefone: {e}")

# Localiza o campo de telefone (ajuste o seletor conforme necessário)
    try:
        telefone = gerar_telefone_bh()

        actions.send_keys(telefone).perform()
        print(f"Telefone {telefone} preenchido com sucesso!")
    


    except Exception as e:
        print(f"Não achei o span, tentando 5 TABs: {e}")

    # 1. Voltar para o topo da página para garantir que o loop de iframes comece do zero
    driver.switch_to.default_content()
    time.sleep(2)
    
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"Analisando {len(iframes)} iframes para encontrar o checkbox...")

    for index, frame in enumerate(iframes):
        try:
            driver.switch_to.frame(index)
            
            # Buscamos o SPAN que você viu, mas também o 'label' ou 'span' pai dele
            # O seletor abaixo tenta o span direto ou qualquer container de checkbox
            seletor_checkbox = ".byted-checkbox-icon, .byted-checkbox, .ac-account-register-agreement__checkbox"
            checkboxes = driver.find_elements(By.CSS_SELECTOR, seletor_checkbox)
            
            if len(checkboxes) > 0:
                print(f"Checkbox localizado no iFrame {index}. Tentando clicar...")
                
                # Pegamos o primeiro encontrado
                alvo = checkboxes[0]
                
                # Move a tela para ele
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", alvo)
                time.sleep(1)
                
                # Clique via JavaScript (força o evento mesmo se o span for pequeno)
                driver.execute_script("arguments[0].click();", alvo)
                
                print("Clique realizado!")
                # NÃO damos switch_to.default_content() aqui para continuar no mesmo frame 
                # onde os próximos botões (como Confirmar) provavelmente estão.
                break 
            
            # Se não achou neste frame, volta para o topo para tentar o próximo
            driver.switch_to.default_content()
            
        except Exception as e:
            print(f"Erro no iFrame {index}: {e}")
            driver.switch_to.default_content()
        


    try:
        time.sleep(2)

        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(Keys.TAB).perform()   

        actions.send_keys(Keys.ENTER).perform()
    
    except Exception as e:
        print(f"Não achei o span, tentando 5 TABs: {e}")

    try:
        time.sleep(5)
        
        # Tenta encontrar em todos os contextos (Página principal e iFrames)
        def clicar_confirmar(driver):
            xpath = "//*[(self::button or self::a or self::span) and contains(normalize-space(), 'Confirmar')]"
            
            # 1. Tenta na página principal
            try:
                botao = driver.find_element(By.XPATH, xpath)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", botao)
                print("Botão Confirmar clicado na página principal!")
                return True
            except:
                pass

            # 2. Tenta dentro dos iFrames
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for index, frame in enumerate(iframes):
                try:
                    driver.switch_to.frame(index)
                    botao = driver.find_element(By.XPATH, xpath)
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", botao)
                    print(f"Botão Confirmar clicado dentro do iFrame {index}!")
                    return True
                except:
                    print("Botão Confirmar não foi encontrado em nenhum contexto.")

            return False

        if not clicar_confirmar(driver):
            print("Botão Confirmar não foi encontrado em nenhum contexto.")


    except Exception as e:
        print(f"Erro geral: {e}")

    try:

        time.sleep(3)
        actions.send_keys(Keys.TAB).perform()
        actions.send_keys(Keys.ENTER).perform()


    except:

        print(f"Erro geral: {e}")


if __name__ == "__main__":
    executar_segunda_parte()
