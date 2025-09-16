### CRAB ISOs Downloader 🦀
O CRAB ISOs Downloader é um software de desktop simples e intuitivo, desenvolvido em Python, que permite aos usuários baixar facilmente imagens ISO de sistemas operacionais. A aplicação utiliza uma interface gráfica (GUI) para simplificar o processo, permitindo que você selecione a ISO desejada e o diretório de destino com apenas alguns cliques.

### Pré-requisitos
Para executar este software, você precisa ter o `Python` instalado em seu sistema. Além disso, as seguintes bibliotecas Python são necessárias e podem ser instaladas via pip:
```bash
    pip install requests tqdm
```

Nota: A biblioteca `isos_lib` é um módulo customizado que você precisa criar, contendo a lista de ISOs disponíveis para download. O código de exemplo para essa biblioteca deve ser um dicionário semelhante a:

```bash
    # isos_lib.py
isos_disponiveis = {
    'Linux Mint': {
        'nome_exibicao': 'Linux Mint 21.2',
        'url': 'http://mirrors.evowise.com/linuxmint/images/linuxmint-21.2-cinnamon-64bit.iso',
        'nome_arquivo': 'linuxmint-21.2-cinnamon-64bit.iso'
    },
    'Ubuntu': {
        'nome_exibicao': 'Ubuntu 22.04.4 LTS',
        'url': 'https://releases.ubuntu.com/jammy/ubuntu-22.04.4-desktop-amd64.iso',
        'nome_arquivo': 'ubuntu-22.04.4-desktop-amd64.iso'
    },
}
```

### Como Usar
Clone o Repositório: Obtenha o código-fonte do projeto.

Instale as Dependências: Execute o comando de pip install acima.

Execute o Programa: Abra o terminal na pasta do projeto e execute o script principal.

```bash
    python main.py
```

Selecione a ISO: No menu suspenso, escolha a imagem ISO que deseja baixar.

Escolha a Pasta de Destino: Clique no botão "Choose Destination Folder" e selecione onde deseja salvar o arquivo.

Inicie o Download: Clique em "Start Download" para começar a transferência. A barra de progresso irá mostrar o andamento.

<p align="center">
<img src="src\img\img1.png" alt="img1"/>
<img src="src\img\img2.png" alt="img2"/>
<img src="src\img\img3.png" alt="img3"/>
</p>

