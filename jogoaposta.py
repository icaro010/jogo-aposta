import tkinter as tk
from tkinter import messagebox
import random

class CasinoAdivinhacao:
    def __init__(self, root):
        self.root = root
        self.root.title("Cassino Royale - Adivinhação")
        self.root.geometry("450x400")
        
        # Cores tema cassino / apostas de luxo
        self.bg_principal = "#1A1A1A" # Preto fosco
        self.fg_ouro = "#FC0303"      # Vermelho destaque
        self.fg_texto = "#FFFFFF"     # Branco
        self.bg_card = "#2A2A2A"      # Cinza escuro para destaque
        
        self.root.configure(bg=self.bg_principal)
        
        # Mecânica de aposta
        self.saldo_inicial = 1000
        self.custo_palpite = 50
        self.reiniciar_jogo()
        
        # --- HEADER / SALDO ---
        self.frame_topo = tk.Frame(root, bg=self.bg_card, bd=2, relief="ridge")
        self.frame_topo.pack(fill="x", padx=15, pady=15)
        
        self.lbl_saldo = tk.Label(
            self.frame_topo, 
            text=f"Saldo: ${self.saldo}", 
            font=("Courier New", 16, "bold"), 
            bg=self.bg_card, 
            fg=self.fg_ouro
        )
        self.lbl_saldo.pack(pady=10)
        
        # --- CORPO DO JOGO ---
        self.lbl_instrucoes = tk.Label(
            root, 
            text="Selecione um número de 1 a 100\nCada palpite custa $50!", 
            font=("Arial", 10, "italic"), 
            bg=self.bg_principal, 
            fg="#AAAAAA"
        )
        self.lbl_instrucoes.pack(pady=5)
        
        # Entrada estilizada
        self.txt_palpite = tk.Entry(
            root, 
            font=("Arial Black", 20), 
            justify="center", 
            width=6, 
            bg="#333333", 
            fg=self.fg_ouro, 
            insertbackground="white", 
            bd=3, 
            relief="flat"
        )
        self.txt_palpite.pack(pady=15)
        self.txt_palpite.bind("<Return>", lambda event: self.verificar_palpite())
        
        # Botão estilo Las Vegas
        self.btn_enviar = tk.Button(
            root, 
            text="JOGAR ROLETA", 
            command=self.verificar_palpite, 
            font=("Arial", 12, "bold"), 
            bg="#D4AF37", # Dourado metálico
            fg="#000000", 
            activebackground="#FFD700", 
            activeforeground="#000000", 
            bd=0, 
            padx=20, 
            pady=8, 
            cursor="hand2"
        )
        self.btn_enviar.pack(pady=5)
        
        # Feedback de status
        self.lbl_feedback = tk.Label(
            root, 
            text="A mesa está aberta. Boa sorte!", 
            font=("Arial", 12, "bold"), 
            bg=self.bg_principal, 
            fg="#888888"
        )
        self.lbl_feedback.pack(pady=15)

    def reiniciar_jogo(self):
        self.numero_secreto = random.randint(1, 100)
        if not hasattr(self, 'saldo') or self.saldo <= 0:
            self.saldo = self.saldo_inicial

    def atualizar_interface_saldo(self):
        self.lbl_saldo.config(text=f"Saldo: ${self.saldo}")

    def verificar_palpite(self):
        entrada = self.txt_palpite.get().strip()
        
        if not entrada.isdigit():
            messagebox.showwarning("Erro da Banca", "A banca só aceita números inteiros!")
            self.txt_palpite.delete(0, tk.END)
            return
            
        palpite = int(entrada)
        
        # Deduz o valor da aposta
        self.saldo -= self.custo_palpite
        self.atualizar_interface_saldo()
        
        if palpite < self.numero_secreto:
            self.lbl_feedback.config(text="Banca diz: Muito baixo!", fg="#FF4500")
        elif palpite > self.numero_secreto:
            self.lbl_feedback.config(text="Banca diz: Muito alto!", fg="#FF4500")
        else:
            premio = 300
            self.saldo += premio
            self.atualizar_interface_saldo()
            self.lbl_feedback.config(text="Você ganhou da banca!", fg="#00FF00")
            
            resposta = messagebox.askyesno(
                "Green!", 
                f"Você acertou o número {self.numero_secreto}!\nRecebeu ${premio} de prêmio!\nContinuar apostando?"
            )
            
            if resposta:
                self.reiniciar_jogo()
                self.lbl_feedback.config(text="Nova rodada iniciada!", fg="#888888")
            else:
                self.root.destroy()
                return

        if self.saldo <= 0:
            messagebox.showerror("Fim de Jogo", "Você faliu! A banca levou tudo.")
            resposta = messagebox.askyesno("Reembolsar", "Deseja pegar um empréstimo de $1000 e tentar de novo?")
            if resposta:
                self.saldo = self.saldo_inicial
                self.reiniciar_jogo()
                self.atualizar_interface_saldo()
                self.lbl_feedback.config(text="A mesa está aberta de novo!", fg="#888888")
            else:
                self.root.destroy()
                return
                
        self.txt_palpite.delete(0, tk.END)

if __name__ == "__main__":
    janela = tk.Tk()
    app = CasinoAdivinhacao(janela)
    janela.mainloop()
