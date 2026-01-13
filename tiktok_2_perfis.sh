#!/usr/bin/env bash

# Script para executar TikTok 2 em perfis especificos
# Uso: ./tiktok_2_perfis.sh <PERFIL1> [PERFIL2] [PERFIL3] ...
# Exemplo: ./tiktok_2_perfis.sh k188ap6w k18t5h7s

BASE_URL="http://127.0.0.1:50325"
ARQUIVO_CONTAS="contas_outlook.txt"

if [ $# -eq 0 ]; then
    echo "=========================================="
    echo "TIKTOK 2 - Selecao por Perfil"
    echo "=========================================="
    echo ""
    echo "Uso: ./tiktok_2_perfis.sh <PERFIL1> [PERFIL2] [PERFIL3] ..."
    echo ""
    echo "Exemplo:"
    echo "  ./tiktok_2_perfis.sh k188ap6w"
    echo "  ./tiktok_2_perfis.sh k188ap6w k18t5h7s k18meedg"
    echo ""
    echo "Perfis disponiveis:"
    echo "------------------------------------------"
    grep "Perfil:" "$ARQUIVO_CONTAS" | while read linha; do
        perfil=$(echo "$linha" | grep -oE 'Perfil: [^ ]+' | sed 's/Perfil: //')
        email=$(echo "$linha" | grep -oE 'Email: [^ |]+' | sed 's/Email: //')
        echo "  $perfil -> $email"
    done
    echo "=========================================="
    exit 0
fi

echo "=========================================="
echo "TIKTOK 2 - $# perfil(is) selecionado(s)"
echo "=========================================="

# Array para armazenar os perfis validos
declare -a PERFIS

i=0
for perfil in "$@"; do
    # Verifica se o perfil existe no arquivo
    if grep -q "Perfil: $perfil" "$ARQUIVO_CONTAS"; then
        PERFIS[$i]="$perfil"
        echo "  $((i+1)). Perfil: $perfil"
        ((i++)) || true
    else
        echo "  ERRO: Perfil '$perfil' nao encontrado!"
    fi
done

TOTAL=${#PERFIS[@]}

if [ $TOTAL -eq 0 ]; then
    echo ""
    echo "Nenhum perfil valido encontrado!"
    exit 1
fi

echo ""
echo "Total de perfis validos: $TOTAL"
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
