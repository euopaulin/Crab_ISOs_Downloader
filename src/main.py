import requests
import os
import tkinter as tk
import threading
from tkinter import filedialog, messagebox
from tkinter import ttk
from isos_lib import isos_disponiveis
from tqdm import tqdm

class ISODownloaderGUI:
    def __init__(self, master):
        self.master = master
        master.title("CRAB ISO's Downloader")
        master.geometry("500x350")

        try:
            self.logo = tk.PhotoImage(file="crab.png")
            master.iconphoto(True, self.logo)
        except tk.TclError:
            print("Logo not found. Still no icon.")

        self.isos = isos_disponiveis
        self.iso_selecionada = None
        self.caminho_destino = None

        self.label_titulo = tk.Label(master, text="Select an ISO to download", font=("Arial", 14), fg=("#f3571a"))
        self.label_titulo.pack(pady=10)

        self.combo_iso = ttk.Combobox(master, state="readonly", width=40)
        self.combo_iso['values'] = [iso['nome_exibicao'] for iso in self.isos.values()]
        self.combo_iso.pack(pady=5)
        self.combo_iso.bind("<<ComboboxSelected>>", self.on_iso_selected)

        self.btn_pasta = tk.Button(master, text="Choose Destination Folder", command=self.obter_caminho_destino)
        self.btn_pasta.pack(pady=5)
        self.label_caminho = tk.Label(master, text="No path selected")
        self.label_caminho.pack(pady=5)

        self.btn_download = tk.Button(master, text="Start Download", command=self.iniciar_download, state=tk.DISABLED)
        self.btn_download.pack(pady=10)

        self.progressbar = ttk.Progressbar(master, orient="horizontal", length=400, mode="determinate")
        self.progressbar.pack(pady=10)

        self.label_status = tk.Label(master, text="Waiting for selection...", font=("Arial", 10))
        self.label_status.pack(pady=5)
        
        tk.Label(master, text="Developed by @euopaulin - 2025", font=("Arial", 8)).pack(side=tk.BOTTOM, pady=5)

    def on_iso_selected(self, event):
        nome_exibicao = self.combo_iso.get()
        for iso_key, iso_data in self.isos.items():
            if iso_data['nome_exibicao'] == nome_exibicao:
                self.iso_selecionada = iso_data
                break
        self.label_status.config(text=f"Selected ISO: {self.iso_selecionada['nome_exibicao']}")
        if self.caminho_destino:
            self.btn_download.config(state=tk.NORMAL)

    def obter_caminho_destino(self):
        self.caminho_destino = filedialog.askdirectory()
        if self.caminho_destino:
            self.label_caminho.config(text=f"Selected folder: {self.caminho_destino}")
            if self.iso_selecionada:
                self.btn_download.config(state=tk.NORMAL)
        else:
            self.caminho_destino = None
            self.btn_download.config(state=tk.DISABLED)

    def iniciar_download(self):
        if not self.iso_selecionada or not self.caminho_destino:
            messagebox.showerror("Erro", "Please select an ISO and a destination folder.")
            return

        self.btn_download.config(state=tk.DISABLED)
        self.label_status.config(text="Starting download...")
        download_thread = threading.Thread(target=self.executar_download_em_thread)
        download_thread.start()

    def executar_download_em_thread(self):
        caminho_arquivo = os.path.join(self.caminho_destino, self.iso_selecionada["nome_arquivo"])

        try:
            response = requests.get(self.iso_selecionada["url"], stream=True)
            response.raise_for_status()

            total_size_in_bytes = int(response.headers.get('content-length', 0))
            self.progressbar["maximum"] = total_size_in_bytes

            with open(caminho_arquivo, 'wb') as f:
                with tqdm(total=total_size_in_bytes, unit='B', unit_scale=True, unit_divisor=1024, leave=False) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
                            self.master.after(0, self.atualizar_barra_de_progresso, pbar.n)
            
            self.master.after(0, self.finalizar_download_sucesso)
        
        except requests.exceptions.RequestException as e:
            self.master.after(0, self.finalizar_download_erro, e)
        except Exception as e:
            self.master.after(0, self.finalizar_download_erro, f"Unexpected error: {e}")

    def atualizar_barra_de_progresso(self, valor):
        self.progressbar['value'] = valor
        self.label_status.config(text=f"Download in progress: {valor/self.progressbar['maximum']:.2%}")

    def finalizar_download_sucesso(self):
        messagebox.showinfo("Success", "Download completed successfully!")
        self.btn_download.config(state=tk.NORMAL)
        self.progressbar['value'] = 0
        self.label_status.config(text="Download complete.")

    def finalizar_download_erro(self, erro):
        messagebox.showerror("Download Error", f"Error downloading: {erro}")
        self.btn_download.config(state=tk.NORMAL)
        self.progressbar['value'] = 0
        self.label_status.config(text="Download failed.")


def main():
    root = tk.Tk()
    app = ISODownloaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()