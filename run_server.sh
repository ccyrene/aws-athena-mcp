#!/bin/bash
# Script wrapper para executar o servidor MCP com o ambiente virtual ativado

# Obtém o diretório do script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Verifica se o ambiente virtual existe
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Erro: Ambiente virtual não encontrado em $SCRIPT_DIR/venv" >&2
    echo "Por favor, crie o ambiente virtual primeiro:" >&2
    echo "  cd $SCRIPT_DIR" >&2
    echo "  python3 -m venv venv" >&2
    echo "  source venv/bin/activate" >&2
    echo "  pip install -r requirements.txt" >&2
    echo "  pip install -e ." >&2
    exit 1
fi

# Ativa o ambiente virtual e executa o servidor
source "$SCRIPT_DIR/venv/bin/activate"
exec python "$SCRIPT_DIR/main.py" "$@"