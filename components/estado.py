"""Estado compartilhado do jogo (substitui as variáveis globais)."""

from dataclasses import dataclass, field

from .modelos import Item


@dataclass
class Estado:
    """Guarda tudo o que muda durante a execução do jogo."""
    # Nomes de usuário e suas respectivas senhas.
    contas: dict[str, str] = field(default_factory=dict)
    # Controla se o jogador está conectado.
    logado: bool = False
    # Nome do jogador conectado (vazio quando ninguém está logado).
    usuario: str = ""
    # Contador de eventos, usado para calcular a dificuldade.
    tick: int = 0
    # Itens coletados durante a partida.
    inventario: list[Item] = field(default_factory=list)

    def reiniciar_partida(self) -> None:
        """Zera o progresso da partida (tick e inventário)."""
        self.tick = 0
        self.inventario = []
