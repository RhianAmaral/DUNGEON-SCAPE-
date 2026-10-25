"""Ações de combate contra inimigos."""

from .estado import Estado
from .modelos import Inimigo


def lutar(estado: Estado, inimigo: Inimigo) -> None:
    """Ponto reservado para implementar o combate."""
    print(
        f"Combate ainda não implementado. "
        f"Inimigo: {inimigo.vida} de vida."
    )


def fugir(estado: Estado, inimigo: Inimigo) -> None:
    """Ponto reservado para implementar a fuga do inimigo."""
    print("A fuga ainda não foi implementada.")


def usar_item(estado: Estado, inimigo: Inimigo) -> None:
    """Ponto reservado para implementar o uso de itens em combate."""
    if estado.inventario:
        print("O uso de itens ainda não foi implementado.")
    else:
        print("Você não tem itens no inventário.")
