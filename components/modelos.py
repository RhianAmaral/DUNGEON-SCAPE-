"""Classes que representam as entidades do jogo."""

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

    def atacar_inimigo(self, inimigo: Inimigo) -> None:

        inimigo.vida = int(inimigo.vida - self.ataque)


@dataclass
class Item:
    """Representa um item que pode ser encontrado."""
    tipo: str
    atk: float
    dfs: float
    interacoes: tuple[str, ...] = ("pegar", "descartar")
