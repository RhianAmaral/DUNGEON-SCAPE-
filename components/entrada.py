"""Funções de leitura de dados digitados pelo jogador."""


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
