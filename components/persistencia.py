"""Salvar e carregar o progresso do jogo em arquivo."""

import json

from .config import ARQUIVO_SAVE
from .estado import Estado
from .modelos import Item


def salvar_jogo(estado: Estado) -> None:
    """Salva o tick atual, o inventário e as contas no arquivo de save."""
    # Item é uma classe, então precisa virar dicionário para ir pro JSON.
    inventario = [
        {"tipo": item.tipo, "atk": item.atk, "dfs": item.dfs}
        for item in estado.inventario
    ]
    dados = [estado.tick, inventario, estado.contas]

    with open(ARQUIVO_SAVE, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo)


def carregar_jogo() -> Estado | None:
    """Carrega o jogo salvo. Retorna None se não houver save válido."""
    try:
        with open(ARQUIVO_SAVE, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        # Se o arquivo não tem todos os dados esperados, retorna None.
        if not isinstance(dados, list) or len(dados) != 3:
            return None

        tick, inventario, contas = dados
        itens = [Item(**item) for item in inventario]
        return Estado(contas=contas, tick=tick, inventario=itens)

    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        # Sem save, JSON inválido ou itens com formato inesperado.
        return None
