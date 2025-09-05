import requests
import os
import isos_lib

#Esse aqui vai listar as isos
isos_disponiveis = isos_lib.isos_disponiveis
nome_exibicao = "\n".join(
        [iso["nome_exibicao"] for iso in isos_disponiveis.values()])
print(nome_exibicao)
iso_selecionada = input("Digite o nome do ISO que deseja baixar: ")
nome_exibicao = iso_selecionada
iso_selecionada = isos_disponiveis.get(nome_exibicao)

if iso_selecionada is None:
        print("Nenhum ISO selecionado ou nome digitado errado." 
              "\n" "Tente novamente.")
        
else:
        print("ISO selecionado:", iso_selecionada["nome_exibicao"])

#Esse aqui vai fazer o download da iso
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