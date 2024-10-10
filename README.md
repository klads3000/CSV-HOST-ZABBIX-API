# CSV-HOST-ZABBIX-API
# Zabbix Host Creation Script

Este script Python automatiza a criação de hosts no Zabbix utilizando a API JSON-RPC. Ele lê informações de um arquivo CSV e cria hosts SNMPv2 a partir dos dados fornecidos.

## Pré-requisitos

- Python
- Bibliotecas: `requests`, `json`, `csv`
- Acesso à API do Zabbix

## Configuração

Antes de executar o script, você deve ajustar as seguintes configurações:

1. **URL do Zabbix**: Altere a variável `url` para o endpoint correto da sua instância do Zabbix.
2. **Credenciais**: Insira suas credenciais de autenticação (usuário e senha) nas variáveis `username` e `password`.
3. **Template e Grupo**: Ajuste os IDs do template e do grupo no script (`template_id` e `group_id`). (ESSAS INFORMAÇÕES ESTÃO NA URL DO TEMPLATE OU DO GRUPO)
4. **Arquivo CSV**: Altere o caminho do arquivo CSV para o que contém os dados dos hosts a serem criados.

### Estrutura do CSV

O CSV deve conter as seguintes colunas:

- `Circuito`: Nome do host que será criado.
- `IP De Wan`: Endereço IP do host.
- `STATUS`: Status do host (deve incluir "Migrado" para ser considerado).
- `EQUIPAMENTO`: Tipo de equipamento (deve incluir "FORTIGATE" para ser considerado).

Exemplo de CSV:

```csv
Circuito,IP De Wan,EQUIPAMENTO
Host1,192.168.1.1,FORTIGATE
Host2,192.168.1.2,FORTIGATE
