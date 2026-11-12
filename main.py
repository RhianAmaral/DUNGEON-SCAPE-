"""Ponto de entrada do jogo Escape da Masmorra."""

# Importa as funções responsáveis pelo cadastro, login e logout.
from components.contas import cadastro, login, logout

# Importa a classe que armazena o estado atual do jogo.
from components.estado import Estado

# Importa a função responsável por iniciar uma partida.
from components.jogo import iniciar_jogo

# Importa as funções que exibem os menus do jogo.
from components.menus import mostrar_menu_principal, mostrar_menu_signin

# Importa as funções responsáveis por carregar e salvar o progresso.
from components.persistencia import carregar_jogo, salvar_jogo

from components.modelos import Player


def lidar_com_signin_login(estado: Estado) -> bool:
    """Exibe o menu de cadastro e login até o jogador entrar ou sair."""

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


def menu_principal(estado: Estado, jogador: Player) -> bool:
    """Exibe o menu principal enquanto o jogador estiver conectado."""

    while estado.logado:
        mostrar_menu_principal()

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Digite um número válido.")
            continue

        if opcao == 1:
            iniciar_jogo(estado, jogador)

        elif opcao == 2:
            logout(estado)
        elif opcao == 3:
            print("Salvando e saindo do jogo...")
            salvar_jogo(estado)
            return False
        else:
            print("Opção inválida! Tente novamente.")

    return True


def menu_em_texto(estado: Estado, jogador: Player) -> None:
    """Exibe o menu antigo no terminal, caso a janela não possa ser aberta."""

    while True:
        if not lidar_com_signin_login(estado):
            return

        if not menu_principal(estado, jogador):
            return


def abrir_janela_inicial(estado: Estado, jogador: Player) -> bool:
    """Abre a janela inicial e retorna True se ela for aberta com sucesso."""

    try:
        from components.tela_inicial import JanelaInicial

        janela = JanelaInicial(estado, jogador)
    except Exception as erro:
        print(f"Não foi possível abrir a janela inicial ({erro}).")
        print("Usando o menu em texto.")
        return False

    janela.executar()
    return True


def main() -> None:

    jogador = Player(vida=10, ataque=10, defesa=0)

    # Tenta carregar os dados salvos de uma execução anterior.
    estado = carregar_jogo()

    # Cria um novo estado caso não exista um jogo salvo.
    if estado is None:
        estado = Estado()

    # Tenta abrir a janela inicial; se falhar, utiliza os menus no terminal.
    if not abrir_janela_inicial(estado, jogador):
        menu_em_texto(estado, jogador)


# Executa a função principal quando este arquivo é iniciado diretamente.
if __name__ == "__main__":
    main()
