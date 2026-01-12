#!/usr/bin/env bash

# Script para executar TikTok em multiplos perfis em paralelo
# Uso: ./tiktok_parallel.sh <QUANTIDADE>

QUANTIDADE=${1:-3}
BASE_URL="http://127.0.0.1:50325"

echo "=========================================="
echo "TIKTOK PARALELO - $QUANTIDADE perfil(is)"
echo "=========================================="

# Extrai as ultimas N contas que tem Perfil associado
echo "Carregando contas com perfil..."
CONTAS=$(grep "Perfil:" contas_outlook.txt | tail -n "$QUANTIDADE")

if [ -z "$CONTAS" ]; then
    echo "Erro: Nenhuma conta com Perfil encontrada!"
    exit 1
fi

# Arrays para armazenar os dados
declare -a PERFIS
declare -a EMAILS
declare -a SENHAS

i=0
while IFS= read -r linha; do
    PERFIL=$(echo "$linha" | grep -oE 'Perfil: [^ ]+' | sed 's/Perfil: //')
    EMAIL=$(echo "$linha" | grep -oE 'Email: [^ |]+' | sed 's/Email: //')
    SENHA=$(echo "$linha" | grep -oE 'Senha: [^ |]+' | sed 's/Senha: //')

    PERFIS[$i]="$PERFIL"
    EMAILS[$i]="$EMAIL"
    SENHAS[$i]="$SENHA"

    echo "  $((i+1)). Perfil: $PERFIL -> Email: $EMAIL"
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
