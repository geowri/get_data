import os
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile

# URLs base para os arquivos dos estados e do Brasil
base_url = 'https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/UFs/'
brasil_url = 'https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/Brasil/BR/'

# Local onde todos os arquivos descompactados serão salvos
output_dir = 'dados_ibge_unificados'

# Lista das siglas dos estados (UFs) que você deseja baixar
estados = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS',
           'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC',
           'SP', 'SE', 'TO']

# Função para criar diretórios se não existirem
def criar_diretorio(pasta):
    if not os.path.exists(pasta):
        os.makedirs(pasta)

# Função para renomear arquivos e diretórios, adicionando o prefixo "a_" e convertendo para minúsculas
def renomear_com_prefixo_a(pasta):
    for root, dirs, files in os.walk(pasta):
        # Renomear os diretórios dentro de cada pasta
        for dir_name in dirs:
            new_dir_name = f"a_{dir_name.lower()}"
            os.rename(os.path.join(root, dir_name), os.path.join(root, new_dir_name))
       
        # Renomear os arquivos dentro de cada diretório
        for file_name in files:
            new_file_name = f"a_{file_name.lower()}"
            os.rename(os.path.join(root, file_name), os.path.join(root, new_file_name))

# Função para baixar e descompactar os arquivos
def download_e_extrair_zip(url, pasta_destino):
    response = requests.get(url)
    if response.status_code == 200:
        nome_arquivo = url.split('/')[-1]
        caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
       
        # Salvar o arquivo ZIP baixado
        with open(caminho_arquivo, 'wb') as file:
            file.write(response.content)
        print(f"Arquivo {nome_arquivo} baixado com sucesso.")

        # Criar um nome de pasta com base no nome do arquivo ZIP (removendo a extensão .zip e colocando tudo em letras minúsculas)
        nome_pasta = f"a_{nome_arquivo.replace('.zip', '').lower()}"
        pasta_zip = os.path.join(pasta_destino, nome_pasta)
        criar_diretorio(pasta_zip)

        # Descompactar o arquivo ZIP para a pasta correspondente
        with ZipFile(caminho_arquivo, 'r') as zip_ref:
            zip_ref.extractall(pasta_zip)
        print(f"Arquivo {nome_arquivo} descompactado em {pasta_zip}.")

        # Renomear todos os arquivos e diretórios dentro da pasta descompactada com o prefixo "a_" e letras minúsculas
        renomear_com_prefixo_a(pasta_zip)

        # Após descompactar e renomear, remover o arquivo ZIP para economizar espaço
        os.remove(caminho_arquivo)
        print(f"Arquivo {nome_arquivo} removido após descompactação.")
    else:
        print(f"Erro ao baixar {url}")

# Função para buscar e baixar os arquivos de cada estado
def baixar_arquivos_estado(estado):
    estado_url = f'{base_url}{estado}/'
   
    # Fazer requisição à página do estado
    response = requests.get(estado_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
       
        # Encontrar todos os links da página que apontam para arquivos
        for link in soup.find_all('a'):
            href = link.get('href')
            if href.endswith('.zip'):  # Baixar apenas arquivos .zip
                arquivo_url = estado_url + href
                download_e_extrair_zip(arquivo_url, output_dir)
    else:
        print(f"Erro ao acessar {estado_url}")

# Função para buscar e baixar os arquivos do Brasil
def baixar_arquivos_brasil():
    print(f"Baixando e organizando arquivos para o Brasil.")
    response = requests.get(brasil_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrar todos os links da página que apontam para arquivos
        for link in soup.find_all('a'):
            href = link.get('href')
            if href.endswith('.zip'):  # Baixar apenas arquivos .zip
                arquivo_url = brasil_url + href
                download_e_extrair_zip(arquivo_url, output_dir)
    else:
        print(f"Erro ao acessar {brasil_url}")

# Função principal para baixar os arquivos de todos os estados e do Brasil
def baixar_todos_estados_e_brasil():
    criar_diretorio(output_dir)  # Criar diretório raiz para os arquivos unificados se não existir
   
    # Baixar arquivos dos estados
    for estado in estados:
        print(f"Baixando e organizando arquivos para o estado: {estado}")
        baixar_arquivos_estado(estado)
   
    # Baixar arquivos do Brasil
    baixar_arquivos_brasil()

# Executar o download para todos os estados e o Brasil
baixar_todos_estados_e_brasil()
