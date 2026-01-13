#!/usr/bin/env bash

# Script para executar TikTok 2 em multiplos perfis em paralelo
# Uso: ./tiktok_2_parallel.sh <QUANTIDADE>

QUANTIDADE=${1:-3}
BASE_URL="http://127.0.0.1:50325"

echo "=========================================="
echo "TIKTOK 2 PARALELO - $QUANTIDADE perfil(is)"
echo "=========================================="

# Extrai as ultimas N contas que tem Perfil associado
echo "Carregando contas com perfil..."
CONTAS=$(grep "Perfil:" contas_outlook.txt | tail -n "$QUANTIDADE")

if [ -z "$CONTAS" ]; then
    echo "Erro: Nenhuma conta com Perfil encontrada!"
    exit 1
fi

# Array para armazenar os perfis
declare -a PERFIS

i=0
while IFS= read -r linha; do
    PERFIL=$(echo "$linha" | grep -oE 'Perfil: [^ ]+' | sed 's/Perfil: //')

    PERFIS[$i]="$PERFIL"

    echo "  $((i+1)). Perfil: $PERFIL"
    ((i++)) || true
done <<< "$CONTAS"

TOTAL=${#PERFIS[@]}
echo ""
echo "Total de perfis: $TOTAL"
echo "=========================================="

read -p "Pressione ENTER para abrir os perfis no AdsPower..."

# Abre todos os perfis primeiro
echo ""
echo "Abrindo perfis..."
for perfil in "${PERFIS[@]}"; do
    echo "Abrindo perfil: $perfil"
    curl -s "$BASE_URL/api/v1/browser/start?user_id=$perfil" > /dev/null
    sleep 2
done

echo ""
echo "Aguardando 10 segundos para os navegadores carregarem..."
sleep 10

read -p "Perfis abertos! Pressione ENTER para iniciar TikTok 2 em paralelo..."

echo ""
echo "Executando TikTok 2 em $TOTAL perfil(is) em paralelo..."
echo "=========================================="

# Executa em paralelo (todos ao mesmo tempo)
printf '%s\n' "${PERFIS[@]}" | xargs -P "$TOTAL" -I {} python3 tiktok_2.py {}

echo ""
echo "=========================================="
echo "BATCH FINALIZADO!"
echo "=========================================="
