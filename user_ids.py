import requests
import sys

def buscar_ids_joao_lima():
    url = "http://localhost:50325/api/v1/user/list"
    # Nome exato conforme seu grupo
    NOME_GRUPO = "JOAO LIMA 03 - 21/12/25"
    
    params = {"page_size": 100} 
    
    try:
        response = requests.get(url, params=params).json()
        
        if response["code"] == 0:
            perfis = response["data"]["list"]
            # Filtra apenas o grupo desejado
            ids = [p["user_id"] for p in perfis if p.get("group_name") == NOME_GRUPO]
            
            if ids:
                # Imprime um por linha para o Bash ler corretamente
                print("\n".join(ids))
            else:
                # Se não achar nada, avisa no erro padrão (stderr) para não sujar o pipe
                print(f"Nenhum ID encontrado no grupo: {NOME_GRUPO}", file=sys.stderr)
        else:
            print(f"Erro na API: {response['msg']}", file=sys.stderr)
            
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)

if __name__ == "__main__":
    buscar_ids_joao_lima()