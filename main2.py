"""
Sombra e Luz - Círculo Cromático (versão "papel e lápis")

O usuário escolhe uma das 6 cores primárias/secundárias (RGB puras) e o
programa mostra, de forma FIXA e exata, qual cor DO PRÓPRIO CÍRCULO
CROMÁTICO um desenhista usaria para a sombra e qual usaria para a luz --
nada de só misturar com preto/branco (isso deixa a cor "suja"/sem vida).

Regra usada (a mesma que ilustradores chamam de "hue shifting"):
  - No círculo cromático, cada cor tem dois vizinhos (a 60° de distância).
  - LUZ  = o vizinho mais próximo do amarelo (o polo mais "quente").
  - SOMBRA = o vizinho mais próximo do azul (o polo mais "frio").
Ou seja: pra clarear, a cor puxa pro lado quente do círculo; pra
escurecer/sombrear, ela puxa pro lado frio -- sem nunca virar cinza/preto.

Como só temos 6 cores igualmente espaçadas (60° cada), essa regra dá uma
resposta exata e sem ambiguidade pra cada uma delas; por isso a tabela
abaixo é fixa (calculada uma vez, não recalculada em tempo de execução).

Executar:
    python main.py
"""

import math
import tkinter as tk

# Tabela fixa: cor escolhida -> nome, cor de sombra, cor de luz.
# (sombra/luz são sempre outra cor desta mesma lista, nunca uma mistura)
CORES = {
    "#FF0000": {"nome": "Vermelho", "sombra": "#FF00FF", "luz": "#FFFF00"},
    "#FFFF00": {"nome": "Amarelo",  "sombra": "#00FF00", "luz": "#FF0000"},
    "#00FF00": {"nome": "Verde",    "sombra": "#00FFFF", "luz": "#FFFF00"},
    "#00FFFF": {"nome": "Ciano",    "sombra": "#0000FF", "luz": "#00FF00"},
    "#0000FF": {"nome": "Azul",     "sombra": "#FF00FF", "luz": "#00FFFF"},
    "#FF00FF": {"nome": "Magenta",  "sombra": "#0000FF", "luz": "#FF0000"},
}

# Ordem das cores ao redor do círculo (usada só pra desenhar o círculo).
ORDEM_CIRCULO = ["#FFFF00", "#FF0000", "#FF00FF", "#0000FF", "#00FFFF", "#00FF00"]

FONTE_TITULO = ("Segoe UI", 16, "bold")
FONTE_LABEL = ("Segoe UI", 11, "bold")
FONTE_HEX = ("Consolas", 11)


def cor_do_texto(hex_cor: str) -> str:
    """Decide se o texto em cima dessa cor deve ser preto ou branco,
    com base no brilho percebido da cor (evita texto ilegível)."""
    hex_cor = hex_cor.lstrip("#")
    r = int(hex_cor[0:2], 16)
    g = int(hex_cor[2:4], 16)
    b = int(hex_cor[4:6], 16)
    luminancia = 0.299 * r + 0.587 * g + 0.114 * b
    return "#000000" if luminancia > 150 else "#FFFFFF"


class AppSombraLuz(tk.Tk):
    RAIO = 130
    CENTRO = (160, 160)

    def __init__(self):
        super().__init__()
        self.title("Duda Color Assistant")
        self.configure(bg="#222222")
        self.resizable(False, False)

        self._fatias = {}       # hex -> id da fatia no canvas
        self._marcadores = []   # ids de texto (L / S) desenhados por cima

        self._montar_cabecalho()

        corpo = tk.Frame(self, bg="#222222")
        corpo.pack(padx=20, pady=(0, 15))

        self._montar_circulo(corpo)
        self._montar_paleta_e_resultado(corpo)

        # Mostra o vermelho selecionado por padrão, só pra já ter algo na tela.
        self._mostrar_resultado("#FF0000")

    def _montar_cabecalho(self):
        titulo = tk.Label(
            self, text="Escolha uma cor no círculo cromático:",
            font=FONTE_TITULO, bg="#222222", fg="#FFFFFF", pady=12,
        )
        titulo.pack()

    def _montar_circulo(self, pai):
        coluna = tk.Frame(pai, bg="#222222")
        coluna.pack(side="left", padx=(0, 25))

        self.canvas = tk.Canvas(
            coluna, width=320, height=320, bg="#222222", highlightthickness=0
        )
        self.canvas.pack()

        cx, cy = self.CENTRO
        r = self.RAIO
        n = len(ORDEM_CIRCULO)
        angulo_fatia = 360 / n
        # Primeira fatia (amarelo) centralizada no topo (90°).
        inicio = 90 - angulo_fatia / 2

        for i, hex_cor in enumerate(ORDEM_CIRCULO):
            start = inicio + i * angulo_fatia
            item = self.canvas.create_arc(
                cx - r, cy - r, cx + r, cy + r,
                start=start, extent=angulo_fatia,
                fill=hex_cor, outline="#222222", width=3,
                style=tk.PIESLICE,
            )
            self.canvas.tag_bind(item, "<Button-1>",
                                  lambda e, c=hex_cor: self._mostrar_resultado(c))
            self._fatias[hex_cor] = item

        legenda = tk.Label(
            coluna, text="Clique numa fatia do círculo também funciona.",
            font=("Segoe UI", 9), bg="#222222", fg="#AAAAAA",
        )
        legenda.pack(pady=(6, 0))

    def _ponto_na_fatia(self, hex_cor, fracao_raio):
        """Ponto (x, y) no meio angular da fatia dessa cor, a uma fração
        do raio (usado pra desenhar as legendas 'L' e 'S')."""
        cx, cy = self.CENTRO
        r = self.RAIO
        n = len(ORDEM_CIRCULO)
        angulo_fatia = 360 / n
        inicio = 90 - angulo_fatia / 2
        i = ORDEM_CIRCULO.index(hex_cor)
        centro_graus = inicio + i * angulo_fatia + angulo_fatia / 2
        rad = math.radians(centro_graus)
        x = cx + math.cos(rad) * r * fracao_raio
        y = cy - math.sin(rad) * r * fracao_raio
        return x, y

    def _montar_paleta_e_resultado(self, pai):
        coluna = tk.Frame(pai, bg="#222222")
        coluna.pack(side="left")

        paleta = tk.Frame(coluna, bg="#222222")
        paleta.pack(pady=(0, 15))

        for hex_cor in CORES:
            texto = cor_do_texto(hex_cor)
            botao = tk.Button(
                paleta,
                text=CORES[hex_cor]["nome"],
                bg=hex_cor, fg=texto,
                activebackground=hex_cor, activeforeground=texto,
                font=FONTE_LABEL, width=9, height=2,
                relief="raised", bd=2,
                command=lambda c=hex_cor: self._mostrar_resultado(c),
            )
            botao.grid(row=0, column=list(CORES).index(hex_cor), padx=3)

        resultado = tk.Frame(coluna, bg="#222222")
        resultado.pack()

        self.swatch_sombra = self._criar_swatch(resultado, "Sombra (lado frio)")
        self.swatch_original = self._criar_swatch(resultado, "Cor escolhida")
        self.swatch_luz = self._criar_swatch(resultado, "Luz (lado quente)")

        self.swatch_sombra["frame"].pack(side="left", padx=8)
        self.swatch_original["frame"].pack(side="left", padx=8)
        self.swatch_luz["frame"].pack(side="left", padx=8)

    def _criar_swatch(self, pai, titulo):
        frame = tk.Frame(pai, bg="#222222")

        rotulo_titulo = tk.Label(
            frame, text=titulo, font=FONTE_LABEL, bg="#222222", fg="#FFFFFF"
        )
        rotulo_titulo.pack()

        caixa = tk.Frame(frame, width=110, height=90, relief="ridge", bd=2)
        caixa.pack_propagate(False)
        caixa.pack(pady=4)

        rotulo_hex = tk.Label(caixa, text="", font=FONTE_HEX)
        rotulo_hex.pack(expand=True)

        return {"frame": frame, "caixa": caixa, "rotulo_hex": rotulo_hex}

    def _atualizar_swatch(self, swatch, hex_cor, texto_extra=""):
        texto_cor = cor_do_texto(hex_cor)
        swatch["caixa"].configure(bg=hex_cor)
        swatch["rotulo_hex"].configure(
            text=(texto_extra + "\n" if texto_extra else "") + hex_cor,
            bg=hex_cor, fg=texto_cor,
        )

    def _mostrar_resultado(self, hex_cor):
        dados = CORES[hex_cor]
        self._atualizar_swatch(self.swatch_original, hex_cor, dados["nome"])
        self._atualizar_swatch(self.swatch_sombra, dados["sombra"])
        self._atualizar_swatch(self.swatch_luz, dados["luz"])
        self._destacar_no_circulo(hex_cor, dados["sombra"], dados["luz"])

    def _destacar_no_circulo(self, escolhida, sombra, luz):
        # Reseta o contorno de todas as fatias.
        for hex_cor, item in self._fatias.items():
            self.canvas.itemconfigure(item, outline="#222222", width=3)

        # Remove marcadores "S"/"L" antigos.
        for marcador in self._marcadores:
            self.canvas.delete(marcador)
        self._marcadores.clear()

        # Destaca a fatia escolhida com contorno branco grosso.
        self.canvas.itemconfigure(self._fatias[escolhida], outline="#FFFFFF", width=5)

        # Destaca sombra (contorno escuro) e luz (contorno claro), e marca
        # cada uma com um rótulo "S"/"L" pra deixar claro qual é qual.
        self.canvas.itemconfigure(self._fatias[sombra], outline="#000000", width=4)
        self.canvas.itemconfigure(self._fatias[luz], outline="#FFFFFF", width=4)

        x_s, y_s = self._ponto_na_fatia(sombra, 0.55)
        x_l, y_l = self._ponto_na_fatia(luz, 0.55)

        self._marcadores.append(self.canvas.create_text(
            x_s, y_s, text="S", font=("Segoe UI", 14, "bold"),
            fill=cor_do_texto(sombra),
        ))
        self._marcadores.append(self.canvas.create_text(
            x_l, y_l, text="L", font=("Segoe UI", 14, "bold"),
            fill=cor_do_texto(luz),
        ))


if __name__ == "__main__":
    app = AppSombraLuz()
    app.mainloop()