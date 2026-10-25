"""Cadastro, login e logout de jogadores."""

from time import sleep

from .estado import Estado
from .menus import mostrar_titulo_cadastro, mostrar_titulo_login


def cadastro(estado: Estado) -> None:
    """Cadastra uma nova conta para o jogador."""
    mostrar_titulo_cadastro()

    usuario = input("Crie seu nome de usuário: ")

    if usuario in estado.contas:
        print("Esse usuário já existe!")
        return

    senha = input("Crie sua senha: ")

    estado.contas[usuario] = senha

    print("Cadastro realizado com sucesso!")
    sleep(1)


def login(estado: Estado) -> None:
    """Realiza o login na conta do jogador."""
    mostrar_titulo_login()

    usuario = input("Digite seu nome de usuário: ")
    senha = input("Digite sua senha: ")

    if usuario in estado.contas and estado.contas[usuario] == senha:
        print(f"\nBem-vindo ao Dungeon Scape, {usuario}!")
        estado.logado = True
    else:
        print("Usuário ou senha incorretos!")
        estado.logado = False


def logout(estado: Estado) -> None:
    """Desconecta o jogador e zera a partida."""
    estado.logado = False
    estado.reiniciar_partida()
