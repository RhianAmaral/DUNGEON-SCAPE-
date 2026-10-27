
"""Gerenciamento do inventário do jogador."""

# Importa a função responsável por ler e validar as opções do jogador.
from .entrada import ler_opcao

# Importa a classe que armazena o estado atual do jogo.
from .estado import Estado

# Importa a classe que representa os itens do jogo.
from .modelos import Item


def pegar_item(estado: Estado, item: Item) -> None:
    """Adiciona o item encontrado ao inventário."""

    # Adiciona o item à lista de itens do inventário.
    estado.inventario.append(item)

    # Informa ao jogador que o item foi coletado.
    print(f"Item do tipo '{item.tipo}' adicionado ao inventário.")


def descartar_item(estado):
    """Permite descartar um item do inventário."""

    # Percorre os itens e exibe seus números e atributos.
    for numero, item in enumerate(estado.inventario, start=1):
        print(f"[{numero}] Tipo:", item.tipo)
        print(f"    Ataque:", item.atk)
        print(f"    Defesa:", item.dfs)
        print("-" * 30 + "\n")

    # Solicita o número do item que o jogador deseja descartar.
    opcao = ler_opcao(
        "Qual item deseja descartar? ",1,len(estado.inventario) )

    # Remove o item escolhido da lista do inventário.
    item = estado.inventario.pop(opcao - 1)

    # Informa ao jogador qual item foi descartado.
    print(f"Você descartou: {item.tipo}")


def ver_inventario(estado: Estado) -> None:
    """Exibe o inventário e suas opções."""

    # Exibe o título do inventário.
    print("\n" + "=" * 30)
    print("     INVENTÁRIO")
    print("=" * 30)

    # Verifica se o inventário está vazio.
    if not estado.inventario:
        print("Seu inventário está vazio!")
        return

    # Percorre os itens e exibe seus números e atributos.
    for numero, item in enumerate(estado.inventario, start=1):
        print(f"[{numero}] Tipo:", item.tipo)
        print(f"    Ataque:", item.atk)
        print(f"    Defesa:", item.dfs)
        print("-" * 30 + "\n")

    # Exibe as opções disponíveis no inventário.
    print("\n1 - Descartar item")
    print("2 - Voltar")

    # Solicita ao jogador uma opção entre 1 e 2.
    opcao = ler_opcao("Escolha uma opção: ", 1, 2)

    # Executa a ação correspondente à opção escolhida.
    if opcao == 1:
        descartar_item(estado)
    elif opcao == 2:
        return
