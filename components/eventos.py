"""Eventos aleatórios da masmorra (inimigos, loot e puzzles)."""

import random

from .combate import fugir, lutar, usar_item
from .entrada import ler_opcao
from .estado import Estado
from .inventario import pegar_item
from .modelos import Inimigo, Item, Player


def spawnar_inimigo(dificuldade: int) -> Inimigo:
    """Cria um inimigo de acordo com a dificuldade atual."""
    vida = 10 + dificuldade
    ataque = dificuldade * 0.6
    defesa = 2 + dificuldade

    print("Um inimigo apareceu!")
    return Inimigo(vida=vida, ataque=ataque, defesa=defesa)


def gerar_loot(dificuldade: int) -> Item:
    """Gera uma arma ou uma armadura de acordo com a dificuldade."""
    tipo = random.choice(("armadura", "arma"))

    if tipo == "armadura":
        ataque = 0
        defesa = 3 + dificuldade
    else:
        ataque = (3 + dificuldade) * 1.5
        defesa = 0

    print("Você encontrou um item!")
    return Item(tipo=tipo, atk=ataque, dfs=defesa)


def gerar_puzzle(dificuldade: int) -> None:
    """Ponto reservado para implementar os puzzles."""
    print(f"Você encontrou um puzzle (dificuldade {dificuldade}).")
    print("Puzzle ainda não implementado.")


def _perguntar_interacao(interacoes: tuple[str, ...]) -> int:
    """Mostra as interações disponíveis e devolve a escolha do jogador."""
    print("\nO que deseja fazer?")
    for indice, opcao in enumerate(interacoes, start=1):
        print(f"{indice} - {opcao}")

    return ler_opcao("Escolha uma opção: ", 1, len(interacoes))


def chamar_evento(estado: Estado, jogador: Player) -> None:
    """Escolhe e executa um evento aleatório da masmorra."""
    estado.tick += 1
    dificuldade = estado.tick // 2

    eventos = (spawnar_inimigo, gerar_loot, gerar_puzzle)
    evento = random.choice(eventos)
    resultado = evento(dificuldade)

    if isinstance(resultado, Item):
        escolha = _perguntar_interacao(resultado.interacoes)

        if escolha == 1:
            pegar_item(estado, resultado)
        else:
            print("Você descartou o item.")

    elif isinstance(resultado, Inimigo):
        escolha = _perguntar_interacao(resultado.interacoes)

        if escolha == 1:
            lutar(estado, resultado, jogador)
        elif escolha == 2:
            fugir(estado, resultado)
        else:
            usar_item(estado, resultado)
