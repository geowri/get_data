import os
import requests
from zipfile import ZipFile

# URLs dos arquivos .zip e seus respectivos nomes de diretório
files = {
    # Amazônia Legal
    "https://terrabrasilis.dpi.inpe.br/download/dataset/legal-amz-aux/vector/states_legal_amazon.zip": "a_legal_amazon_states",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/legal-amz-aux/vector/brazilian_legal_amazon.zip": "a_legal_amazon",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/legal-amz-aux/vector/municipalities_legal_amazon.zip": "a_legal_amazon_municipalities",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/legal-amz-aux/vector/conservation_units_legal_amazon.zip": "a_legal_amazon_ucs",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/legal-amz-aux/vector/indigenous_area_legal_amazon.zip": "a_legal_amazon_ti",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/legal-amz-prodes/vector/hydrography.zip": "a_legal_amazon_hydrography",
    # Bioma Amazônia
    "https://terrabrasilis.dpi.inpe.br/download/dataset/amz-aux/vector/states_amazon_biome.zip": "a_amazon_states",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/amz-aux/vector/amazon_biome_border.zip": "a_amazon",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/amz-aux/vector/municipalities_amazon_biome.zip": "a_amazon_municipalities",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/amz-aux/vector/conservation_units_amazon_biome.zip": "a_amazon_ucs",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/amz-aux/vector/indigenous_area_amazon_biome.zip": "a_amazon_ti",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/amz-prodes/vector/hydrography_biome.zip": "a_amazon_hydrography",
    #Bioma Caatinga
    "https://terrabrasilis.dpi.inpe.br/download/dataset/caatinga-aux/vector/states_caatinga_biome.zip": "a_caatinga_states",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/caatinga-aux/vector/biome_border.zip": "a_caatinga",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/caatinga-aux/vector/municipalities_caatinga_biome.zip": "a_caatinga_municipalities",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/caatinga-aux/vector/conservation_units_caatinga_biome.zip": "a_caatinga_ucs",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/caatinga-aux/vector/indigenous_area_caatinga_biome.zip": "a_caatinga_ti",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/caatinga-prodes/vector/hydrography.zip": "a_caatinga_hydrography",
    #Bioma Cerrado
    "https://terrabrasilis.dpi.inpe.br/download/dataset/cerrado-aux/vector/states_cerrado_biome.zip": "a_cerrado_states",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/cerrado-aux/vector/biome_border.zip": "a_cerrado",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/cerrado-aux/vector/municipalities_cerrado_biome.zip": "a_cerrado_municipalities",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/cerrado-aux/vector/conservation_units_cerrado_biome.zip": "a_cerrado_ucs",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/cerrado-aux/vector/indigenous_area_cerrado_biome.zip": "a_cerrado_ti",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/cerrado-prodes/vector/hydrography.zip": "a_cerrado_hydrography",
    #Bioma Mata Atlântica
    "https://terrabrasilis.dpi.inpe.br/download/dataset/mata-atlantica-aux/vector/states_mata_atlantica_biome.zip": "a_mata_atlantica_states",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/mata-atlantica-aux/vector/biome_border.zip": "a_mata_atlantica",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/mata-atlantica-aux/vector/municipalities_mata_atlantica_biome.zip": "a_mata_atlantica_municipalities",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/mata-atlantica-aux/vector/conservation_units_mata_atlantica_biome.zip": "a_mata_atlantica_ucs",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/mata-atlantica-aux/vector/indigenous_area_mata_atlantica_biome.zip": "a_mata_atlantica_ti",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/mata-atlantica-prodes/vector/hydrography.zip": "a_mata_atlantica_hydrography",
    #Bioma Pampa
    "https://terrabrasilis.dpi.inpe.br/download/dataset/pampa-aux/vector/states_pampa_biome.zip": "a_pampa_states",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/pampa-aux/vector/biome_border.zip": "a_pampa",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/pampa-aux/vector/municipalities_pampa_biome.zip": "a_pampa_municipalities",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/pampa-aux/vector/conservation_units_pampa_biome.zip": "a_pampa_ucs",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/pampa-aux/vector/indigenous_area_pampa_biome.zip": "a_pampa_ti",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/pampa-prodes/vector/hydrography.zip": "a_pampa_hydrography",
    #Bioma Pnatanal
    "https://terrabrasilis.dpi.inpe.br/download/dataset/pantanal-aux/vector/states_pantanal_biome.zip": "a_pantanal_states",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/pantanal-aux/vector/biome_border.zip": "a_pantanal",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/pantanal-aux/vector/municipalities_pantanal_biome.zip": "a_pantanal_municipalities",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/pantanal-aux/vector/conservation_units_pantanal_biome.zip": "a_pantanal_ucs",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/pantanal-aux/vector/indigenous_area_pantanal_biome.zip": "a_pantanal_ti",
    "https://terrabrasilis.dpi.inpe.br/download/dataset/pantanal-prodes/vector/hydrography.zip": "a_pantanal_hydrography",
}

# Diretório onde os arquivos serão baixados e extraídos
download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)

# Função para verificar se uma URL existe
def check_url_exists(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Erro ao verificar {url}: {e}")
        return False

# Função para baixar e extrair arquivos .zip
def download_and_extract_zip(url, extract_to):
    # Nome do arquivo zip baseado na URL
    zip_path = os.path.join(download_dir, url.split("/")[-1])

    # Baixa o arquivo .zip
    print(f"Baixando {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Verifica se o download foi bem-sucedido
    with open(zip_path, "wb") as zip_file:
        for chunk in response.iter_content(chunk_size=8192):
            zip_file.write(chunk)
    print(f"{zip_path} baixado com sucesso.")

    # Cria o diretório para extrair o conteúdo
    extract_path = os.path.join(download_dir, extract_to)
    os.makedirs(extract_path, exist_ok=True)

    # Extrai o conteúdo do .zip para o diretório especificado
    print(f"Extraindo {zip_path} para {extract_path}...")
    with ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)
    print(f"Extração completa: {extract_path}")

    # Renomeia os arquivos dentro do diretório extraído
    for filename in os.listdir(extract_path):
        file_path = os.path.join(extract_path, filename)
        if os.path.isfile(file_path):
            # Obtém a extensão do arquivo
            extension = os.path.splitext(filename)[1]
            # Define o novo nome do arquivo com o nome da pasta
            new_name = os.path.join(extract_path, f"{extract_to}{extension}")
            os.rename(file_path, new_name)
            print(f"Arquivo renomeado para: {new_name}")

    # Remove o arquivo .zip após a extração (opcional)
    os.remove(zip_path)
    print(f"{zip_path} removido.\n")

# Verifica as URLs e separa as válidas das inválidas
valid_files = {}
invalid_urls = []

for url, name in files.items():
    if check_url_exists(url):
        valid_files[url] = name
    else:
        invalid_urls.append(url)

# Exibe as URLs inválidas
if invalid_urls:
    print("\nAs seguintes URLs não estão funcionando e precisam ser verificadas manualmente:")
    for url in invalid_urls:
        print(f"- {url}")

# Pergunta ao usuário se deseja continuar com o download das URLs válidas
if valid_files:
    print("\nAs seguintes URLs estão acessíveis e prontas para download:")
    for url in valid_files:
        print(f"- {url}")

    proceed = input("\nDeseja prosseguir com o download dos arquivos acessíveis? (s/n): ").strip().lower()
    if proceed == 's':
        # Baixa e extrai cada arquivo existente
        for url, folder_name in valid_files.items():
            download_and_extract_zip(url, folder_name)
    else:
        print("Download cancelado pelo usuário.")
else:
    print("Nenhuma URL válida encontrada para download.")

