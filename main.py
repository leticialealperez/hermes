import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import pywhatkit
import time
import random
from threading import Thread

root = tk.Tk()
root.title("Nova Acrópole - Hermes Trismegisto")
root.geometry("600x500")

csv_path = tk.StringVar()
tipo_mensagem = tk.StringVar(value="texto")
midia_path = tk.StringVar()
mensagem_texto_widget = None

def selecionar_csv():
    path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    csv_path.set(path)

def selecionar_midia():
    path = filedialog.askopenfilename(filetypes=[("Imagem", "*.png;*.jpg;*.jpeg")])
    midia_path.set(path)

def atualizar_campos():
    tipo = tipo_mensagem.get()
    for widget in frame_campos.winfo_children():
        widget.destroy()

    global mensagem_texto_widget
    mensagem_texto_widget = None

    if tipo in ["texto", "imagem_texto"]:
        tk.Label(frame_campos, text="Mensagem de texto:").pack(anchor='w')
        mensagem_texto_widget = tk.Text(frame_campos, height=5, width=80, wrap=tk.WORD)
        mensagem_texto_widget.pack()

    if tipo in ["imagem", "imagem_texto"]:
        tk.Button(frame_campos, text="Selecionar imagem", command=selecionar_midia).pack()
        tk.Label(frame_campos, textvariable=midia_path).pack()

def log(msg):
    log_box.config(state=tk.NORMAL)
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)
    log_box.config(state=tk.DISABLED)
    root.update()

def enviar_mensagens():
    if not csv_path.get():
        messagebox.showerror("Erro", "Selecione o arquivo CSV.")
        return

    try:
        contatos = pd.read_csv(csv_path.get())
    except:
        messagebox.showerror("Erro", "Não foi possível ler o arquivo CSV.")
        return

    if 'telefone' not in contatos.columns:
        messagebox.showerror("Erro", "O CSV deve conter uma coluna chamada 'telefone'.")
        return

    tipo = tipo_mensagem.get()
    texto = mensagem_texto_widget.get("1.0", tk.END).strip() if mensagem_texto_widget else ""
    midia = midia_path.get()

    if tipo in ["texto", "imagem_texto"] and not texto:
        messagebox.showerror("Erro", "Digite a mensagem de texto.")
        return

    if tipo in ["imagem", "imagem_texto"] and not midia:
        messagebox.showerror("Erro", "Selecione a imagem.")
        return

    conectado = messagebox.askokcancel(
        "Conectar ao WhatsApp Web",
        "Abra o WhatsApp Web no seu navegador e escaneie o QR Code com seu celular.\n"
        "Clique em OK para iniciar o envio após confirmar que está conectado."
    )

    if not conectado:
        log("❌ Envio cancelado pelo usuário.")
        return

    total = len(contatos)
    progress["value"] = 0
    progress["maximum"] = total

    for i, row in contatos.iterrows():
        numero = f"+{str(row['telefone']).strip()}"

        try:
            if tipo == "texto":
                pywhatkit.sendwhatmsg_instantly(
                    numero, 
                    texto, 
                    wait_time=random.uniform(15, 20), 
                    tab_close=True,
                    close_time=random.uniform(3, 4)
                )
                log(f"[✓] Mensagem de texto enviada para {numero}")

            elif tipo == "imagem":
                pywhatkit.sendwhats_image(
                    receiver=numero, 
                    img_path=midia, 
                    caption="",
                    wait_time=random.uniform(15, 20), 
                    tab_close=True,
                    close_time=random.uniform(3, 4)
                )
                log(f"[✓] Imagem enviada para {numero}")

            elif tipo == "imagem_texto":
                pywhatkit.sendwhats_image(
                    receiver=numero, 
                    img_path=midia, 
                    caption=texto,
                    wait_time=random.uniform(15, 20),  
                    tab_close=True,
                    close_time=random.uniform(3, 4)
                )
                log(f"[✓] Imagem com legenda enviada para {numero}")

        except Exception as e:
            log(f"[x] Erro ao enviar para {numero}: {e}")

        progress["value"] = i + 1
        root.update()
        time.sleep(random.uniform(3, 5))  # tempo randômico entre envios

    messagebox.showinfo("Concluído", "Todas as mensagens foram processadas.")
    log("✔️ Envio concluído com sucesso.")

def enviar_thread():
    Thread(target=enviar_mensagens).start()

# Interface
tk.Label(root, text="Arquivo CSV com contatos:").pack(anchor='w', padx=10)
tk.Button(root, text="Selecionar CSV", command=selecionar_csv).pack()
tk.Label(root, textvariable=csv_path).pack()

tk.Label(root, text="Tipo de mensagem:").pack(anchor='w', padx=10)
tipos = [
    ("Apenas texto", "texto"),
    ("Apenas imagem", "imagem"),
    ("Imagem com legenda", "imagem_texto"),
]
for text, value in tipos:
    tk.Radiobutton(root, text=text, variable=tipo_mensagem, value=value, command=atualizar_campos).pack(anchor='w')

frame_campos = tk.Frame(root)
frame_campos.pack(pady=10)
atualizar_campos()

tk.Button(root, text="Enviar Mensagens", bg="green", fg="white", command=enviar_thread).pack(pady=10)

progress = ttk.Progressbar(root, length=400, mode='determinate')
progress.pack(pady=5)

tk.Label(root, text="Logs:").pack()
log_box = tk.Text(root, height=10, width=70)
log_box.pack(padx=10, pady=5)
log_box.config(state=tk.DISABLED)

root.mainloop()
