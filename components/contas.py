"""Cadastro, login e logout de jogadores."""

from time import sleep

from .estado import Estado
from .menus import mostrar_titulo_cadastro, mostrar_titulo_login


def criar_conta(estado: Estado, usuario: str, senha: str) -> bool:
    """Cria uma conta nova. Retorna False se o usuário já existir."""
    if usuario in estado.contas:
        return False

    estado.contas[usuario] = senha
    return True


def autenticar(estado: Estado, usuario: str, senha: str) -> bool:
    """Confere usuário e senha e atualiza o estado de login."""
    if usuario in estado.contas and estado.contas[usuario] == senha:
        estado.logado = True
        estado.usuario = usuario
        return True

    estado.logado = False
    estado.usuario = ""
    return False


def cadastro(estado: Estado) -> None:
    """Cadastra uma nova conta para o jogador."""
    mostrar_titulo_cadastro()

    usuario = input("Crie seu nome de usuário: ")

    if usuario in estado.contas:
        print("Esse usuário já existe!")
        return

    senha = input("Crie sua senha: ")

    criar_conta(estado, usuario, senha)

    print("Cadastro realizado com sucesso!")
    sleep(1)


def login(estado: Estado) -> None:
    """Realiza o login na conta do jogador."""
    mostrar_titulo_login()

    usuario = input("Digite seu nome de usuário: ")
    senha = input("Digite sua senha: ")

    if autenticar(estado, usuario, senha):
        print(f"\nBem-vindo ao Dungeon Scape, {usuario}!")
    else:
        print("Usuário ou senha incorretos!")


def logout(estado: Estado) -> None:
    """Desconecta o jogador e zera a partida."""
    estado.logado = False
    estado.usuario = ""
    estado.reiniciar_partida()
