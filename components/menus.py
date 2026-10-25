"""Funções que exibem menus e textos na tela."""

from .config import LARGURA_MENU


def _cabecalho(titulo: str) -> None:
    """Exibe um título decorado com linhas de '='."""
    print("\n" + "=" * LARGURA_MENU)
    print(titulo)
    print("=" * LARGURA_MENU)


def mostrar_menu_signin() -> None:
    """Exibe o menu para quando o jogador ainda não está logado."""
    _cabecalho("Escape da Masmorra")
    print("1 - Cadastro")
    print("2 - Login")
    print("3 - Sair")


def mostrar_menu_principal() -> None:
    """Exibe o menu principal do jogo."""
    _cabecalho("Escape da Masmorra")
    print("1 - Iniciar Jogo")
    print("2 - Logout")
    print("3 - Sair")


def mostrar_titulo_cadastro() -> None:
    """Exibe o cabeçalho da tela de cadastro."""
    _cabecalho("CADASTRO DO JOGO")


def mostrar_titulo_login() -> None:
    """Exibe o cabeçalho da tela de login."""
    _cabecalho("LOGIN")


def instrucoes() -> None:
    """Exibe as instruções básicas do jogo."""
    print(
        "\nExplore a masmorra, encontre itens e tome decisões para escapar."
    )
