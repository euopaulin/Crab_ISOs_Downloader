import requests
import os
from isos_lib import isos_disponiveis

#Classe criada para gerenciar os atritutos das ISOs para depois ser chamada no código
class ISODownloader:
    def __init__(self):
        self.isos = isos_disponiveis
        self.iso_selecionada = None

#Função para exibir o menu de ISOs disponíveis
    def exibir_menu(self):
        print("\nISOs disponíveis:")
        for nome_exibicao in self.isos.values():
            print(f"- {nome_exibicao['nome_exibicao']}")

    def selecionar_iso(self):
        while True:
            nome_exibicao = input("\nDigite o nome do ISO que deseja baixar: ")
            self.iso_selecionada = self.isos.get(nome_exibicao)
            if self.iso_selecionada:
                print(f"ISO selecionado: {self.iso_selecionada['nome_exibicao']}")
                return True
            else:
                print("ISO não encontrado. Por favor, tente novamente.")
                self.exibir_menu()

    def obter_caminho_destino(self):
        pasta = input("Digite o caminho da pasta de destino para salvar o ISO: ")
        pasta_destino = os.path.abspath(pasta)
        print(f'Pasta selecionada: {pasta_destino}')

        if not os.path.exists(pasta_destino):
            try:
                os.makedirs(pasta_destino)
                print(f"Pasta criada: {pasta_destino}")
            except OSError as e:
                print(f"Erro ao criar a pasta: {e}")
                return None

        caminho_arquivo = os.path.join(pasta_destino, self.iso_selecionada["nome_arquivo"])
        return caminho_arquivo

    def download_iso(self):
        if not self.iso_selecionada:
            print("Nenhum ISO selecionado para download.")
            return

        caminho_arquivo = self.obter_caminho_destino()
        if not caminho_arquivo:
            return

        print(f'Salvando em: {caminho_arquivo}')

        try:
            with requests.get(self.iso_selecionada["url"], stream=True) as resposta:
                resposta.raise_for_status()
                tamanho_total = float(resposta.headers.get('content-length', 0))
                tamanho_total_mb = tamanho_total / (1024 * 1024)
                print(f"Tamanho total do arquivo: {tamanho_total_mb:.2f} MB")

                tamanho_baixado = 0
                with open(caminho_arquivo, 'wb') as arquivo:
                    for dados in resposta.iter_content(chunk_size=8192):
                        arquivo.write(dados)
                        tamanho_baixado += len(dados)
                        porcentagem = (tamanho_baixado / tamanho_total) * 100
                        print(f"Progresso: {porcentagem:.2f}%", end="\r")

            print("\nDownload concluído com sucesso!")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao fazer o download: {e}")

def main():
    downloader = ISODownloader()
    downloader.exibir_menu()
    if downloader.selecionar_iso():
        downloader.download_iso()

if __name__ == "__main__":
    main()