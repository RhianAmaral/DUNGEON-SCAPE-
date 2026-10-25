"""Gerenciamento do inventário do jogador."""

from .estado import Estado
from .modelos import Item


def pegar_item(estado: Estado, item: Item) -> None:
    """Adiciona o item encontrado ao inventário."""
    estado.inventario.append(item)
    print(f"Item do tipo '{item.tipo}' adicionado ao inventário.")
