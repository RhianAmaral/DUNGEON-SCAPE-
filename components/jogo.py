"""Fluxo de uma partida: exploração das salas e menu da partida."""

import random
from time import sleep

from .config import LIMITE_DE_SALAS
from .estado import Estado
from .eventos import chamar_evento


def explorar_sala(estado: Estado) -> None:
    """Explora uma quantidade aleatória de salas."""
    salas_disponiveis = random.randint(1, LIMITE_DE_SALAS)

    for numero_sala in range(1, salas_disponiveis + 1):
        print(f"\nSala {numero_sala}:")
        chamar_evento(estado)

        # Animação simples de exploração.
        print("Explorando salas.", end="\r", flush=True)
        sleep(0.5)
        print("Explorando salas..", end="\r", flush=True)
        sleep(0.5)
        print("Explorando salas...", flush=True)


def iniciar_jogo(estado: Estado) -> None:
    """Inicia uma partida e permite explorar ou voltar ao menu."""
    # Impede que a partida comece sem login.
    if not estado.logado:
        print("Realize o login para iniciar o jogo.")
        return

    estado.reiniciar_partida()

    print("Você acordou em uma masmorra.")
    print("Encontre uma maneira de escapar.")

    while True:
        print("\n1 - Explorar a masmorra")
        print("2 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            explorar_sala(estado)
        elif opcao == "2":
            print("Voltando para o menu...")
            return
        else:
            print("Opção inválida! Tente novamente.")
