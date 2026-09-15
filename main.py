import tkinter as tk
janela=tk.Tk()
janela.title("duda color wheel")
janela.geometry("1000x800")

title=tk.Label(janela,
               text="Color Assistant",
               font=("Arial",20)
               )
title.pack(pady=20)

janela.mainloop()
