import random
from dataclasses import dataclass
from time import sleep

#Armazena os nomes de usuário e suas respectivas senhas.
contas = {}

# Alteração: controla se o jogador está conectado.
logado = False

# Contador de eventos, usado para calcular a dificuldade.
tick = 0

# Itens coletados durante a partida.
inventario: list["Item"] = []


@dataclass
class Inimigo:
    """Representa um inimigo encontrado na masmorra."""
    vida: int
    ataque: float
    defesa: float = 0.0
    interacoes: tuple[str, ...] = ("lutar", "fugir", "usar item")


@dataclass
class Item:
    """Representa um item que pode ser encontrado."""
    tipo: str
    atk: float
    dfs: float
    interacoes: tuple[str, ...] = ("pegar", "descartar")


def ler_opcao(mensagem: str, minimo: int, maximo: int) -> int:
    """Lê uma opção numérica e repete a pergunta se ela for inválida."""
    while True:
        try:
            opcao = int(input(mensagem))
            if minimo <= opcao <= maximo:
                return opcao
        except ValueError:
            pass

        print(f"Digite um número entre {minimo} e {maximo}.")


def mostrar_menu() -> None:
    """Exibe o menu principal do jogo."""
    print("\n" + "=" * 30)
    print("Escape da Masmorra")
    print("=" * 30)
    print("1 - Iniciar jogo")
    print("2 - Cadastro")
    print("3 - Login")
    print("4 - Instruções")
    print("5 - Sair")


def spawnar_inimigo(dificuldade: int) -> Inimigo:
    """Cria um inimigo de acordo com a dificuldade atual."""
    vida = 10 + dificuldade
    ataque = dificuldade * 0.6
    defesa = 2 + dificuldade

    print("Um inimigo apareceu!")
    return Inimigo(vida=vida, ataque=ataque, defesa=defesa)


def gerar_loot(dificuldade: int) -> Item:
    """Gera uma arma ou uma armadura de acordo com a dificuldade."""
    tipo = random.choice(("armadura", "arma"))

    if tipo == "armadura":
        ataque = 0
        defesa = 3 + dificuldade
    else:
        ataque = (3 + dificuldade) * 1.5
        defesa = 0

    print("Você encontrou um item!")
    return Item(tipo=tipo, atk=ataque, dfs=defesa)


def gerar_puzzle(dificuldade: int) -> None:
    """Ponto reservado para implementar os puzzles."""
    print(f"Você encontrou um puzzle (dificuldade {dificuldade}).")
    print("Puzzle ainda não implementado.")


def pegar_item(item: Item) -> None:
    """Adiciona o item encontrado ao inventário."""
    inventario.append(item)
    print(f"Item do tipo '{item.tipo}' adicionado ao inventário.")


def lutar(inimigo: Inimigo) -> None:
    """Ponto reservado para implementar o combate."""
    print(
        f"Combate ainda não implementado. "
        f"Inimigo: {inimigo.vida} de vida."
    )


def fugir(inimigo: Inimigo) -> None:
    """Ponto reservado para implementar a fuga do inimigo."""
    print("A fuga ainda não foi implementada.")


def usar_item(inimigo: Inimigo) -> None:
    """Ponto reservado para implementar o uso de itens em combate."""
    if inventario:
        print("O uso de itens ainda não foi implementado.")
    else:
        print("Você não tem itens no inventário.")


def chamar_evento() -> None:
    """Escolhe e executa um evento aleatório da masmorra."""
    global tick
    tick += 1
    dificuldade = tick // 2

    eventos = (spawnar_inimigo, gerar_loot, gerar_puzzle)
    evento = random.choice(eventos)
    resultado = evento(dificuldade)

    if isinstance(resultado, Item):
        print("\nO que deseja fazer?")
        for indice, opcao in enumerate(resultado.interacoes, start=1):
            print(f"{indice} - {opcao}")

        escolha = ler_opcao(
            "Escolha uma opção: ", 1, len(resultado.interacoes)
        )

        if escolha == 1:
            pegar_item(resultado)
        else:
            print("Você descartou o item.")

    elif isinstance(resultado, Inimigo):
        print("\nO que deseja fazer?")
        for indice, opcao in enumerate(resultado.interacoes, start=1):
            print(f"{indice} - {opcao}")

        escolha = ler_opcao(
            "Escolha uma opção: ", 1, len(resultado.interacoes)
        )

        if escolha == 1:
            lutar(resultado)
        elif escolha == 2:
            fugir(resultado)
        else:
            usar_item(resultado)


def explorar_sala() -> None:
    """Explora uma quantidade aleatória de salas."""
    limite_de_salas = 4
    salas_disponiveis = random.randint(1, limite_de_salas)

    for numero_sala in range(1, salas_disponiveis + 1):
        print(f"\nSala {numero_sala}:")
        chamar_evento()

        # Animação simples de exploração.
        print("Explorando salas.", end="\r", flush=True)
        sleep(0.5)
        print("Explorando salas..", end="\r", flush=True)
        sleep(0.5)
        print("Explorando salas...", flush=True)


def iniciar_jogo() -> None:
    """Inicia uma partida e permite explorar ou voltar ao menu."""
    global tick, inventario

    # Alteração: verifica se o jogador está conectado.
    if not logado:
        print("Realize o login para iniciar o jogo.")
        return  # Impede que a partida comece sem login.

    tick = 0
    inventario = []

    print("Você acordou em uma masmorra.")
    print("Encontre uma maneira de escapar.")

    while True:
        print("\n1 - Explorar a masmorra")
        print("2 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            explorar_sala()
        elif opcao == "2":
            print("Voltando para o menu...")
            return
        else:
            print("Opção inválida! Tente novamente.")


def cadastro():
    """Cadastra uma nova conta para o jogador."""
    print("\n" + "=" * 30)
    print("CADASTRO DO JOGO")
    print("=" * 30)

    usuario = input("Crie seu nome de usuário: ")

    if usuario in contas:
        print("Esse usuário já existe!")
        return

    senha = input("Crie sua senha: ")

    contas[usuario] = senha

    print("Cadastro realizado com sucesso!")
    sleep(1)


def login():
    """Realiza o login na conta do jogador."""

    # Alteração: permite modificar a variável global.
    global logado

    print("\n" + "=" * 30)
    print("LOGIN")
    print("=" * 30)

    usuario = input("Digite seu nome de usuário: ")
    senha = input("Digite sua senha: ")

    if usuario in contas and contas[usuario] == senha:
        print(f"\nBem-vindo ao Dungeon Scape, {usuario}!")
        logado = True  # Alteração: registra o login bem-sucedido.
    else:
        print("Usuário ou senha incorretos!")
        logado = False  # Alteração: bloqueia o jogo após login inválido.

    sleep(1)


def instrucoes() -> None:
    """Exibe as instruções básicas do jogo."""
    print(
        "\nExplore a masmorra, encontre itens e tome decisões para escapar."
    )


def main() -> None:
    """Mantém o menu principal ativo até o jogador sair."""
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            iniciar_jogo()
        elif opcao == "2":
            cadastro()
        elif opcao == "3":
            login()
        elif opcao == "4":
            instrucoes()
        elif opcao == "5":
            print("Saindo do jogo...")
            break
        else:
            print("Opção inválida! Tente novamente.")


# Executa o jogo quando este arquivo é iniciado diretamente.
if __name__ == "__main__":
    main()
