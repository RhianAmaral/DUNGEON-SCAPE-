
"""Funções responsáveis pelos puzzles da masmorra."""

import random


def executar_puzzle_matematico(dificuldade: int) -> bool:
    """Gera uma conta matemática e verifica a resposta do jogador."""

    operacao = random.choice(("+", "-", "*"))
    limite = 10 + dificuldade * 5

    numero1 = random.randint(1, limite)
    numero2 = random.randint(1, limite)

    if operacao == "+":
        resposta_correta = numero1 + numero2

    elif operacao == "-":
        # Organiza os números para evitar resultados negativos.
        numero1, numero2 = max(numero1, numero2), min(numero1, numero2)
        resposta_correta = numero1 - numero2

    else:
        resposta_correta = numero1 * numero2

    print("\nResolva o desafio:")
    print(f"{numero1} {operacao} {numero2}")

    while True:
        try:
            resposta = int(input("Sua resposta: "))
            break
        except ValueError:
            print("Digite um número inteiro válido.")

    if resposta == resposta_correta:
        print("Você acertou!")
        return True

    print(f"Você errou! A resposta correta era {resposta_correta}.")
    return False

