"""Janela inicial do jogo (menu principal com visual medieval).

A janela usa apenas o tkinter, que já vem com o Python. As imagens ficam na
pasta ``assets`` e existem em três tamanhos; o tamanho é escolhido de acordo
com a altura da tela do jogador.

Os botões são desenhados por cima da imagem de fundo, então dá para mudar
os textos e as ações sem mexer nas imagens.
"""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import font as tkfont

from .comoJogar import TEXTO_COMO_JOGAR, TITULO_COMO_JOGAR
from .contas import autenticar, criar_conta, logout
from .estado import Estado
from .jogo import iniciar_jogo
from .persistencia import salvar_jogo

PASTA_ASSETS = Path(__file__).resolve().parent.parent / "assets"

# Todas as medidas de layout abaixo foram pensadas para a imagem original
# (1518 x 1036) e são multiplicadas pela escala da janela.
LARGURA_REF = 1518
ALTURA_REF = 1036
LARGURAS_DISPONIVEIS = (1280, 1100, 900)

CENTRO_X = 468        # centro horizontal dos botões
PRIMEIRO_Y = 545      # centro vertical do primeiro botão
ESPACO_Y = 74         # distância entre os centros dos botões
ICONE_X = 285         # centro do ícone (botão não selecionado)
TEXTO_X = 333         # início do texto (botão não selecionado)
DESLOCA_SEL = -22     # o botão selecionado é mais largo e "sai" para a esquerda
LARGURA_SEL = (218, 718)
RASTREIO = 4          # espaço extra entre as letras

# Paleta
COR_FUNDO = "#120d0a"
COR_CAMPO = "#1d1611"
COR_BORDA = "#6b4f2a"
COR_OURO = "#c9a15a"
COR_TEXTO = "#cbb892"
COR_TEXTO_SEL = "#f6e8c8"
COR_VERMELHO = "#7a1a14"
COR_VERMELHO_HOVER = "#a02419"
COR_BOTAO = "#241b14"
COR_ERRO = "#e0624a"

FONTES_PREFERIDAS = (
    "Cinzel",
    "Palatino Linotype",
    "Book Antiqua",
    "Georgia",
    "Cambria",
    "Times New Roman",
    "DejaVu Serif",
    "Liberation Serif",
)


def _ativar_dpi_alto() -> None:
    """No Windows, evita que a janela fique borrada em telas com zoom."""
    if sys.platform != "win32":
        return
    try:
        import ctypes

        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


class JanelaInicial:
    """Menu inicial: Iniciar Jogo, Login, Registrar-se, Como Jogar e Sair."""

    def __init__(self, estado: Estado) -> None:
        self.estado = estado

        _ativar_dpi_alto()
        self.root = tk.Tk()
        self.root.title("Dungeon Escape")
        self.root.resizable(False, False)
        self.root.configure(bg=COR_FUNDO)

        self._definir_escala()
        self._criar_fontes()
        self._carregar_imagens()

        self.canvas = tk.Canvas(
            self.root,
            width=self.largura,
            height=self.altura,
            bg=COR_FUNDO,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.img_fundo)

        self.status_id = self.canvas.create_text(
            self.px(CENTRO_X),
            self.px(906),
            text="",
            fill=COR_OURO,
            font=self.fonte_status,
        )

        self.botoes = [
            {"icone": "play", "rotulo": lambda: "Iniciar Jogo", "acao": self.iniciar},
            {
                "icone": "user",
                "rotulo": lambda: "Logout" if self.estado.logado else "Login",
                "acao": self.alternar_login,
            },
            {"icone": "doc", "rotulo": lambda: "Registrar-se", "acao": self.registrar},
            {"icone": "book", "rotulo": lambda: "Como Jogar", "acao": self.como_jogar},
            {"icone": "power", "rotulo": lambda: "Sair", "acao": self.sair},
        ]
        for botao in self.botoes:
            botao["itens"] = []

        self.selecionado = 0
        self._desenhar_tudo()
        self._atualizar_status()

        self.canvas.bind("<Motion>", self._ao_mover)
        self.canvas.bind("<Leave>", lambda _e: self.canvas.config(cursor=""))
        self.canvas.bind("<Button-1>", self._ao_clicar)
        for tecla in ("<Up>", "<Left>"):
            self.root.bind(tecla, lambda _e: self._mover_selecao(-1))
        for tecla in ("<Down>", "<Right>", "<Tab>"):
            self.root.bind(tecla, lambda _e: self._mover_selecao(1))
        for tecla in ("<Return>", "<KP_Enter>", "<space>"):
            self.root.bind(tecla, lambda _e: self._ativar(self.selecionado))
        self.root.protocol("WM_DELETE_WINDOW", self.sair)

        self._centralizar_na_tela()

    # ------------------------------------------------------------ preparação
    def _definir_escala(self) -> None:
        """Escolhe o maior tamanho de imagem que cabe na tela."""
        altura_tela = self.root.winfo_screenheight() - 110
        largura_tela = self.root.winfo_screenwidth() - 40

        escolhida = LARGURAS_DISPONIVEIS[-1]
        for largura in LARGURAS_DISPONIVEIS:
            altura = round(ALTURA_REF * largura / LARGURA_REF)
            if altura <= altura_tela and largura <= largura_tela:
                escolhida = largura
                break

        self.largura = escolhida
        self.altura = round(ALTURA_REF * escolhida / LARGURA_REF)
        self.escala = escolhida / LARGURA_REF

    def px(self, valor: float) -> int:
        """Converte uma medida da imagem original para a escala atual."""
        return round(valor * self.escala)

    def _criar_fontes(self) -> None:
        disponiveis = {nome.lower(): nome for nome in tkfont.families(self.root)}
        familia = "serif"
        for nome in FONTES_PREFERIDAS:
            if nome.lower() in disponiveis:
                familia = disponiveis[nome.lower()]
                break
        self.familia = familia

        def criar(tamanho: int, negrito: bool = False) -> tkfont.Font:
            return tkfont.Font(
                family=familia,
                size=-tamanho,
                weight="bold" if negrito else "normal",
            )

        self.fonte_botao = criar(self.px(30))
        self.fonte_botao_sel = criar(self.px(32))
        self.fonte_status = criar(max(13, self.px(22)))
        self.fonte_titulo = criar(max(18, self.px(34)), negrito=True)
        self.fonte_texto = criar(max(15, self.px(25)))
        self.fonte_campo = criar(max(15, self.px(26)))
        self.fonte_dialogo_botao = criar(max(15, self.px(25)), negrito=True)

    def _imagem(self, nome: str) -> tk.PhotoImage:
        return tk.PhotoImage(file=str(PASTA_ASSETS / f"{nome}_{self.largura}.png"))

    def _carregar_imagens(self) -> None:
        # As referências precisam ficar guardadas, senão o tkinter as apaga.
        self.img_fundo = self._imagem("fundo")
        self.img_botao = self._imagem("botao")
        self.img_botao_sel = self._imagem("botao_sel")
        self.img_icones = {
            nome: self._imagem(f"icone_{nome}")
            for nome in ("play", "user", "doc", "book", "power")
        }

    def _centralizar_na_tela(self) -> None:
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.largura) // 2
        y = max(0, (self.root.winfo_screenheight() - self.altura) // 2 - 20)
        self.root.geometry(f"{self.largura}x{self.altura}+{x}+{y}")

    # --------------------------------------------------------------- desenho
    def _centro_y(self, indice: int) -> int:
        return self.px(PRIMEIRO_Y + ESPACO_Y * indice)

    def _desenhar_botao(self, indice: int) -> None:
        botao = self.botoes[indice]
        for item in botao["itens"]:
            self.canvas.delete(item)
        botao["itens"] = []

        selecionado = indice == self.selecionado
        cy = self._centro_y(indice)
        deslocamento = DESLOCA_SEL if selecionado else 0
        itens = botao["itens"]

        quadro = self.img_botao_sel if selecionado else self.img_botao
        itens.append(self.canvas.create_image(self.px(CENTRO_X), cy, image=quadro))
        itens.append(
            self.canvas.create_image(
                self.px(ICONE_X + deslocamento),
                cy,
                image=self.img_icones[botao["icone"]],
            )
        )
        self._desenhar_texto(
            itens,
            botao["rotulo"](),
            self.px(TEXTO_X + deslocamento),
            cy,
            self.fonte_botao_sel if selecionado else self.fonte_botao,
            COR_TEXTO_SEL if selecionado else COR_TEXTO,
        )

    def _desenhar_texto(self, itens, texto, x, y, fonte, cor) -> None:
        """Escreve o texto letra por letra, para dar espaçamento entre elas."""
        rastreio = self.px(RASTREIO)
        sombra = max(1, self.px(2))
        for letra in texto:
            largura = fonte.measure(letra)
            centro = x + largura / 2
            itens.append(
                self.canvas.create_text(
                    centro + sombra, y + sombra, text=letra, font=fonte, fill="#000000"
                )
            )
            itens.append(
                self.canvas.create_text(centro, y, text=letra, font=fonte, fill=cor)
            )
            x += largura + rastreio

    def _desenhar_tudo(self) -> None:
        # O botão selecionado é desenhado por último para ficar por cima.
        for indice in range(len(self.botoes)):
            if indice != self.selecionado:
                self._desenhar_botao(indice)
        self._desenhar_botao(self.selecionado)

    def _atualizar_status(self) -> None:
        texto = f"Jogador: {self.estado.usuario}" if self.estado.logado else ""
        self.canvas.itemconfigure(self.status_id, text=texto)
        self.canvas.tag_raise(self.status_id)

    # ---------------------------------------------------------------- eventos
    def _botao_em(self, x: int, y: int) -> int | None:
        if not self.px(LARGURA_SEL[0]) <= x <= self.px(LARGURA_SEL[1]):
            return None
        for indice in range(len(self.botoes)):
            if abs(y - self._centro_y(indice)) <= self.px(ESPACO_Y / 2 - 4):
                return indice
        return None

    def _selecionar(self, indice: int) -> None:
        if indice == self.selecionado:
            return
        anterior = self.selecionado
        self.selecionado = indice
        self._desenhar_botao(anterior)
        self._desenhar_botao(indice)
        self.canvas.tag_raise(self.status_id)

    def _mover_selecao(self, passo: int) -> None:
        self._selecionar((self.selecionado + passo) % len(self.botoes))

    def _ao_mover(self, evento: tk.Event) -> None:
        indice = self._botao_em(evento.x, evento.y)
        if indice is None:
            self.canvas.config(cursor="")
            return
        self.canvas.config(cursor="hand2")
        self._selecionar(indice)

    def _ao_clicar(self, evento: tk.Event) -> None:
        indice = self._botao_em(evento.x, evento.y)
        if indice is not None:
            self._selecionar(indice)
            self._ativar(indice)

    def _ativar(self, indice: int) -> None:
        self.botoes[indice]["acao"]()

    def _atualizar_interface(self) -> None:
        self._desenhar_tudo()
        self._atualizar_status()

    # ----------------------------------------------------------------- ações
    def iniciar(self) -> None:
        if not self.estado.logado:
            self.mensagem("Dungeon Escape", "Realize o login para iniciar o jogo.")
            return

        # A partida roda no terminal; a janela some enquanto o jogo roda.
        self.root.withdraw()
        print("\n[Dungeon Escape] A aventura continua aqui no terminal.")
        try:
            iniciar_jogo(self.estado)
        except (KeyboardInterrupt, EOFError):
            print("\nPartida interrompida.")
        finally:
            salvar_jogo(self.estado)
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()

    def alternar_login(self) -> None:
        if self.estado.logado:
            logout(self.estado)
            self._atualizar_interface()
            return

        def validar(valores: dict[str, str]) -> str | None:
            usuario = valores["Usuário"].strip()
            if not autenticar(self.estado, usuario, valores["Senha"]):
                return "Usuário ou senha incorretos!"
            return None

        if self.formulario("Login", ["Usuário", "Senha"], "Entrar", validar):
            self._atualizar_interface()

    def registrar(self) -> None:
        def validar(valores: dict[str, str]) -> str | None:
            usuario = valores["Usuário"].strip()
            senha = valores["Senha"]
            if not usuario:
                return "Informe um nome de usuário."
            if not senha:
                return "Informe uma senha."
            if not criar_conta(self.estado, usuario, senha):
                return "Esse usuário já existe!"
            return None

        if self.formulario("Registrar-se", ["Usuário", "Senha"], "Cadastrar", validar):
            salvar_jogo(self.estado)
            self.mensagem(
                "Registrar-se",
                "Cadastro realizado com sucesso!\nAgora faça o login para jogar.",
            )

    def como_jogar(self) -> None:
        self.mensagem(TITULO_COMO_JOGAR, TEXTO_COMO_JOGAR, largura_texto=560)

    def sair(self) -> None:
        print("Salvando e saindo do jogo...")
        salvar_jogo(self.estado)
        self.root.destroy()

    # --------------------------------------------------------------- diálogos
    def _botao_dialogo(self, pai, texto, comando, principal=False) -> tk.Label:
        cor = COR_VERMELHO if principal else COR_BOTAO
        cor_hover = COR_VERMELHO_HOVER if principal else "#3a2b1e"
        botao = tk.Label(
            pai,
            text=texto,
            font=self.fonte_dialogo_botao,
            fg=COR_TEXTO_SEL,
            bg=cor,
            padx=22,
            pady=7,
            cursor="hand2",
            highlightthickness=1,
            highlightbackground=COR_OURO if principal else COR_BORDA,
        )
        botao.bind("<Enter>", lambda _e: botao.config(bg=cor_hover))
        botao.bind("<Leave>", lambda _e: botao.config(bg=cor))
        botao.bind("<Button-1>", lambda _e: comando())
        return botao

    def _criar_dialogo(self, titulo: str, largura_texto: int):
        top = tk.Toplevel(self.root)
        top.title(titulo)
        top.configure(bg=COR_BORDA)
        top.resizable(False, False)
        top.transient(self.root)

        moldura = tk.Frame(top, bg=COR_FUNDO, padx=self.px(34), pady=self.px(26))
        moldura.pack(padx=2, pady=2)
        tk.Label(
            moldura, text=titulo, font=self.fonte_titulo, fg=COR_OURO, bg=COR_FUNDO
        ).pack()
        tk.Frame(moldura, bg=COR_BORDA, height=1, width=self.px(largura_texto)).pack(
            pady=(8, 12)
        )
        return top, moldura

    def _exibir_dialogo(self, top: tk.Toplevel) -> None:
        """Centraliza o diálogo sobre a janela e espera ele fechar."""
        top.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - top.winfo_width()) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - top.winfo_height()) // 2
        top.geometry(f"+{max(0, x)}+{max(0, y)}")
        try:
            top.wait_visibility()
            top.grab_set()
        except tk.TclError:
            pass
        top.focus_force()
        self.root.wait_window(top)
        self.root.focus_set()

    def mensagem(self, titulo: str, texto: str, largura_texto: int = 460) -> None:
        """Mostra uma mensagem com botão OK."""
        top, moldura = self._criar_dialogo(titulo, largura_texto)
        tk.Label(
            moldura,
            text=texto,
            font=self.fonte_texto,
            fg=COR_TEXTO,
            bg=COR_FUNDO,
            justify="left",
            wraplength=self.px(largura_texto),
        ).pack()
        self._botao_dialogo(moldura, "OK", top.destroy, principal=True).pack(
            pady=(self.px(24), 0)
        )
        top.bind("<Return>", lambda _e: top.destroy())
        top.bind("<Escape>", lambda _e: top.destroy())
        self._exibir_dialogo(top)

    def formulario(self, titulo, campos, rotulo_ok, validar) -> dict[str, str] | None:
        """Mostra campos de texto e só fecha quando ``validar`` aprova.

        ``validar`` recebe os valores digitados e devolve uma mensagem de erro
        (ou None se estiver tudo certo). Retorna os valores ou None se o
        jogador cancelar.
        """
        top, moldura = self._criar_dialogo(titulo, 420)
        entradas: dict[str, tk.Entry] = {}

        for nome in campos:
            tk.Label(
                moldura,
                text=nome,
                font=self.fonte_texto,
                fg=COR_TEXTO,
                bg=COR_FUNDO,
                anchor="w",
            ).pack(fill="x", pady=(8, 3))
            entrada = tk.Entry(
                moldura,
                width=24,
                font=self.fonte_campo,
                show="•" if nome == "Senha" else "",
                bg=COR_CAMPO,
                fg=COR_TEXTO_SEL,
                insertbackground=COR_TEXTO_SEL,
                selectbackground=COR_VERMELHO,
                relief="flat",
                highlightthickness=1,
                highlightbackground=COR_BORDA,
                highlightcolor=COR_OURO,
            )
            entrada.pack(fill="x", ipady=5)
            entradas[nome] = entrada

        erro = tk.Label(
            moldura,
            text="",
            font=self.fonte_texto,
            fg=COR_ERRO,
            bg=COR_FUNDO,
            wraplength=self.px(420),
        )
        erro.pack(pady=(10, 0))

        resultado: dict[str, dict[str, str]] = {}

        def confirmar(_evento=None) -> None:
            valores = {nome: entrada.get() for nome, entrada in entradas.items()}
            mensagem_erro = validar(valores)
            if mensagem_erro:
                erro.config(text=mensagem_erro)
                return
            resultado["valores"] = valores
            top.destroy()

        linha = tk.Frame(moldura, bg=COR_FUNDO)
        linha.pack(pady=(self.px(16), 0))
        self._botao_dialogo(linha, "Cancelar", top.destroy).pack(side="left", padx=6)
        self._botao_dialogo(linha, rotulo_ok, confirmar, principal=True).pack(
            side="left", padx=6
        )

        top.bind("<Return>", confirmar)
        top.bind("<Escape>", lambda _e: top.destroy())
        entradas[campos[0]].focus_set()
        self._exibir_dialogo(top)
        return resultado.get("valores")

    # --------------------------------------------------------------- execução
    def executar(self) -> None:
        self.root.mainloop()
