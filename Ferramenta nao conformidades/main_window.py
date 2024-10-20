import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from crud_window import CrudWindow
from email_window import EmailWindow

class MainWindow:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Gestão de Não Conformidades")

        # Aumentar o tamanho da janela principal
        self.janela.geometry("1000x700")

        self.db = Database()

        # Frame principal
        self.frame_principal = tk.Frame(self.janela)
        self.frame_principal.grid(row=0, column=0, sticky="nsew")

        # Configurar grid para que o frame principal preencha a janela
        self.janela.grid_rowconfigure(0, weight=1)
        self.janela.grid_columnconfigure(0, weight=1)

        self._criar_botoes()
        self._criar_tabela()
        self.carregar_dados()

    def _criar_botoes(self):
        frame_botoes = tk.Frame(self.janela)
        frame_botoes.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Botão Adicionar
        botao_adicionar = tk.Button(frame_botoes, text="Adicionar", command=self.adicionar_nao_conformidade, font=('Arial', 14), width=15, height=2, bg="lightgreen")
        botao_adicionar.grid(row=0, column=0, padx=5)

        # Botão Editar
        botao_editar = tk.Button(frame_botoes, text="Editar", command=self.editar_nao_conformidade, font=('Arial', 14), width=15, height=2, bg="lightblue")
        botao_editar.grid(row=0, column=1, padx=5)

        # Botão Remover
        botao_remover = tk.Button(frame_botoes, text="Remover", command=self.remover_nao_conformidade, font=('Arial', 14), width=15, height=2, bg="tomato")
        botao_remover.grid(row=0, column=2, padx=5)

        # Adicionar a label para porcentagem de "Sim" ao lado dos botões
        self.percent_label = tk.Label(frame_botoes, text="Aderencia: 0%", font=('Arial', 12))
        self.percent_label.grid(row=0, column=3, padx=5)

        # Botão Email
        botao_email = tk.Button(frame_botoes, text="Enviar por Email", command=self.enviar_email, font=('Arial', 14), width=15, height=2, bg="lightgreen")
        botao_email.grid(row=0, column=4, padx=5)

    def _criar_tabela(self):
        colunas = ('id', 'secao', 'descricao', 'resultado', 'responsavel', 'prazo', 'observacoes', 'acao')
        self.tabela = ttk.Treeview(self.janela, columns=colunas, show='headings')

        for coluna in colunas:
            self.tabela.heading(coluna, text=coluna.capitalize())
            self.tabela.column(coluna, width=120)

        # Configuração para cores alternadas
        self.tabela.tag_configure('oddrow', background='lightgray')
        self.tabela.tag_configure('evenrow', background='lightgreen')

        # Exibir a tabela com grid
        self.tabela.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        # Configurar para que a tabela expanda conforme a janela
        self.janela.grid_rowconfigure(1, weight=1)
        self.janela.grid_columnconfigure(0, weight=1)

        # Associar evento de clique duplo
        self.tabela.bind("<Double-1>", self._abrir_seletor_resultado)

    def carregar_dados(self):
        # Limpar tabela antes de carregar novos dados
        for i in self.tabela.get_children():
            self.tabela.delete(i)

        rows = self.db.fetch_all()

        count = 0
        for row in rows:
            # Inserir dados na tabela com coloração alternada
            if count % 2 == 0:
                self.tabela.insert('', 'end', values=row, tags=('evenrow',))
            else:
                self.tabela.insert('', 'end', values=row, tags=('oddrow',))
            count += 1

        # Atualiza a porcentagem de "Sim"
        self.atualizar_percentual_sim()

    def _abrir_seletor_resultado(self, event):
        # Identificar a célula clicada
        item_id = self.tabela.identify_row(event.y)
        coluna = self.tabela.identify_column(event.x)

        # Verifica se foi clicado na coluna "Resultado"
        if coluna == '#4':  # A coluna "Resultado" é a quarta coluna (index 3)
            item = self.tabela.item(item_id)
            valor_atual = item['values'][3]

            # Criar um Combobox na célula para edição
            combobox = ttk.Combobox(self.janela, values=["Sim", "Não", "N/A"], state="readonly")
            combobox.set(valor_atual)
            combobox.place(x=event.x_root - self.janela.winfo_rootx(), y=event.y_root - self.janela.winfo_rooty())

            combobox.bind("<<ComboboxSelected>>", lambda e: self._atualizar_resultado(combobox, item_id))
    
    def _atualizar_resultado(self, combobox, item_id):
        novo_resultado = combobox.get()

        # Atualizar na tabela
        self.tabela.item(item_id, values=(
            self.tabela.item(item_id)['values'][0],  # id
            self.tabela.item(item_id)['values'][1],  # secao
            self.tabela.item(item_id)['values'][2],  # descricao
            novo_resultado,                          # novo resultado
            self.tabela.item(item_id)['values'][4],  # responsavel
            self.tabela.item(item_id)['values'][5],  # prazo
            self.tabela.item(item_id)['values'][6],  # observacoes
            self.tabela.item(item_id)['values'][7]   # acao
        ))

        # Atualizar no banco de dados
        self.db.update_resultado(self.tabela.item(item_id)['values'][0], novo_resultado)

        # Atualiza a porcentagem de "Sim"
        self.atualizar_percentual_sim()

        # Fechar Combobox
        combobox.destroy()

    def atualizar_percentual_sim(self):
        rows = self.db.fetch_all()
        sim_count = 0
        sim_nao_count = 0

        for row in rows:
            if row[3] == "Sim":
                sim_count += 1
            if row[3] == "Sim" or row[3] == "Não":
                sim_nao_count += 1

        if sim_nao_count > 0:
            percent_sim = (sim_count / sim_nao_count) * 100
        else:
            percent_sim = 0

        self.percent_label.config(text=f"Aderencia: {percent_sim:.2f}%")

    def adicionar_nao_conformidade(self):
        CrudWindow(action='Adicionar', parent=self)

    def editar_nao_conformidade(self):
        selected_item = self.tabela.selection()
        if selected_item:
            item_id = self.tabela.item(selected_item)['values'][0]
            CrudWindow(action='Editar', parent=self, item_id=item_id)
        else:
            messagebox.showwarning("Seleção", "Selecione uma não conformidade para editar.")

    def remover_nao_conformidade(self):
        selected_item = self.tabela.selection()
        if selected_item:
            item_id = self.tabela.item(selected_item)['values'][0]
            self.db.delete(item_id)
            self.carregar_dados()
            messagebox.showinfo("Sucesso", "Não conformidade removida com sucesso.")
        else:
            messagebox.showwarning("Seleção", "Selecione uma não conformidade para remover.")

    def enviar_email(self):
        EmailWindow(self)

    def run(self):
        self.janela.mainloop()

