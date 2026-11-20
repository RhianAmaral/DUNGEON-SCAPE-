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

    def atacar_inimigo(self, inimigo: Inimigo) -> None:
        # O dano é o ataque do jogador menos a defesa do inimigo.
        # Sempre causa pelo menos 1 de dano, para a luta sempre terminar.

        dano = max(1, self.ataque - inimigo.defesa)
        inimigo.vida = int(inimigo.vida - dano)

@dataclass
class Item:
    """Representa um item que pode ser encontrado."""
    tipo: str
    atk: float
    dfs: float
    cura: float
    interacoes: tuple[str, ...] = ("pegar", "descartar")
