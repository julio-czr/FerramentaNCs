import sqlite3

class Database:
    def __init__(self, db_name="gestao_nao_conformidades.db"):
        self.db_name = db_name
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        conexao = self._connect()
        cursor = conexao.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nao_conformidades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                secao TEXT,
                descricao TEXT,
                resultado TEXT,
                responsavel TEXT,
                prazo TEXT,
                observacoes TEXT,
                acao TEXT
            )
        ''')
        conexao.commit()
        conexao.close()

    def fetch_all(self):
        conexao = self._connect()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM nao_conformidades")
        rows = cursor.fetchall()
        conexao.close()
        return rows

    def insert(self, secao, descricao, resultado, responsavel, prazo, observacoes, acao):
        conexao = self._connect()
        cursor = conexao.cursor()
        cursor.execute('''
            INSERT INTO nao_conformidades (secao, descricao, resultado, responsavel, prazo, observacoes, acao)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (secao, descricao, resultado, responsavel, prazo, observacoes, acao))
        conexao.commit()
        conexao.close()

    def update_resultado(self, item_id, novo_resultado):
            conexao = self._connect()
            cursor = conexao.cursor()
            cursor.execute('''
                UPDATE nao_conformidades SET resultado=? WHERE id=?
            ''', (novo_resultado, item_id))
            conexao.commit()
            conexao.close()
            
    def update(self, item_id, secao, descricao, resultado, responsavel, prazo, observacoes, acao):
        conexao = self._connect()
        cursor = conexao.cursor()
        cursor.execute('''
            UPDATE nao_conformidades SET secao=?, descricao=?, resultado=?, responsavel=?, prazo=?, observacoes=?, acao=?
            WHERE id=?
        ''', (secao, descricao, resultado, responsavel, prazo, observacoes, acao, item_id))
        conexao.commit()
        conexao.close()

    def delete(self, item_id):
        conexao = self._connect()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM nao_conformidades WHERE id=?", (item_id,))
        conexao.commit()
        conexao.close()
