"""Classes que representam as entidades do jogo."""

from dataclasses import dataclass


@dataclass
class Inimigo:
    """Representa um inimigo encontrado na masmorra."""
    vida: int
    ataque: float
    defesa: float = 0.0
    interacoes: tuple[str, ...] = ("lutar", "fugir", "usar item")


@dataclass
class Item:
    """Representa um item que pode ser encontrado."""
    tipo: str
    atk: float
    dfs: float
    interacoes: tuple[str, ...] = ("pegar", "descartar")
