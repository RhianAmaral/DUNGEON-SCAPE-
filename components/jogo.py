
"""Fluxo de uma partida: exploração das salas e menu da partida."""

# Importa recursos para gerar números aleatórios e criar pausas na execução.
import random
from time import sleep

# Importa o limite de salas definido nas configurações do jogo.
from .config import LIMITE_DE_SALAS

# Importa a classe que armazena o estado atual do jogo.
from .estado import Estado

# Importa a função responsável por executar os eventos da exploração.
from .eventos import chamar_evento

# Importa a função responsável por ler e validar as opções do jogador.
from .entrada import ler_opcao

# Importa a função que exibe o inventário do jogador.
from .inventario import ver_inventario

from .modelos import Player


def escolher_porta() -> int:
    """Permite ao jogador escolher uma das três portas."""

    # Exibe as opções de caminhos disponíveis na sala.
    print("\nEscolha seu caminho:")
    print("[1] Porta à esquerda")
    print("[2] Caminho à frente")
    print("[3] Porta à direita")

    # Solicita uma opção entre 1 e 3 e retorna o valor escolhido.
    return ler_opcao("Escolha uma porta: ", 1, 3)


def explorar_sala(estado: Estado, jogador: Player) -> None:
    """Explora uma quantidade aleatória de salas."""

    # Sorteia a quantidade de salas que serão exploradas nesta rodada.
    salas_disponiveis = random.randint(1, LIMITE_DE_SALAS)

    # Percorre as salas sorteadas, começando pela primeira.
    for numero_sala in range(1, salas_disponiveis + 1):
        # Informa ao jogador qual sala está sendo explorada.
        print(f"\nSala {numero_sala}:")

        # Permite ao jogador escolher um dos caminhos disponíveis.
        escolher_porta()

        # Executa um evento relacionado à exploração da sala.
        chamar_evento(estado, jogador)

        # Exibe uma animação simples para representar a exploração.
        print("Explorando salas.", end="\r", flush=True)
        sleep(0.5)
        print("Explorando salas..", end="\r", flush=True)
        sleep(0.5)
        print("Explorando salas...", flush=True)


def iniciar_jogo(estado: Estado, jogador: Player) -> None:
    """Inicia uma partida e permite explorar ou voltar ao menu."""

    # Impede que a partida comece se o jogador não estiver conectado.
    if not estado.logado:
        print("Realize o login para iniciar o jogo.")
        return

    # Reinicia o progresso e os atributos da partida.
    estado.reiniciar_partida()

    # Apresenta a situação inicial da história.
    print("Você acordou em uma masmorra.")
    print("Encontre uma maneira de escapar.")

    # Mantém o menu da partida ativo até o jogador escolher voltar.
    while True:
        print("\n1 - Explorar a masmorra")
        print("2 - Mostrar inventário")
        print("3 - Voltar ao menu inicial")

        # Solicita uma opção válida entre 1 e 3.
        opcao = ler_opcao("Escolha uma opção: ", 1, 3)

        # Executa a ação correspondente à opção escolhida.
        if opcao == 1:
            explorar_sala(estado, jogador)
        elif opcao == 2:
            ver_inventario(estado)
        elif opcao == 3:
            # Exibe uma animação antes de retornar ao menu inicial.
            print("Voltando para o menu inicial", end="\r", flush=True)
            sleep(0.5)
            print("Voltando para o menu inicial..", end="\r", flush=True)
            sleep(0.5)
            print("Voltando para o menu inicial...", flush=True)
            sleep(0.5)
            return
