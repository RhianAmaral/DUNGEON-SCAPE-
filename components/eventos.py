"""Eventos aleatórios da masmorra (inimigos, loot e puzzles)."""

import random
from collections.abc import Callable
from typing import cast


from .combate import fugir, lutar, usar_item
from .entrada import ler_opcao
from .estado import Estado
from .inventario import pegar_item
from .modelos import Inimigo, Item, Player, Puzzle_conta, Puzzle_fato, Puzzle_labirinto


def spawnar_inimigo(dificuldade: int) -> Inimigo:
    """Cria um inimigo de acordo com a dificuldade atual."""
    vida = 10 + dificuldade
    ataque = dificuldade * 0.6
    defesa = 2 + dificuldade

    print("Um inimigo apareceu!")
    return Inimigo(vida=vida, ataque=ataque, defesa=defesa)


def gerar_loot(dificuldade: int) -> Item:
    """Gera uma arma, uma armadura ou um item de cura."""
    tipo = random.choice(("armadura", "arma", "cura"))

    ataque = 0
    defesa = 0
    cura = 0

    if tipo == "armadura":
        defesa = 3 + dificuldade
    elif tipo == "arma":
        ataque = (3 + dificuldade) * 1.5
    elif tipo == "cura":
        cura = 50

    print("Você encontrou um item!")
    return Item(tipo=tipo, atk=ataque, dfs=defesa, cura=cura)


def gerar_puzzle(dificuldade: int):
    """Ponto reservado para implementar os puzzles."""

    puzzle = random.choice((Puzzle_conta, Puzzle_fato, Puzzle_labirinto))

    if isinstance(puzzle, Puzzle_labirinto):
        lista_de_mapas = ["mapa1.txt", "mapa2.txt", "mapa3.txt"]

        mapa_selecionado = random.choice(lista_de_mapas)

        CHAR_LOOT = "L"
        CHAR_ARMADILHA = "A"
        CHAR_SPAWN_JOGADOR = "X"

        with open(mapa_selecionado, "r", encoding="utf-8") as arquivo:
            for (
                index_linha,
                linha,
            ) in enumerate(arquivo):
                linha_do_mapa = []

                for index_coluna, char in enumerate(linha.rstrip("\r\n")):
                    if char == CHAR_LOOT:
                        puzzle.coordenada_loot_x = index_linha
                        puzzle.coordenada_loot_y = index_coluna

                    elif char == CHAR_ARMADILHA:
                        puzzle.coordenadas_de_armadilhas.append(
                            (index_linha, index_coluna)
                        )

                    elif char == CHAR_SPAWN_JOGADOR:
                        puzzle.coordenada_spawn_x = index_linha
                        puzzle.coordenada_loot_y = index_coluna

                    linha_do_mapa.append(char)

                puzzle.mapa.append(linha_do_mapa)
        return puzzle
    elif isinstance(puzzle, Puzzle_conta):
        puzzle.primeiro_num = random.randint(1, 100)
        puzzle.segundo_num = random.randint(1, 100)

        LISTA_DE_OPERADORES = ["+", "-", "/", "*"]

        operador_selecionado = random.choice(LISTA_DE_OPERADORES)

        puzzle.operador = operador_selecionado

        match operador_selecionado:
            case "+":
                puzzle.solucao = puzzle.primeiro_num + puzzle.segundo_num
            case "-":
                puzzle.solucao = puzzle.primeiro_num - puzzle.segundo_num
            case "*":
                puzzle.solucao = puzzle.primeiro_num * puzzle.segundo_num
            case "/":
                puzzle.solucao = puzzle.primeiro_num / puzzle.segundo_num

        puzzle.str_pergunta = f"Quanto e {puzzle.primeiro_num} {operador_selecionado} {puzzle.segundo_num}"
        return puzzle
    elif isinstance(puzzle, Puzzle_fato):
        PERGUNTAS_E_RESPOSTAS: list[tuple[str, str]] = [
            (
                "Arranjando a primeira letra de cada um dos nomes dos criadores da masmorra, em ordem alfabetica, como ficaria?",
                "glrr",
            ),
            ("Qual o nome do Papagaio da profecia?", "junio"),
        ]

        puzzle.perguntas_e_respostas = random.choice(PERGUNTAS_E_RESPOSTAS)
        return puzzle


def _perguntar_interacao(interacoes: tuple[str, ...]) -> int:
    """Mostra as interações disponíveis e devolve a escolha do jogador."""
    print("\nO que deseja fazer?")
    for indice, opcao in enumerate(interacoes, start=1):
        print(f"{indice} - {opcao}")

    return ler_opcao("Escolha uma opção: ", 1, len(interacoes))


def chamar_evento(estado: Estado, jogador: Player) -> bool:
    """Escolhe e executa um evento aleatório da masmorra.

    Retorna False se o jogador morreu (a partida acaba) e True caso contrário.
    """
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
            return lutar(estado, resultado, jogador)
        elif escolha == 2:
            fugir(estado, resultado)
        else:
            usar_item(estado, resultado, jogador)
    elif isinstance(resultado, Puzzle_labirinto):
        while True:
            escolha = _perguntar_interacao(resultado.interacoes)

            if escolha == 1:
                jogador.andar_cima(resultado)
                jogador.andar_cima(resultado)

            elif escolha == 2:
                jogador.andar_baixo(resultado)
                jogador.andar_baixo(resultado)
            elif escolha == 3:
                jogador.andar_direita(resultado)
                jogador.andar_direita(resultado)
            elif escolha == 4:
                jogador.andar_esquerda(resultado)
                jogador.andar_esquerda(resultado)

            for armadilha_x, armadilha_y in resultado.coordenadas_de_armadilhas:
                if (
                    jogador.pos_puzzle_mapa_x == armadilha_x
                    and jogador.pos_puzzle_mapa_y == armadilha_y
                ):
                    return False
            if (
                jogador.pos_puzzle_mapa_x == resultado.coordenada_loot_x
                and jogador.pos_puzzle_mapa_y == resultado.coordenada_loot_y
            ):
                return True

    elif isinstance(resultado, Puzzle_conta):
        print("b")
    elif isinstance(resultado, Puzzle_fato):
        print("a")

    return True
