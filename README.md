# Image and Mask Selection Tool

Este projeto consiste em um script que auxilia na seleção de imagens e máscaras de um determinado dataset para segmentação. Através de uma interface gráfica, o usuário pode visualizar e classificar imagens e suas respectivas máscaras, salvando-as em pastas de "bad_data" e "good_data".

## Funcionalidades

- Visualização de imagens e máscaras do dataset.
- Interface gráfica simples e intuitiva usando Tkinter.
- Botões para classificar e salvar imagens/máscaras em pastas específicas ("bad_data" e "good_data").
- Agrupamento dos botões de classificação para fácil acesso.

## Requisitos

- Python 3.8 ou superior
- Tkinter (geralmente incluído com Python)
- Biblioteca Pillow (para manipulação de imagens)

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/brunojlle/dataset-seg

2. Navegue até o diretório do projeto:

    ```bash
    cd dataset-seg

3. (Opcional) Crie um ambiente virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Linux/Mac
    venv\Scripts\activate  # Para Windows

4. Instale as dependências:

    ```bash
    pip install -r requirements.txt

## Uso

1. Execute o script principal:

    ```bash
    python main.py

2. A interface gráfica será aberta, permitindo a visualização das imagens e máscaras.

3. Utilize os botões para classificar as imagens/máscaras como "good_data" ou "bad_data".

## Estrutura do projeto

    ```bash
    dataset-seg/
    │
    ├── data/                 # Diretório contendo as imagens e máscaras do dataset
    │
    ├── good_data/            # Diretório para salvar imagens e máscaras classificadas como boas
    ├── bad_data/             # Diretório para salvar imagens e máscaras classificadas como ruins
    │
    ├── main.py               # Script principal para execução da interface gráfica
    ├── requirements.txt      # Arquivo com as dependências do projeto
    └── README.md             # Este arquivo

## Contribuição

Contribuições são bem-vindas! Se você tiver sugestões ou encontrar problemas, por favor, abra uma issue ou envie um pull request.
## Licença

Este projeto está licenciado sob a licença [MIT](https://choosealicense.com/licenses/mit/).

Sinta-se à vontade para modificar conforme necessário para atender às especificidades do seu projeto.