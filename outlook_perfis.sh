#!/usr/bin/env bash

# Script para criar contas Outlook em perfis especificos
# Uso: ./outlook_perfis.sh <PERFIL1> [PERFIL2] [PERFIL3] ...
# Exemplo: ./outlook_perfis.sh k188ap6w k18t5h7s

if [ $# -eq 0 ]; then
    echo "=========================================="
    echo "OUTLOOK - Criacao por Perfil"
    echo "=========================================="
    echo ""
    echo "Uso: ./outlook_perfis.sh <PERFIL1> [PERFIL2] [PERFIL3] ..."
    echo ""
    echo "Exemplo:"
    echo "  ./outlook_perfis.sh k188ap6w"
    echo "  ./outlook_perfis.sh k188ap6w k18t5h7s k18meedg"
    echo ""
    echo "NOTA: Este script CRIA novas contas Outlook para os perfis."
    echo "=========================================="
    exit 0
fi

echo "=========================================="
echo "OUTLOOK - $# perfil(is) selecionado(s)"
echo "=========================================="
echo ""

for perfil in "$@"; do
    echo "Executando criacao de conta para perfil: $perfil"
    python3 criar_unico.py "$perfil"
    echo ""
done

echo "=========================================="
echo "PROCESSO FINALIZADO!"
echo "=========================================="
