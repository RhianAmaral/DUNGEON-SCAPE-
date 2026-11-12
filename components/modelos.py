"""Classes que representam as entidades do jogo."""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Inimigo:
    """Representa um inimigo encontrado na masmorra."""

    vida: float
    ataque: float
    defesa: float = 0.0
    interacoes: tuple[str, ...] = ("lutar", "fugir", "usar item")

    def atacar_player(self, jogador: Player) -> None:

        jogador.vida = int(jogador.vida - self.ataque)


@dataclass
class Player:
    vida: float
    ataque: float
    defesa: float
    char_mapa = "@"
    pos_puzzle_mapa_x: int
    pos_puzzle_mapa_y: int

    def atacar_inimigo(self, inimigo: Inimigo) -> None:
        # O dano é o ataque do jogador menos a defesa do inimigo.
        # Sempre causa pelo menos 1 de dano, para a luta sempre terminar.

        dano = max(1, self.ataque - inimigo.defesa)
        inimigo.vida = int(inimigo.vida - dano)

    # if next plyer pos != wall, move
    # also create a little stack to store the next tile
    # of the map that the player is about to replace when it moves
    # so then when he moves again then pop the stack and restore the
    # previous tile, then store new tile on stack, then move, and so on...
    def andar_baixo(self, mapa: Puzzle_labirinto) -> None:
        PAREDE = "#"
        CHAO = "."

        pos_atual_x = self.pos_puzzle_mapa_x
        pos_atual_y = self.pos_puzzle_mapa_y

        if (mapa.mapa[pos_atual_x + 1][pos_atual_y]) != PAREDE:
            if (
                pos_atual_x == mapa.coordenada_spawn_x
                and pos_atual_y == mapa.coordenada_spawn_y
            ):
                mapa.ultimo_char = CHAO

            # restora a celula que o joagdor sobreescreveu em seu ultimo movimento
            # e salva a nova celula que o joador ira sobrescrever para depois restaura-la
            mapa.mapa[pos_atual_x - 1][pos_atual_y] = mapa.ultimo_char
            mapa.ultimo_char = mapa.mapa[pos_atual_x + 1][pos_atual_y]

            mapa.mapa[pos_atual_x + 1][pos_atual_y] = self.char_mapa

    def andar_cima(self, mapa: Puzzle_labirinto) -> None:
        PAREDE = "#"
        CHAO = "."

        pos_atual_x = self.pos_puzzle_mapa_x
        pos_atual_y = self.pos_puzzle_mapa_y

        if (mapa.mapa[pos_atual_x - 1][pos_atual_y]) != PAREDE:
            if (
                pos_atual_x == mapa.coordenada_spawn_x
                and pos_atual_y == mapa.coordenada_spawn_y
            ):
                mapa.ultimo_char = CHAO

            # restora a celula que o joagdor sobreescreveu em seu ultimo movimento
            # e salva a nova celula que o joador ira sobrescrever para depois restaura-la
            mapa.mapa[pos_atual_x + 1][pos_atual_y] = mapa.ultimo_char
            mapa.ultimo_char = mapa.mapa[pos_atual_x - 1][pos_atual_y]

            mapa.mapa[pos_atual_x - 1][pos_atual_y] = self.char_mapa

    def andar_direita(self, mapa: Puzzle_labirinto) -> None:
        PAREDE = "#"
        CHAO = "."

        pos_atual_x = self.pos_puzzle_mapa_x
        pos_atual_y = self.pos_puzzle_mapa_y

        if (mapa.mapa[pos_atual_x][pos_atual_y + 1]) != PAREDE:
            if (
                pos_atual_x == mapa.coordenada_spawn_x
                and pos_atual_y == mapa.coordenada_spawn_y
            ):
                mapa.ultimo_char = CHAO

            # restora a celula que o joagdor sobreescreveu em seu ultimo movimento
            # e salva a nova celula que o joador ira sobrescrever para depois restaura-la
            mapa.mapa[pos_atual_x][pos_atual_y + 1] = mapa.ultimo_char
            mapa.ultimo_char = mapa.mapa[pos_atual_x][pos_atual_y - 1]

            mapa.mapa[pos_atual_x][pos_atual_y + 1] = self.char_mapa

    def andar_esquerda(self, mapa: Puzzle_labirinto) -> None:
        PAREDE = "#"
        CHAO = "."

        pos_atual_x = self.pos_puzzle_mapa_x
        pos_atual_y = self.pos_puzzle_mapa_y

        if (mapa.mapa[pos_atual_x][pos_atual_y - 1]) != PAREDE:
            if (
                pos_atual_x == mapa.coordenada_spawn_x
                and pos_atual_y == mapa.coordenada_spawn_y
            ):
                mapa.ultimo_char = CHAO

            # restora a celula que o joagdor sobreescreveu em seu ultimo movimento
            # e salva a nova celula que o joador ira sobrescrever para depois restaura-la
            mapa.mapa[pos_atual_x][pos_atual_y - 1] = mapa.ultimo_char
            mapa.ultimo_char = mapa.mapa[pos_atual_x][pos_atual_y + 1]

            mapa.mapa[pos_atual_x][pos_atual_y - 1] = self.char_mapa


@dataclass
class Item:
    """Representa um item que pode ser encontrado."""

    tipo: str
    atk: float
    dfs: float
    cura: float
    interacoes: tuple[str, ...] = ("pegar", "descartar")


@dataclass
class Puzzle_labirinto:
    mapa: list[list[str]]
    coordenada_loot_x: int
    coordenada_loot_y: int
    coordenadas_de_armadilhas: list[tuple[int, int]]
    coordenada_spawn_x: int
    coordenada_spawn_y: int
    ultimo_char: str
    interacoes: tuple[str, ...] = (
        "andar para cima",
        "andar para baixo",
        "andar para direita",
        "andar para esquerda",
    )


@dataclass
class Puzzle_conta:
    primeiro_num: int
    operador: str
    segundo_num: int
    solucao: float
    str_pergunta: str


@dataclass
class Puzzle_fato:
    perguntas_e_respostas: tuple[str, str]
