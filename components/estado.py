
"""Estado compartilhado do jogo (substitui as variáveis globais)."""

# Importa os recursos necessários para criar uma classe de dados.
from dataclasses import dataclass, field

# Importa a classe Item, utilizada para representar os itens do jogo.
from .modelos import Item


@dataclass
class Estado:
    """Armazena tudo o que muda durante a execução do jogo."""

    # Armazena os nomes de usuário e suas respectivas senhas.
    contas: dict[str, str] = field(default_factory=dict)

    # Controla se o jogador está conectado.
    logado: bool = False

    # Armazena o nome do jogador conectado (vazio quando ninguém está logado).
    usuario: str = ""

    # Conta os eventos ocorridos, sendo utilizado para calcular a dificuldade.
    tick: int = 0

    # Armazena os itens coletados durante a partida.
    inventario: list[Item] = field(default_factory=list)

    # Armazena o número da sala atual da exploração.
    sala_atual: int = 1

    # Define os atributos de vida do jogador.
    vida_maxima: int = 100
    vida: int = 100

    # Define os atributos básicos de combate do jogador.
    ataque_base: int = 10
    defesa_base: int = 0

    # Armazena a quantidade de moedas do jogador.
    moedas: int = 0

    # Armazena os equipamentos utilizados pelo jogador.
    arma_equipada: Item | None = None
    armadura_equipada: Item | None = None

    def reiniciar_partida(self) -> None:
        """Reinicia o progresso e os atributos do jogador para uma nova partida."""

        # Zera o contador de eventos.
        self.tick = 0

        # Remove todos os itens do inventário.
        self.inventario.clear()

        # Retorna o jogador à primeira sala.
        self.sala_atual = 1

        # Restaura a vida máxima do jogador.
        self.vida = self.vida_maxima

        # Restaura os atributos básicos de combate.
        self.ataque_base = 10
        self.defesa_base = 0

        # Zera a quantidade de moedas.
        self.moedas = 0

        # Remove os equipamentos atualmente utilizados.
        self.arma_equipada = None
        self.armadura_equipada = None
