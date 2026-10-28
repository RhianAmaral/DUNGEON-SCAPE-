
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
    """Exibe o menu de cadastro e login até o jogador entrar ou sair.

    Retorna True se o jogador fizer login e False se escolher sair do jogo.
    """

    # Continua exibindo o menu enquanto o jogador não estiver conectado.
    while not estado.logado:
        mostrar_menu_signin()

        # Solicita a opção escolhida pelo jogador e verifica se é um número.
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Digite um número válido.")
            continue

        # Executa a ação correspondente à opção escolhida.
        if opcao == 1:
            cadastro(estado)
        elif opcao == 2:
            login(estado)
        elif opcao == 3:
            # Salva o estado atual antes de encerrar o jogo.
            print("Salvando e saindo do jogo...")
            salvar_jogo(estado)
            return False
        else:
            # Informa ao jogador que a opção não existe no menu.
            print("Opção inválida! Tente novamente.")

    # Retorna True quando o jogador estiver conectado.
    return True


def menu_principal(estado: Estado) -> bool:
    """Exibe o menu principal enquanto o jogador estiver conectado.

    Retorna False se o jogador escolher sair do jogo.
    """

    # Mantém o menu principal ativo enquanto o jogador estiver conectado.
    while estado.logado:
        mostrar_menu_principal()

        # Solicita a opção escolhida pelo jogador.
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Digite um número válido.")
            continue

        # Executa a ação correspondente à opção escolhida.
        if opcao == 1:
            iniciar_jogo(estado)
        elif opcao == 2:
            # Encerra a sessão do jogador.
            logout(estado)
        elif opcao == 3:
            # Salva o progresso antes de sair do jogo.
            print("Salvando e saindo do jogo...")
            salvar_jogo(estado)
            return False
        else:
            # Informa ao jogador que a opção é inválida.
            print("Opção inválida! Tente novamente.")

    # Retorna True quando o jogador sair do menu principal, por exemplo, ao fazer logout.
    return True


def menu_em_texto(estado: Estado) -> None:
    """Exibe o menu antigo no terminal, caso a janela não possa ser aberta."""

    # Mantém o fluxo de menus em execução.
    while True:
        # Solicita que o jogador faça login antes de acessar o menu principal.
        if not lidar_com_signin_login(estado):
            return

        # Exibe o menu principal enquanto o jogador estiver conectado.
        if not menu_principal(estado):
            return


def abrir_janela_inicial(estado: Estado, jogador: Player) -> bool:
    """Abre a janela inicial e retorna True se ela for aberta com sucesso.

    Retorna False se não for possível abrir a janela, por exemplo,
    se o tkinter não estiver disponível ou não houver ambiente gráfico.
    """

    # Tenta importar e criar a janela inicial do jogo.
    try:
        from components.tela_inicial import JanelaInicial

        janela = JanelaInicial(estado, jogador)
    except Exception as erro:
        # Informa o motivo da falha e indica que será usado o terminal.
        print(f"Não foi possível abrir a janela inicial ({erro}).")
        print("Usando o menu em texto.")
        return False

    # Inicia a execução da janela.
    janela.executar()
    return True


def main() -> None:

    jogador = Player(vida=100, ataque=10, defesa=0)

    # Tenta carregar os dados salvos de uma execução anterior.
    estado = carregar_jogo()

    # Cria um novo estado caso não exista um jogo salvo.
    if estado is None:
        estado = Estado()

    # Tenta abrir a janela inicial; se falhar, utiliza os menus no terminal.
    if not abrir_janela_inicial(estado, jogador):
        menu_em_texto(estado)


# Executa a função principal quando este arquivo é iniciado diretamente.
if __name__ == "__main__":
    main()
