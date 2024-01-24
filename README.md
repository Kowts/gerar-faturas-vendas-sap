# Gerar faturasde Vendas no SAP

## Índice

* [Descrição](#descrição)
* [Estrutura do projeto](#estrutura-do-projeto)
* [Introdução](#introdução)
  * [Pré-requisitos](#pré-requisitos)
  * [Dependências](#dependências)
  * [Instalação](#instalação)
* [Autores](#autores)
* [Documentação adicional](#documentação-adicional)
* [Links adicionais](#links-adicionais)

## Descrição

Este processo (...).

## Estrutura do projeto

```bash
├── main.py
├── helpers/
│   ├── __init__.py
│   ├── configuration.py
│   ├── exception_handler.py
│   ├── notification.py
│   ├── openflow.py
│   ├── constants.py
│   ├── sapgui.py
│   ├── outlook.py
│   └── utils.py
├── .gitignore
├── README.md
├── config.json
├── package.json
└── requirements.txt
```

## Introdução

Estas instruções irão ajudá-lo a obter uma cópia do projeto e a executá-la na sua máquina local para fins de desenvolvimento e teste, consulte as instruções sobre instalação para saber como executar o projeto. A aplicação irá executar abrindo "Sap Logon".

### Fluxograma

```mermaid

```

### Pré-requisitos

Antes de instalar este software, verifique se você tem o seguinte:

* Python 3.x
* Acesso a um servidor SMTP ou Outlook para enviar e-mails
* Configurações para conectar-se ao serviço OpenIAP (mongodb) para dados dos funcionários
* SAP Logon instalado na máquina local

### Dependências

Este projeto pode ser executado em qualquer sistema operativo e requer as seguintes bibliotecas:

* `asyncio`: para programação assíncrona
* `pywin32`: para integração com SAP Logon
* `openiap`: para integração com o serviço OpenIAP (mongodb)

### Instalação

1. **Clone o repositório**

   Primeiro, clone o repositório para sua máquina local:

   ```bash
    git clone https://github.com/DSI-OMS-RPA/mudar-password-sap.git
   ```

   Em seguida, navegue para o diretório do projeto:

   ```bash
   cd mudar-password-sap
   ```
2. **Instalar dependências**

   Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```
3. **Execute o processo**

   Finalmente, execute o processo:

   ```bash
    python main.py
   ```

## Autores

Colaboradores deste processo:

- Joselito Coutinho ([Kowts](https://github.com/Kowts))

## Documentação adicional

Este processo faz uso significativo de várias tecnologias e bibliotecas avançadas:
Estas tecnologias e bibliotecas contribuem de forma significativa para a funcionalidade e eficiência do processo, possibilitando a entrega de uma experiência de utilizador de alta qualidade.

- **Integração SAP**: O processo utiliza `pywin32`, uma biblioteca Python que fornece acesso a muitas das APIs do Windows. Esta biblioteca permite ao projeto integrar-se com o SAP Logon, possibilitando a execução de tarefas automatizadas no SAP.
- **Integração OpenFlow**: O projeto integra-se com o `OpenFlow` (mongodb), um serviço que fornece dados de colaboradores. Esta integração permite ao projeto aceder a informações dos colaboradores, como nomes, datas de aniversário e fotos, para o envio de cartões de aniversário e e-mails personalizados.
- **Integração SMTP**: O processo utiliza `smtplib`, uma biblioteca Python que fornece acesso a um servidor SMTP. Esta biblioteca permite ao projeto enviar e-mails personalizados para os colaboradores.

## Links adicionais

* Github link: https://github.com/DSI-OMS-RPA/mudar-password-sap
* Confluence link:
