"""Ponto de entrada do jogo Escape da Masmorra."""

from components.contas import cadastro, login, logout
from components.estado import Estado
from components.jogo import iniciar_jogo
from components.menus import mostrar_menu_principal, mostrar_menu_signin
from components.persistencia import carregar_jogo, salvar_jogo


def lidar_com_signin_login(estado: Estado) -> bool:
    """Mostra o menu de cadastro/login até o jogador entrar ou sair.

    Retorna True se o jogador logou e False se escolheu sair do jogo.
    """
    while not estado.logado:
        mostrar_menu_signin()

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Digite um número válido.")
            continue

        if opcao == 1:
            cadastro(estado)
        elif opcao == 2:
            login(estado)
        elif opcao == 3:
            print("Salvando e saindo do jogo...")
            salvar_jogo(estado)
            return False
        else:
            print("Opção inválida! Tente novamente.")

    return True


def menu_principal(estado: Estado) -> bool:
    """Mostra o menu principal enquanto o jogador estiver logado.

    Retorna False se o jogador escolheu sair do jogo.
    """
    while estado.logado:
        mostrar_menu_principal()

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Digite um número válido.")
            continue

        if opcao == 1:
            iniciar_jogo(estado)
        elif opcao == 2:
            logout(estado)
        elif opcao == 3:
            print("Salvando e saindo do jogo...")
            salvar_jogo(estado)
            return False
        else:
            print("Opção inválida! Tente novamente.")

    return True


def main() -> None:
    estado = carregar_jogo()
    if estado is None:
        estado = Estado()

    while True:
        # Requer um login novo depois que o jogo inicia.
        if not lidar_com_signin_login(estado):
            return

        if not menu_principal(estado):
            return


# Executa o jogo quando este arquivo é iniciado diretamente.
if __name__ == "__main__":
    main()
