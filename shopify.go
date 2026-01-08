package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
	"time"

	"github.com/tebeka/selenium"
)

// Estrutura para ler a resposta da API do AdsPower
type AdsPowerResponse struct {
	Code int    `json:"code"`
	Msg  string `json:"msg"`
	Data struct {
		Ws struct {
			Selenium string `json:"selenium"`
		} `json:"ws"`
		Webdriver string `json:"webdriver"`
	} `json:"data"`
}

const BASE_URL = "http://127.0.0.1:50325"

func executarPerfil(id, email, senha string, wg *sync.WaitGroup) {
	defer wg.Done()

	// 1. Conectar à API do AdsPower (Igual ao requests.get do Python)
	apiUrl := fmt.Sprintf("%s/api/v1/browser/active?user_id=%s", BASE_URL, id)
	resp, err := http.Get(apiUrl)
	if err != nil {
		fmt.Printf("❌ [%s] Erro ao conectar na API: %v\n", id, err)
		return
	}
	defer resp.Body.Close()

	var adspower AdsPowerResponse
	json.NewDecoder(resp.Body).Decode(&adspower)

	if adspower.Code != 0 {
		fmt.Printf("❌ [%s] Perfil não está aberto no AdsPower!\n", id)
		return
	}

	// 2. Configurar Selenium
	caps := selenium.Capabilities{
		"debuggerAddress": adspower.Data.Ws.Selenium,
	}

	// Importante: O NewRemote precisa do caminho do WebDriver que a API retornou
	driver, err := selenium.NewRemote(caps, "http://127.0.0.1:9515")
	if err != nil || driver == nil {
		fmt.Printf("❌ [%s] Erro ao iniciar driver: %v\n", id, err)
		return
	}
	defer driver.Quit()

	// 3. Execução
	fmt.Printf("🚀 [%s] Acessando Shopify para: %s\n", id, email)
	err = driver.Get("https://www.shopify.com/br/free-trial")
	if err != nil {
		fmt.Printf("❌ [%s] Erro no Get: %v\n", id, err)
		return
	}

	time.Sleep(5 * time.Second)
}
