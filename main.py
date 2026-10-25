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


def menu_em_texto(estado: Estado) -> None:
    """Menu antigo, no terminal (usado se a janela não puder ser aberta)."""
    while True:
        # Requer um login novo depois que o jogo inicia.
        if not lidar_com_signin_login(estado):
            return

        if not menu_principal(estado):
            return


def abrir_janela_inicial(estado: Estado) -> bool:
    """Abre a janela inicial e retorna True quando o jogador a encerra.

    Retorna False se não foi possível abrir a janela (por exemplo, sem
    tkinter instalado ou sem ambiente gráfico).
    """
    try:
        from components.tela_inicial import JanelaInicial

        janela = JanelaInicial(estado)
    except Exception as erro:
        print(f"Não foi possível abrir a janela inicial ({erro}).")
        print("Usando o menu em texto.")
        return False

    janela.executar()
    return True


def main() -> None:
    estado = carregar_jogo()
    if estado is None:
        estado = Estado()

    if not abrir_janela_inicial(estado):
        menu_em_texto(estado)


# Executa o jogo quando este arquivo é iniciado diretamente.
if __name__ == "__main__":
    main()
