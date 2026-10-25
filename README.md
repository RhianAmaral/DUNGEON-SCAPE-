# ESCAPE DA MASMORRA

**Integrantes**

* Mathues Lima Barbosa
* Gustavo Chagas Neri
* Rhian Amaral Dionisio da Silva
* Romulo Batista Costa santos
* Richarlyson Vilar Dos Santos



> Uma aventura desenvolvida em Python na qual cada decisão pode ser a diferença entre escapar e permanecer preso na masmorra.

##  Sobre o projeto

**Escape da Masmorra** é um jogo de aventura desenvolvido em Python, com foco na exploração, na tomada de decisões e na superação de desafios.

O projeto tem como objetivo aplicar conceitos de lógica de programação na construção de uma experiência interativa, evoluindo gradualmente em funcionalidades e organização do código.

## Funcionalidades

* Menu inicial interativo
* Sistema de exploração de salas
* Escolhas com consequências
* Sistema de inventário
* Itens e chaves
* Sistema de combate
* Condições de vitória e derrota

*As funcionalidades serão marcadas conforme forem implementadas e testadas.*

## Tecnologias utilizadas

- **Python** — linguagem de programação.
- **Git** — controle de versão.
- **GitHub** — hospedagem do código-fonte.

## Como executar

### Pré-requisitos

- Python 3 instalado.
- Git instalado, caso queira clonar o repositório.

### Instalação

1. Clone o repositório:

   ```bash
    git clone https://github.com/RhianAmaral/DUNGEON-SCAPE-.git
   ```

2. Entre na pasta do projeto:

   ```bash
   cd DUNGEON-SCAPE-
   ```

3. Execute o jogo:

   ```bash
   python main.py
   ```

> Dependendo da sua instalação, pode ser necessário utilizar `python3 main.py` ou `py main.py`.


## Estrutura do projeto

```text
DUNGEON-SCAPE-/
├── main.py                 # Ponto de entrada: menus de login e menu principal
└── components/
    ├── config.py           # Constantes (arquivo de save, limite de salas...)
    ├── modelos.py          # Classes Inimigo e Item
    ├── estado.py           # Classe Estado (contas, logado, tick, inventário)
    ├── entrada.py          # Leitura e validação do que o jogador digita
    ├── menus.py            # Textos e menus exibidos na tela
    ├── contas.py           # Cadastro, login e logout
    ├── persistencia.py     # Salvar e carregar o jogo (JSON)
    ├── inventario.py       # Regras do inventário
    ├── combate.py          # Lutar, fugir e usar item
    ├── eventos.py          # Inimigos, loot, puzzles e evento aleatório
    └── jogo.py             # Exploração de salas e fluxo da partida
```

A estrutura será atualizada conforme novos módulos e funcionalidades forem adicionados.

## Conceitos aplicados

Durante o desenvolvimento, serão explorados conceitos como:

* Variáveis e tipos de dados.
* Estruturas condicionais.
* Estruturas de repetição.
* Listas e manipulação de dados.
* Funções e modularização.
* Tratamento de entradas e erros.
* Classes e POO.
* Json, leitura e escrita de arquivos.


---

Projeto desenvolvido com o objetivo de praticar Python, lógica de programação e desenvolvimento de software.

