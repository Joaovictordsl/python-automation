#!/usr/bin/env bash

# Script para executar TikTok em perfis especificos
# Uso: ./tiktok_perfis.sh <PERFIL1> [PERFIL2] [PERFIL3] ...
# Exemplo: ./tiktok_perfis.sh k188ap6w k18t5h7s

BASE_URL="http://127.0.0.1:50325"
ARQUIVO_CONTAS="contas_outlook.txt"

if [ $# -eq 0 ]; then
    echo "=========================================="
    echo "TIKTOK - Selecao por Perfil"
    echo "=========================================="
    echo ""
    echo "Uso: ./tiktok_perfis.sh <PERFIL1> [PERFIL2] [PERFIL3] ..."
    echo ""
    echo "Exemplo:"
    echo "  ./tiktok_perfis.sh k188ap6w"
    echo "  ./tiktok_perfis.sh k188ap6w k18t5h7s k18meedg"
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
echo "TIKTOK - $# perfil(is) selecionado(s)"
echo "=========================================="

# Arrays para armazenar os dados
declare -a PERFIS
declare -a EMAILS
declare -a SENHAS

i=0
for perfil in "$@"; do
    # Busca a linha correspondente ao perfil
    linha=$(grep "Perfil: $perfil" "$ARQUIVO_CONTAS")

    if [ -z "$linha" ]; then
        echo "ERRO: Perfil '$perfil' nao encontrado em $ARQUIVO_CONTAS"
        continue
    fi

    EMAIL=$(echo "$linha" | grep -oE 'Email: [^ |]+' | sed 's/Email: //')
    SENHA=$(echo "$linha" | grep -oE 'Senha: [^ |]+' | sed 's/Senha: //')

    PERFIS[$i]="$perfil"
    EMAILS[$i]="$EMAIL"
    SENHAS[$i]="$SENHA"

    echo "  $((i+1)). Perfil: $perfil -> Email: $EMAIL"
    ((i++)) || true
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

read -p "Perfis abertos! Pressione ENTER para iniciar TikTok em paralelo..."

echo ""
echo "Executando TikTok em $TOTAL perfil(is) em paralelo..."
echo "=========================================="

# Cria arquivo temporario com os comandos
TMPFILE=$(mktemp)
for ((i=0; i<TOTAL; i++)); do
    echo "${PERFIS[$i]} ${EMAILS[$i]} ${SENHAS[$i]}" >> "$TMPFILE"
done

# Executa em paralelo (todos ao mesmo tempo)
cat "$TMPFILE" | xargs -P "$TOTAL" -L 1 bash -c 'python3 tiktok_single.py "$1" "$2" "$3" 2>&1' --

rm -f "$TMPFILE"

echo ""
echo "=========================================="
echo "BATCH FINALIZADO!"
echo "=========================================="
