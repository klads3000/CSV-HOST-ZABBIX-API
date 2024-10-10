import requests
import json
import csv

# Configurações da API do Zabbix
url = 'https://ENDEREÇODOZABBIX/zabbix/api_jsonrpc.php' # Endereço do zabbix
headers = {'Content-Type': 'application/json-rpc'}

# Credenciais de autenticação
username = 'USUARIO'
password = 'SENHA'


# Função para fazer uma chamada à API do Zabbix
def call_zabbix_api(method, params, auth=None):
    payload = {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': 1,
    }
    if auth:
        payload['auth'] = auth

    response = requests.post(url, headers=headers, verify=False, data=json.dumps(payload))
    return response.json()


# Função para autenticar no Zabbix e obter o token de autenticação
def zabbix_login(username, password):
    params = {
        'user': username,
        'password': password,
    }
    response = call_zabbix_api('user.login', params)
    return response['result']


# Função para ler dados do CSV e criar hosts SNMPv2
def create_hosts_from_csv(csv_file, template_id, group_id, auth_token):
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'FORTIGATE' in row['EQUIPAMENTO']:
                hostname = row['Circuito']
                ip_address = row['IP De Wan']
                snmp_community = 'public'  # Sua community SNMP
                params = {
                    'host': hostname,
                    'interfaces': [
                        {
                            'type': 2,  # Tipo 2 para SNMP
                            'main': 1,
                            'useip': 1,
                            'ip': ip_address,
                            'dns': '',
                            'port': '161',
                            "details": {
                                "version": 2,
                                "bulk": 0,
                                "community": snmp_community,
                                "securityname": "",
                                "contextname": "",
                                "securitylevel": 1
                            }
                        }
                    ],
                    'groups': [{'groupid': group_id}],
                    'templates': [{'templateid': template_id}],
                    'inventory_mode': 0,
                    #'proxy_hostid': '13297' CASO SEJA NECESSARIO ZABBIX_PROXY(A informação do ID está na URL do zabbix-proxy no zabbix)
                }
                response = call_zabbix_api('host.create', params, auth_token)
                print(f"Host '{hostname}' criado com sucesso:")
                print(json.dumps(response, indent=4))


# Autenticar no Zabbix
auth_token = zabbix_login(username, password)

if auth_token:
    try:
        # Exemplo: ID do template e grupo
        template_id = 'xxx'  # ID do template SNMP Genérico
        group_id = 'xxx'  # ID do grupo ao qual o host pertencerá

        # Caminho para o arquivo CSV
        csv_file = 'ARQUIVOCOMHOSTS.csv'

        # Criar hosts do CSV
        create_hosts_from_csv(csv_file, template_id, group_id, auth_token)

    finally:
        # Encerrar a sessão de autenticação
        logout_params = []
        logout_response = call_zabbix_api('user.logout', logout_params, auth_token)
        print("Sessão de autenticação encerrada.")
else:
    print("Falha ao autenticar no Zabbix.")
