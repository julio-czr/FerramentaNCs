import tkinter as tk
from tkinter import messagebox
from database import Database
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configurações do servidor de e-mail (exemplo: Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "julioramalho01@gmail.com"  # Insira seu e-mail
SMTP_APP_PASSWORD = "nctq wayx lnmt ayby"  # Insira a senha gerada para o aplicativo

def enviar_email(destinatario, assunto, corpo):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = destinatario
    msg['Subject'] = assunto

    msg.attach(MIMEText(corpo, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Inicia a conexão segura
        server.login(SMTP_USER, SMTP_APP_PASSWORD)  # Usando a senha de app
        server.sendmail(SMTP_USER, destinatario, msg.as_string())
        server.quit()
        print(f"E-mail enviado para {destinatario} com o assunto: {assunto}")
        return True
    except Exception as e:
        print(f"Falha ao enviar e-mail para {destinatario}. Erro: {str(e)}")
        return False

class EmailWindow:
    def __init__(self, parent):
        self.janela = tk.Toplevel(parent.janela)
        self.janela.title("Enviar E-mail")

        # Definir o tamanho da janela
        self.janela.geometry("400x300")

        self.db = Database()  # Conexão com o banco de dados

        self._criar_campos()

    def _criar_campos(self):
        tk.Label(self.janela, text="Destinatário:", font=('Arial', 12)).pack(pady=5)
        self.destinatario_entry = tk.Entry(self.janela, font=('Arial', 14), width=30)
        self.destinatario_entry.pack(pady=5)

        # Botão de Enviar E-mail
        botao_enviar = tk.Button(self.janela, text="Enviar E-mail", command=self.enviar_email, font=('Arial', 14), bg="lightgreen")
        botao_enviar.pack(pady=10)
        # Botão vermelho (Cancelar)
        botao_cancelar=tk.Button(self.janela, text="Cancelar", command=self.janela.destroy, font=('Arial', 14), bg="tomato")
        botao_cancelar.pack(pady=10)

    def enviar_email(self):
        destinatario = self.destinatario_entry.get()
        nc_dados = self.db.fetch_all()  # Obtém todos os dados do banco
        falhas = []  # Lista para armazenar falhas no envio

        for nc in nc_dados:
            # Verifica se o resultado é "Não"
            if nc[3] == "Não":  # Supondo que o resultado está na 4ª coluna
                secao, descricao, resultado, responsavel, prazo, observacoes, acao = nc[1:8]
                assunto = f"Correção necessária para {secao}"
                corpo = (
                    f"Prezado(a),\n\n"
                    f"Identificamos que: {observacoes}. Solicitamos que a correção seja feita em até {prazo}.\n\n"
                    f"Ação corretiva: {acao}\n\n"
                    f"Atenciosamente,\n"
                    f"{responsavel}"
                )

                # Envia o e-mail e armazena o resultado
                if not enviar_email(destinatario, assunto, corpo):
                    falhas.append(destinatario)  # Adiciona destinatário à lista de falhas

        # Mensagem de erro ou sucesso
        if falhas:
            messagebox.showerror("Erro", f"Falha ao enviar e-mail para: {', '.join(falhas)}.")
        else:
            messagebox.showinfo("Sucesso", f"E-mails enviados com sucesso para {destinatario}.")
        
        self.janela.destroy()  # Fecha a janela após enviar

