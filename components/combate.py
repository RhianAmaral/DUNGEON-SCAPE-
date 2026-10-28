"""Ações de combate contra inimigos."""

from .estado import Estado
from .modelos import Inimigo
from time import sleep
from .entrada import ler_opcao

def lutar(estado: Estado, inimigo: Inimigo, jogador: Player) -> None:
    """Ponto reservado para implementar o combate."""

    from .eventos import _perguntar_interacao
    
    while True:

        print("Voce ataca o inimgio!")
        print(f"Vida do inimigo: {inimigo.vida}")
        print(f"Sua Vida: {jogador.vida}")

        jogador.atacar_inimigo(inimigo)
       
        sleep(1)

        if inimigo.vida <= 0:

            print("Voce derrotou o inimigo")
            return

        inimigo.atacar_player(jogador)

        print("O inimigo te atacou!")
        print(f"Vida do inimigo: {inimigo.vida}")
        print(f"Sua Vida: {jogador.vida}")

        if jogador.vida < 0:

            print("===========")
            print("VOCE MORREU")
            print("===========")
            sleep(10)
            print("morte ainda nao implementada")
            return      

        escolha = _perguntar_interacao(inimigo.interacoes)

        if escolha == 1:
            continue
        elif escolha == 2:
            fugir(estado, inimigo)
        else:
            usar_item(estado, inimigo)
    


def fugir(estado: Estado, inimigo: Inimigo) -> None:
    """Ponto reservado para implementar a fuga do inimigo."""
    print("A fuga ainda não foi implementada.")


def usar_item(estado: Estado, inimigo: Inimigo) -> None:
    """Ponto reservado para implementar o uso de itens em combate."""
    if estado.inventario:
        print("O uso de itens ainda não foi implementado.")
    else:
        print("Você não tem itens no inventário.")



