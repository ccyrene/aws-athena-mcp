# Configuração do AWS Athena MCP no Cursor

## Pré-requisitos

1. Certifique-se de ter Python 3.8+ instalado
2. Clone este repositório
3. Configure o ambiente virtual e instale as dependências:

```bash
cd /home/rafael/projects/aws-athena-mcp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Configuração no Cursor

Adicione a seguinte configuração ao seu arquivo de configuração MCP do Cursor:

### Opção 1: Usando o script wrapper (RECOMENDADO)

```json
{
  "mcpServers": {
    "athena-connector": {
      "command": "/home/rafael/projects/aws-athena-mcp/run_server.sh",
      "env": {
        "AWS_REGION": "us-east-1",
        "AWS_S3_OUTPUT_LOCATION": "s3://seu-bucket/athena-results/"
      }
    }
  }
}
```

### Opção 2: Especificando o Python do venv diretamente

```json
{
  "mcpServers": {
    "athena-connector": {
      "command": "/home/rafael/projects/aws-athena-mcp/venv/bin/python",
      "args": ["/home/rafael/projects/aws-athena-mcp/main.py"],
      "env": {
        "AWS_REGION": "us-east-1",
        "AWS_S3_OUTPUT_LOCATION": "s3://seu-bucket/athena-results/"
      }
    }
  }
}
```

## Variáveis de Ambiente

### Obrigatória
- `AWS_S3_OUTPUT_LOCATION`: Local no S3 onde os resultados das queries serão armazenados

### Opcionais para Autenticação

#### Usando credenciais diretas:
```json
"env": {
  "AWS_ACCESS_KEY_ID": "AKIA...",
  "AWS_SECRET_ACCESS_KEY": "sua-chave-secreta",
  "AWS_REGION": "us-east-1",
  "AWS_S3_OUTPUT_LOCATION": "s3://seu-bucket/athena-results/"
}
```

#### Usando perfil AWS:
```json
"env": {
  "AWS_PROFILE": "seu-perfil-aws",
  "AWS_REGION": "us-east-1",
  "AWS_S3_OUTPUT_LOCATION": "s3://seu-bucket/athena-results/"
}
```

#### Usando credenciais do sistema (IAM role, etc):
```json
"env": {
  "AWS_REGION": "us-east-1",
  "AWS_S3_OUTPUT_LOCATION": "s3://seu-bucket/athena-results/"
}
```

## Solução de Problemas

### Erro: ModuleNotFoundError: No module named 'mcp'

Este erro ocorre quando o Python não está usando o ambiente virtual correto. Certifique-se de:

1. Ter criado e ativado o ambiente virtual conforme instruções acima
2. Usar o script `run_server.sh` ou o caminho completo para o Python do venv
3. Verificar se as dependências foram instaladas corretamente:

```bash
source venv/bin/activate
pip list | grep mcp
# Deve mostrar: mcp-python 0.1.x
```

### Erro: Permission denied

Se receber erro de permissão ao executar o script:

```bash
chmod +x /home/rafael/projects/aws-athena-mcp/run_server.sh
```

### Verificando se funciona

Para testar manualmente se o servidor está funcionando:

```bash
cd /home/rafael/projects/aws-athena-mcp
./run_server.sh
# Ou
source venv/bin/activate
python main.py
```

O servidor deve iniciar sem erros e aguardar conexões.