import requests
import os

isos_disponiveis = {
    "ubuntu Desktop": {
        "nome_exibicao": "Ubuntu Desktop 24.04 LTS",
        "url":
        "https://ubuntu.com/download/desktop/thank-you?version=24.04.3&architecture=amd64&lts=true",
        "nome_arquivo": "ubuntu-24.04-desktop-amd64.iso"
    },
    "Windows 11": {
        "nome_exibicao": "Windows 11",
        "url": "https://www.microsoft.com/pt-br/software-download/windows11",
        "nome_arquivo": "windows11.iso"
    },
}

nome_exibicao = "\n".join(
    [iso["nome_exibicao"] for iso in isos_disponiveis.values()])
print(nome_exibicao)
iso_selecionada = input("Digite o nome do ISO que deseja baixar: ")
nome_exibicao = iso_selecionada
iso_selecionada = isos_disponiveis.get(nome_exibicao)

if iso_selecionada is None:
    print("Nenhum ISO selecionado.")
else:
    print("ISO selecionado:", iso_selecionada["nome_exibicao"])


def download_iso():
    try:
        resposta = requests.get(iso_selecionada["url"], stream=True)
        resposta.raise_for_status()
    except requests.exceptions.RequestException as erro:
        print("Erro ao fazer o download:", erro)

    if resposta.status_code == 200:
        print("Requisição bem-sucedida!")
    else:
        print("Erro na requisição:", resposta.status_code)
        # Verifica se houve algum erro na requisição

    #segunda parte

    tamanho_total = float(resposta.headers.get('content-length', 0))
    tamanho_total_mb = tamanho_total / (1024 * 1024)
    print(f"Tamanho total do arquivo: {tamanho_total_mb:.2f} MB")

    pasta = input("Digite o caminho da pasta de destino para salvar o ISO: ")
    pasta_destino = pasta
    print(f'Pasta selecionada: {pasta_destino}')
    caminho_arquivo = os.path.join(pasta_destino,
                                   iso_selecionada["nome_arquivo"])
    print(f'Salvando em: {caminho_arquivo}')

    try:
        resposta = requests.get(iso_selecionada["url"], stream=True)
        resposta.raise_for_status()
        with open(caminho_arquivo, 'wb') as arquivo:
            for dados in resposta.iter_content(chunk_size=8192):
                arquivo.write(dados)

        print(f"Download concluído: {caminho_arquivo}")
    except requests.exceptions.RequestException as erro2:
        print("Erro ao fazer o download:", erro2)
        return


download_iso()
