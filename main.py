
# Exibe o menu principal do jogo com as opções disponíveis para o jogador.
def mostrar_menu():
    print("\n" + "=" * 30)
    print("Escape da Masmorra")
    print("=" * 30)
    print("1 - Iniciar Jogo")
    print("2 - Instruções")
    print("3 - Sair")


# Inicia a partida e permite que o jogador explore a masmorra ou volte ao menu.
def iniciar_jogo():
    print("Você acordou em uma masmorra")
    print("Encontre uma maneira de escapar")

    # Mantém as opções da partida disponíveis até o jogador decidir sair.
    while True:
        print("\n1 - Explorar a Masmorra")
        print("2 - Sair")

        # Recebe a opção escolhida pelo jogador.
        opcao = input("Escolha uma opção: ")

        # Chama a função responsável pela exploração da sala.
        if opcao == "1":
            explorar_sala()

        # Encerra a partida atual e retorna ao menu principal.
        elif opcao == "2":
            print("Voltando para o menu...")
            return

        # Informa ao jogador quando a opção digitada não é válida.
        else:
            print("Opção inválida! Tente novamente...")


# Apresenta as instruções básicas para o jogador entender o objetivo do jogo.
def instrucoes():
    print("\nExplore a masmorra, encontre itens, e tome decisões para escapar")


# Controla o fluxo principal do programa e mantém o menu ativo.
def main():
    # Repete a exibição do menu até o jogador escolher sair do jogo.
    while True:
        mostrar_menu()

        # Lê a opção selecionada no menu principal.
        opcao = input("Escolha uma opção: ")

        # Inicia uma nova partida.
        if opcao == "1":
            iniciar_jogo()

        # Exibe as instruções do jogo.
        elif opcao == "2":
            instrucoes()

        # Encerra o programa e interrompe o laço principal.
        elif opcao == "3":
            print("Saindo do jogo...")
            break

        # Trata opções diferentes das disponíveis no menu.
        else:
            print("Opção inválida! Tente novamente...")


# Verifica se o arquivo está sendo executado diretamente.
# Se estiver, chama a função principal para iniciar o programa.
if __name__ == "__main__":
    main()
