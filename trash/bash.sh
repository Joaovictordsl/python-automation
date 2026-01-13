#!/usr/bin/env bash

paste <(python3 user_ids.py | head -n 2) <(tail -n 2 contas_outlook.txt | tail -r | awk -F' \\| ' '{gsub(/Email: /,"",$1); gsub(/Senha: /,"",$2); print $1, $2}') | xargs -P 1 -L 1 sh -c 'python3 shopify_auto.py "$1" "$2" "$3"' --
