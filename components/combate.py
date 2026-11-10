"""Ações de combate contra inimigos."""

from .estado import Estado
from .modelos import Inimigo, Player
from time import sleep
import random


def lutar(estado: Estado, inimigo: Inimigo, jogador: Player) -> bool:
    """Executa o combate entre o jogador e um inimigo."""

    from .eventos import _perguntar_interacao

    while True:
        print("Você ataca o inimigo!")
        print(f"Vida do inimigo: {inimigo.vida}")
        print(f"Sua vida: {jogador.vida}")

        jogador.atacar_inimigo(inimigo)

        sleep(1)

        if inimigo.vida <= 0:
            print("Você derrotou o inimigo!")
            return True

        inimigo.atacar_player(jogador)

        print("O inimigo te atacou!")
        print(f"Vida do inimigo: {inimigo.vida}")
        print(f"Sua vida: {jogador.vida}")

        if jogador.vida <= 0:
            morte()
            return False

        while True:
            escolha = _perguntar_interacao(inimigo.interacoes)

            if escolha == 1:
                break
            elif escolha == 2:
                if fugir(estado, inimigo):
                    return True
                else:
                    break
            elif escolha == 3:
                usar_item(estado, inimigo)
                break


def fugir(estado: Estado, inimigo: Inimigo) -> bool:
    """Executa a tentativa de fuga do inimigo."""

    chance_fuga = random.randint(1, 100)

    if chance_fuga <= 70:
        print("Você conseguiu fugir!")
        return True

    print("Você não conseguiu fugir!")
    return False


def usar_item(estado: Estado, inimigo: Inimigo) -> None:
            """Executa o uso de itens em combate."""
        
            jogador = estado.jogador
        
            if estado.inventario:
                for indice, item in enumerate(estado.inventario):
                    print(f"{indice + 1} - {item.tipo}")
        
                opcao = ler_opcao("Qual item deseja usar? ", 1, len(estado.inventario))
        
                indice = opcao - 1
                item = estado.inventario[indice]
        
                if item.cura > 0:
                    if jogador.vida < jogador.vida_maxima:
                        vida_anterior = jogador.vida
        
                        jogador.vida = min(jogador.vida + item.cura, jogador.vida_maxima)
                        
                        estado.inventario.pop(indice)
        
                        print(f"Você recuperou {jogador.vida - vida_anterior} pontos de vida!")
                    else:
                        print("Sua vida está cheia!")
                else:
                    print("Esse item não é uma poção de cura!")
        
            else:
                print("Você não tem itens no inventário.")
        

def morte() -> None:
    """Exibe a mensagem de morte do jogador."""

    print("====================")
    print("     GAME OVER")
    print("====================")
