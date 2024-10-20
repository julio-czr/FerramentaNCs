import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class CrudWindow:
    def __init__(self, action, parent, item_id=None):
        self.parent = parent
        self.item_id = item_id
        self.action = action
        self.db = Database()

        # Aumentar o tamanho da janela
        self.janela_crud = tk.Toplevel()
        self.janela_crud.title(f"{action} Não Conformidade")
        self.janela_crud.geometry("700x700")  # Tamanho da janela

        # Variáveis de entrada
        self.secao_var = tk.StringVar()
        self.descricao_var = tk.StringVar()
        self.resultado_var = tk.StringVar()
        self.responsavel_var = tk.StringVar()
        self.prazo_var = tk.StringVar()
        self.observacoes_var = tk.StringVar()
        self.acao_var = tk.StringVar()

        # Carregar dados se a ação for editar
        if action == 'Editar' and item_id:
            self._carregar_dados(item_id)

        # Criar interface
        self._criar_interface()

    def _criar_interface(self):
        # Aumentar o padding e o tamanho dos campos
        padding = 15

        # Estilos adicionais
        label_font = ("Arial", 12)
        entry_font = ("Arial", 12)
        field_width = 45  # Largura uniforme para campos de texto


        # Seção
        tk.Label(self.janela_crud, text="Seção:", font=label_font).grid(row=0, column=0, padx=padding, pady=padding, sticky='e')
        tk.Entry(self.janela_crud, textvariable=self.secao_var, width=field_width, font=entry_font).grid(row=0, column=1, padx=padding, pady=padding)

        # Descrição - Text widget para maior campo
        tk.Label(self.janela_crud, text="Descrição:", font=label_font).grid(row=1, column=0, padx=padding, pady=padding, sticky='ne')
        descricao_text = tk.Text(self.janela_crud, height=5, width=40, font=entry_font)
        descricao_text.grid(row=1, column=1, padx=padding, pady=padding)
        if self.descricao_var.get():
            descricao_text.insert(tk.END, self.descricao_var.get())
        self.descricao_text = descricao_text  # Referência para salvar

        # Resultado - Combobox com tamanho reduzido
        tk.Label(self.janela_crud, text="Resultado:", font=label_font).grid(row=2, column=0, padx=padding, pady=padding, sticky='e')
        resultado_combobox = ttk.Combobox(self.janela_crud, textvariable=self.resultado_var, 
                                          values=["Não verificado", "Sim", "Não", "N/A"], 
                                          width=20, font=entry_font)  # Largura reduzida
        resultado_combobox.grid(row=2, column=1, padx=padding, pady=padding)

        # Responsável
        tk.Label(self.janela_crud, text="Responsável:", font=label_font).grid(row=3, column=0, padx=padding, pady=padding, sticky='e')
        tk.Entry(self.janela_crud, textvariable=self.responsavel_var, width=field_width, font=entry_font).grid(row=3, column=1, padx=padding, pady=padding)

        # Prazo de resolução - Usar Entry padrão
        tk.Label(self.janela_crud, text="Prazo de resolução:", font=label_font).grid(row=4, column=0, padx=padding, pady=padding, sticky='e')
        tk.Entry(self.janela_crud, textvariable=self.prazo_var, width=field_width, font=entry_font).grid(row=4, column=1, padx=padding, pady=padding)

        # Observações - Text widget para maior campo
        tk.Label(self.janela_crud, text="Observações:", font=label_font).grid(row=5, column=0, padx=padding, pady=padding, sticky='ne')
        observacoes_text = tk.Text(self.janela_crud, height=4, width=40, font=entry_font)
        observacoes_text.grid(row=5, column=1, padx=padding, pady=padding)
        if self.observacoes_var.get():
            observacoes_text.insert(tk.END, self.observacoes_var.get())
        self.observacoes_text = observacoes_text  # Referência para salvar

        # Ação corretiva - Text widget para maior campo
        tk.Label(self.janela_crud, text="Ação corretiva:", font=label_font).grid(row=6, column=0, padx=padding, pady=padding, sticky='ne')
        acao_text = tk.Text(self.janela_crud, height=4, width=40, font=entry_font)
        acao_text.grid(row=6, column=1, padx=padding, pady=padding)
        if self.acao_var.get():
            acao_text.insert(tk.END, self.acao_var.get())
        self.acao_text = acao_text  # Referência para salvar

        # Botões
        button_frame = tk.Frame(self.janela_crud)  # Criar frame para centralizar os botões
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)

        # Botão azul (Adicionar ou Editar)
        action_button_text = "Adicionar Não Conformidade" if self.action == 'Adicionar' else "Editar Não Conformidade"
        tk.Button(button_frame, text=action_button_text, command=self._salvar, font=label_font, bg="lightgreen", fg="black", width=25).grid(row=0, column=0, padx=10)

        # Botão vermelho (Cancelar)
        tk.Button(button_frame, text="Cancelar", command=self.janela_crud.destroy, font=label_font, bg="tomato", fg="black", width=15).grid(row=0, column=1, padx=10)

    def _carregar_dados(self, item_id):
        rows = self.db.fetch_all()
        for row in rows:
            if row[0] == item_id:
                self.secao_var.set(row[1])
                self.descricao_var.set(row[2])
                self.resultado_var.set(row[3])
                self.responsavel_var.set(row[4])
                self.prazo_var.set(row[5])  # Agora atribuímos a data diretamente ao Entry
                self.observacoes_var.set(row[6])
                self.acao_var.set(row[7])
                break

    def _salvar(self):
        # Salvar dados dos widgets Text
        self.descricao_var.set(self.descricao_text.get("1.0", tk.END).strip())
        self.observacoes_var.set(self.observacoes_text.get("1.0", tk.END).strip())
        self.acao_var.set(self.acao_text.get("1.0", tk.END).strip())

        prazo = self.prazo_var.get()  # Agora pegamos a data como string

        if self.action == 'Adicionar':
            self.db.insert(self.secao_var.get(), self.descricao_var.get(), self.resultado_var.get(), 
                           self.responsavel_var.get(), prazo, self.observacoes_var.get(), 
                           self.acao_var.get())
        else:
            self.db.update(self.item_id, self.secao_var.get(), self.descricao_var.get(), self.resultado_var.get(), 
                           self.responsavel_var.get(), prazo, self.observacoes_var.get(), 
                           self.acao_var.get())
            messagebox.showinfo("Sucesso", "Não conformidade atualizada com sucesso.")

        self.janela_crud.destroy()
        self.parent.carregar_dados()
