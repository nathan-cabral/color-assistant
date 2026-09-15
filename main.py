import tkinter as tk

janela=tk.Tk()

janela.title("duda color wheel")
janela.geometry("800x600")

title=tk.Label(janela,
               text="Duda Color Assistant",
               font=("Arial",20)
               )

title.pack(pady=20)

frame_colors=tk.Frame(janela)

frame_colors.pack(pady=20)

text_escolha=tk.Label(
    frame_colors,
    text="Escolha uma cor:"
)
frame_colors.pack()

    # cores

red_button=tk.Button(
    frame_colors,
    text="Vermelho",
    bg="#FF0000"
)
red_button.grid(row=0, column=0)

magenta_button=tk.Button(
    frame_colors,
    text="Magenta",
    bg="#FF00FF"
)
magenta_button.grid(row=0, column=2)

yellow_button=tk.Button(
    frame_colors,
    text="Amarelo",
    bg="#FFFF00"
)
yellow_button.grid(row=0, column=1)

green_button=tk.Button(
    frame_colors,
    text="Verde",
    bg="#00FF00"
)
green_button.grid(row=1, column=0)

blue_button=tk.Button(
    frame_colors,
    text="Azul",
    bg="#0000FF"
)
blue_button.grid(row=1, column=1)

ciano_button=tk.Button(
    frame_colors,
    text="Ciano",
    bg="#00FFFF"
)
ciano_button.grid(row=1, column=2)


janela.mainloop()
